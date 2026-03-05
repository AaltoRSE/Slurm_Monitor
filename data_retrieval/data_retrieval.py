import os
from typing import Any, List, Dict, Type, Union
import subprocess
import threading
from datetime import datetime, timedelta

import slurm2sql
import sqlite3
#from prometheus_api_client import PrometheusConnect
from prometheus_api_client.prometheus_connect import PrometheusConnect
from data_retrieval.job_classes import DBJob
from data_retrieval.squeue import SQUEUE
from models.models import (
    GPUGraphData,
    Job,
    RunningJob,
    FinishedJob,
    Resources,
    GPUResources,
    JobEfficiency,
    PrometheusVectorResult,
    PrometheusMatrixResult,
    VectorResult,
    TimeStampValue,
    VectorValue
)
from logger import get_logger
logger = get_logger()
db = None
db_time = None
queue = None
current_jobs : Union[None, List[Job]] = None
lock = threading.Lock()

prometheus_server = "http://stats.triton.aalto.fi:9090"
prometheus_client = PrometheusConnect(url =prometheus_server, disable_ssl=True)

def get_average(values: List[VectorValue]) -> Union[float, None]:
    all_values = [float(val) for vector in values for val in vector.get_values()]
    if not all_values:
        return None
    return sum(all_values) / len(all_values)

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

def fetch_matrix_for_normal_query(query: str, output_type : Union[Type, None] = None) -> Dict[int,Any]:
    """ fetch a vector result from prometheus"""
    result = PrometheusMatrixResult.model_validate(prometheus_client.custom_query(query=query)).to_matrix_result(output_type)
    output_dict : Dict[int,Any]= {}
    for entry in result.values:        
        jid = entry.metric.slurmjobid
        if jid is None:
            continue            
        if not jid in output_dict:
            output_dict[jid] = []
        output_dict[jid].append(entry)
    return output_dict

def fetch_matrix_result(query: str, output_type : Type = TimeStampValue, start_time: Union[datetime, None] = None, end_time: Union[datetime, None] = None, step : Union[str, float] = "1d" ) -> Dict[int,List[VectorValue]]:
    """ Fetch a matrix result (one vector per slurmjobid) from prometheus"""
    if start_time is None:
        start_time = datetime.now() - timedelta(days=30)
    if end_time is None:
        end_time = datetime.now()
    result = PrometheusMatrixResult.model_validate(
        prometheus_client.custom_query_range(query=query,
                                             start_time=start_time, 
                                             end_time=end_time, 
                                             step=step)).to_matrix_result(output_type)
    output_dict : Dict[int,List[VectorValue]]= {}
    for entry in result.values:        
        jid = entry.metric.slurmjobid
        if jid is None:
            continue            
        if not jid in output_dict:
            output_dict[jid] = []
        output_dict[jid].append(entry)
    return output_dict

def fetch_max_gpu_memories(job_id: List[int]) -> Dict[int,int]:   
    """Fetch the maximum GPU memory used from prometheus"""
    # we want the max of the sum of all memory usages for all gpus used in the job
    query = f'max by (slurmjobid) (sum by (slurmjobid) (max_over_time(slurm_job_memory_usage_gpu{{account!="error", slurmjobid=~"{ "|".join(map(str, job_id)) }"}}[30d])))'
    return fetch_vector_result(query, int)

def fetch_max_individual_gpu_memories(job_id: List[int]) -> Dict[int,int]:   
    """Fetch the maximum GPU memory used from prometheus for a single gpu"""
    # we want the max of the sum of all memory usages for all gpus used in the job
    query = f'max by (slurmjobid) (max by (slurmjobid, gpu) (max_over_time(slurm_job_memory_usage_gpu{{account!="error", slurmjobid=~"{ "|".join(map(str, job_id)) }"}}[30d])))'
    return fetch_vector_result(query, int)

def fetch_average_gpu_usage(job_id: List[int]) -> Dict[int,float]:   
    """Fetch the average GPU usage of a job from prometheus"""
    query = f'avg by (slurmjobid) (avg_over_time (slurm_job_utilization_gpu{{ account!="error", slurmjobid=~"{ "|".join(map(str, job_id)) }"}}[30d]))'
    return fetch_vector_result(query, float)

def fetch_gpu_usage_over_time(job_id: int, user: str) -> List[VectorValue]:
    """Fetch the GPU usage of a set of job over time from prometheus"""
    result = fetch_matrix_for_normal_query(f'slurm_job_utilization_gpu{{ user="{user}", account!="error", slurmjobid="{job_id}"}}')
    return result[job_id] if job_id in result else []

def fetch_gpu_mem_over_time(job_id: int, user: str) -> List[VectorValue]:
    """Fetch the GPU usage of a set of job over time from prometheus"""
    result = fetch_matrix_for_normal_query(f'slurm_job_memory_usage_gpu{{ user="{user}", account!="error", slurmjobid="{job_id}"}}')
    return result[job_id] if job_id in result else []


def get_job_start_time(job: DBJob, queue: Union[SQUEUE, None]) -> Union[datetime, None]:
    startTime = job.get("Start")
    if startTime is None:
        if queue is None:
            return None
        queue_start = queue.get_start_time(job.get("JobID"))
        if queue_start == None:
            return None
        else:
            return datetime.fromisoformat(queue_start)
    else:
        return datetime.fromtimestamp(int(startTime))

def fetch_gpu_graphs(job_id: int) -> GPUGraphData:
    user = os.environ.get("USER")
    if user is None:
        raise ValueError("USER environment variable not set")
    gpu_usage = fetch_gpu_usage_over_time(job_id, user)
    gpu_mem = fetch_gpu_mem_over_time(job_id, user)
    return GPUGraphData(gpu_usage=gpu_usage, gpu_mem=gpu_mem)

# create Database
def fetch_jobs() -> None:
    """ Fetch list of jobs for user """
    global db, db_time, queue, current_jobs
    logger.info("Fetching jobs from database...")
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
            db_jobs = [DBJob(result, headers)for result in jobs]
            job_ids = [db_job.get("JobID", int) for db_job in db_jobs]
            logger.info("Fetching data from prometheus..")
            gpu_mem_max = fetch_max_gpu_memories(job_ids)
            gpu_individual_mem_max = fetch_max_individual_gpu_memories(job_ids)
            gpu_utilization_average = fetch_average_gpu_usage(job_ids)            
            logger.info("Data retrieved proceeding...")
            for job in db_jobs:
                job_id = job.get("JobID", int)
                gpu_job = job.get("NGpus", int)
                if gpu_job is not None and gpu_job > 0:                
                    job.set("GPUMemTotalMax", gpu_mem_max[job_id] if job_id in gpu_mem_max else None)
                    job.set("GPUMemIndividualMax", gpu_individual_mem_max[job_id] if job_id in gpu_individual_mem_max else None)
                    job.set("GPUAverageUtil", gpu_utilization_average[job_id] if job_id in gpu_utilization_average else None)                                                                        
            logger.info("Building jobs")
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


def run_command(command: str) -> Union[str, None]:
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
    gpu_eff = db_job.get("GPUAverageUtil", float)
    gpu_mem_max = db_job.get("GPUMemTotalMax", int)
    gpu_individual_mem_max = db_job.get("GPUMemIndividualMax", int)
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
        efficiency = JobEfficiency(cpu=cpu_eff, memory=mem_eff, gpu=gpu_eff, gpu_total_mem=gpu_mem_max, gpu_individual_mem=gpu_individual_mem_max)
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
