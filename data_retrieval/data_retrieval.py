import os
from typing import Any, List, Dict, Type
import subprocess
import threading
from datetime import datetime, timedelta

import slurm2sql
import sqlite3
#from prometheus_api_client import PrometheusConnect
from prometheus_api_client.prometheus_connect import PrometheusConnect

from data_retrieval.squeue import SQUEUE
from models.models import (
    Job,
    RunningJob,
    FinishedJob,
    Resources,
    GPUResources,
    JobEfficiency,
    PrometheusVectorResult,
    PrometheusMatrixResult,
    VectorResult,
    TimeStampValue
)
db = None
db_time = None
queue = None
current_jobs = None | List[Job]
lock = threading.Lock()

#prometheus_server = "http://stats.triton.aalto.fi:9090"
prometheus_server = "http://localhost:8081"
prometheus_client = PrometheusConnect(url =prometheus_server, disable_ssl=True)

def fetch_vector_result(query: str, output_type : Type ) -> Dict[int,Any]:
    """ fetch a vector result from prometheus"""
    result = PrometheusVectorResult.model_validate(prometheus_client.custom_query(query=query)).to_vector_result()
    output_dict : Dict[int,Any]= {}
    for entry in result.value:                
        jid = entry.metric.slurmjobid
        if jid is None:
            continue
        value = entry.value # The first is the time point, the second is the value
        if value is None:
            continue
        output_dict[jid] = output_type(value)
    return output_dict

def fetch_matrix_result(query: str, output_type : Type ) -> Dict[int,List[TimeStampValue]]:
    """ Fetch a matrix result (one vector per slurmjobid) from prometheus"""
    result = PrometheusMatrixResult.model_validate(prometheus_client.custom_query_range(query=query, start_time=datetime.now()-timedelta(days=30), end_time=datetime.now(), step="1d")).to_matrix_result(output_type)
    output_dict : Dict[int,List[Any]]= {}
    for entry in result.values:        
        jid = entry.metric.slurmjobid
        if jid is None:
            continue            
        values = entry.values
        output_dict[jid] = values
    return output_dict

def fetch_max_gpu_memories(job_id: List[int]) -> Dict[int,int]:   
    """Fetch the maximum GPU memory used from prometheus"""
    # we want the max of the sum of all memory usages for all gpus used in the job
    query = f'max by (slurmjobid) (sum by (slurmjobid) (max_over_time(slurm_job_memory_max{{slurmjobid=~"{ "|".join(map(str, job_id)) }"}}[30d]))'
    return fetch_vector_result(query, int)    

def fetch_average_gpu_usage(job_id: List[int]) -> Dict[int,float]:   
    """Fetch the average GPU usage of a job from prometheus"""
    query = f'avg by (slurmjobid) (avg_over_time (slurm_job_utilization_gpu{{slurmjobid=~"{ "|".join(map(str, job_id)) }"}}[30d]))'
    return fetch_vector_result(query, float)




# create Database
def fetch_jobs() -> None:
    """ Fetch list of jobs for user """
    global db, db_time, queue, current_jobs
    # we don't always update.
    with lock:
        if (
            db is None
            or datetime.now() - db_time > timedelta(seconds=15)
            or current_jobs == None
        ):
            db = sqlite3.connect(":memory:")
            slurm2sql.slurm2sql(
                db, ["-S", "now-2weeks", "-u", os.environ.get("USER")], update=True
            )
            db_time = datetime.now()
            queue = SQUEUE()
            jobs = db.cursor().execute(
                "SELECT * FROM eff WHERE State IN ('RUNNING', 'PENDING', 'COMPLETED', 'FAILED', 'COMPLETING')"
            )
            headers = extractHeader(jobs.description)
            current_jobs = [
                convert_DB_to_Job(db_job=DBJob(result, headers), queue=queue)
                for result in jobs
            ]


def fetch_running_jobs() -> List[RunningJob]:
    # possibly update jobs
    fetch_jobs()
    assert current_jobs is not None
    return [job for job in current_jobs if isinstance(job, RunningJob)]


def fetch_finished_jobs() -> List[FinishedJob]:
    # possibly update jobs
    fetch_jobs()
    assert current_jobs is not None
    return [job for job in current_jobs if isinstance(job, FinishedJob)]


def run_command(command: str) -> str | None:
    try:
        # Run the command and capture the output
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout  # Return the standard output
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
        return None


def extractHeader(db_headers):
    header_dict = {}
    for i in range(len(db_headers)):
        header_dict[db_headers[i][0]] = i
    return header_dict


class DBJob:
    def __init__(self, db_result, headers):
        # print(headers)
        # print(db_result)
        self.headers = headers
        self.result = db_result

    def get(self, field, type=str):
        try:
            value = self.result[self.headers[field]]
            return type(value) if not value is None else None
        except:
            return None


def convert_DB_to_Job(db_job: DBJob, queue: SQUEUE) -> Job:

    id = db_job.get("JobID")
    # print(f"ID: {id}")
    name = db_job.get("JobName")
    commands = db_job.get("SubmitLines")
    if commands is None:
        commands = ["Unknown"]
    else:
        commands = db_job.get("SubmitLines").split("\n")
    # print(f"Commands: {commands}")
    # print(f"Commands: {commands}")
    status = db_job.get("State")
    running = status == "PENDING" or status == "RUNNING"
    # print(f" State: {status}")
    time = db_job.get("Timelimit")
    # print(f" Timelimit: {time}")
    delta = None
    if not time is None:
        try:
            t = datetime.strptime(time, "%d-%H:%M:%S")
        except:
            try:
                t = datetime.strptime(time, "%H:%M:%S")
            except:
                t = datetime.min + timedelta(seconds=float(time))

        delta = timedelta(days=t.day, hours=t.hour, minutes=t.minute, seconds=t.second)
    startTime = db_job.get("Start")
    # print(f" Start: {startTime}")
    # print(f" Start: {startTime}")
    if startTime is None:
        queue_start = queue.get_start_time(id)
        if queue_start == None:
            startTime = None
        else:
            startTime = datetime.fromisoformat(queue.get_start_time(id))
    else:
        startTime = datetime.fromtimestamp(int(startTime))
    endTime = db_job.get("End")
    if endTime is None:
        if not startTime is None:
            if delta is None:
                endTime = "unknown"
            else:
                endTime = startTime + delta
    else:
        endTime = datetime.fromtimestamp(int(endTime))
    # print(f" End: {endTime}")
    cpus = db_job.get("NCPUS", int)
    if cpus is None:
        cpus = 0
    # print(cpus)
    memory = db_job.get("MemReq", int)
    if memory is None:
        memory = 0
    # print(memory)
    gpus = db_job.get("NGpus", int)
    # print(gpus)
    nodes = db_job.get("NNodes", int)
    # print(nodes)
    nodeList = db_job.get("NodeList")
    # print(nodeList)
    gpu_type = db_job.get("GPUType")
    # print(gpu_type)
    gpu_eff = db_job.get("GPUeff", float)
    if gpu_eff:
        gpu_eff = gpu_eff * 100
    cpu_eff = db_job.get("CPUeff", float)
    if cpu_eff:
        cpu_eff = cpu_eff * 100
    mem_eff = db_job.get("MemEff", float)
    if mem_eff:
        mem_eff = mem_eff * 100
    alloc_nodes, expected_nodes = queue.get_nodes(id)
    used_nodes = expected_nodes if status == "PENDING" else alloc_nodes
    if used_nodes == None:
        used_nodes = "unknown"

    gpu_res = None if gpus is None else GPUResources(amount=gpus, type=gpu_type)
    res = Resources(cpus=cpus, memory=memory, gpu=gpu_res)
    if running:
        return RunningJob(
            id=id,
            status=status,
            name=name,
            nodes=nodes,
            startTime=startTime,
            endTime=endTime,
            resources=res,
            command=commands[0],
        )
    else:
        efficiency = JobEfficiency(cpu=cpu_eff, memory=mem_eff, gpu=gpu_eff)
        # print(efficieny)
        job = FinishedJob(
            id=id,
            status=status,
            name=name,
            nodes=nodes,
            startTime=startTime,
            endTime=endTime,
            resources=res,
            efficiency=efficiency,
            command=commands[0],
        )
        return job
