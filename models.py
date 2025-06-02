from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class GPUResources(BaseModel):
    type: Optional[str] = None
    amount: int


class Resources(BaseModel):
    cpus: int
    memory: int
    gpu: Optional[GPUResources] = None


class Job(BaseModel):
    id: str
    name: str
    nodes: Optional[int] = None
    status: str
    startTime: datetime
    endTime: Optional[datetime] = None
    resources: Resources


class RunningJob(Job):
    pass


class JobEfficiency(BaseModel):
    cpu: float
    memory: float
    gpu: Optional[float] = None


class FinishedJob(Job):
    efficiency: JobEfficiency


class Quota(BaseModel):
    name: str
    path: str
    used: int
    total: int
    files: int
    used_files: int
