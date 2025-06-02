import os
import subprocess
import slurm2sql
from typing import List

import sqlite3
import threading
from datetime import datetime, timedelta
from models import Job, RunningJob, FinishedJob, Resources, GPUResources, JobEfficiency
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
        if db is None or datetime.now() - db_time > timedelta(seconds=15):
            db = sqlite3.connect(":memory:")
            slurm2sql.slurm2sql(db, ["-S", "now-2weeks", "-u", "bjorkmz1"], update=True)
            db_time = datetime.now()
            queue = SQUEUE()
            jobs = db.cursor().execute(
                "SELECT * FROM eff WHERE State IN ('RUNNING', 'PENDING')"
            )
            headers = extractHeader(current_jobs.description)
            current_jobs = [
                convert_DB_to_Job(DBJob(result, headers, queue), True)
                for result in current_jobs
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
        print(headers)
        print(db_result)
        self.headers = headers
        self.result = db_result

    def get(self, field, type=str):
        try:
            value = self.result[self.headers[field]]
            return type(value) if not value is None else None
        except:
            return None


def convert_DB_to_Job(db_job: DBJob, running: bool, queue: SQUEUE):

    id = db_job.get("JobID")
    print(id)
    name = db_job.get("JobName")
    print(id)
    commands = db_job.get("SubmitLines")
    if commands is None:
        commands = ["Unknown"]
    else:
        commands = db_job.get("SubmitLines").split("\n")
    print(commands)
    status = db_job.get("State")
    print(status)
    time = db_job.get("TimeLimit")
    try:
        t = datetime.strptime(time, "%d-%H:%M:%S")
    except:
        t = datetime.strptime(time, "%H:%M:%S")
    # ...and use datetime's hour, min and sec properties to build a timedelta
    delta = timedelta(days=t.day, hours=t.hour, minutes=t.minute, seconds=t.second)

    print(time)
    startTime = db_job.get("Start")
    if startTime is None:
        startTime = datetime.fromisoformat(queue.get_start_time(id))
    else:
        startTime = datetime.fromtimestamp(startTime)
    print(startTime)
    endTime = db_job.get("End")
    if endTime is None:
        if not startTime is None:
            endTime = startTime + timedelta(time)
    print(endTime)
    cpus = db_job.get("NCPUS", int)
    print(cpus)
    memory = db_job.get("MemReq", int)
    print(memory)
    gpus = db_job.get("NGpus", int)
    print(gpus)
    nodes = db_job.get("NNodes", int)
    print(nodes)
    nodeList = db_job.get("NodeList")
    print(nodeList)
    gpu_type = db_job.get("GPUType")
    print(gpu_type)
    gpu_eff = db_job.get("GPUeff", float)
    cpu_eff = db_job.get("CPUeff", float)
    mem_eff = db_job.get("MemEff", float)
    gpu_res = None if gpus is None else GPUResources(amount=gpus, type=gpu_type)
    res = Resources(cpus=cpus, memory=memory, gpus=gpu_res)
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
        efficieny = JobEfficiency(cpu=cpu_eff, memory=mem_eff, gpu=gpu_eff)
        return FinishedJob(
            id=id,
            status=status,
            name=name,
            nodes=nodes,
            startTime=startTime,
            endTime=endTime,
            resources=res,
            efficieny=efficieny,
            command=commands[0],
        )
