from pydantic import BaseModel
from typing import Optional, Union
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
    endTime: Optional[Union[datetime, str]] = None
    resources: Resources
    command: str


class RunningJob(Job):
    allocatedNodes: Optional[str] = None


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
