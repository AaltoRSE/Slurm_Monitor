import os
import subprocess
import slurm2sql
from typing import List

import sqlite3
import threading
from datetime import datetime, timedelta
from models.models import (
    Job,
    RunningJob,
    FinishedJob,
    Resources,
    GPUResources,
    JobEfficiency,
)
from data_retrieval.squeue import SQUEUE

db = None
db_time = None
queue = None
current_jobs = None
lock = threading.Lock()


# create Database
def fetch_jobs() -> List[Job]:
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
    return [job for job in current_jobs if isinstance(job, RunningJob)]


def fetch_finished_jobs() -> List[RunningJob]:
    # possibly update jobs
    fetch_jobs()
    return [job for job in current_jobs if isinstance(job, FinishedJob)]


def run_command(command: str) -> str:
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


def convert_DB_to_Job(db_job: DBJob, queue: SQUEUE):

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
