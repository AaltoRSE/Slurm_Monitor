from pydantic import BaseModel, RootModel
from typing import Any, Optional, Union, List, Dict, Tuple, Type
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
    startTime: Optional[datetime] = None
    endTime: Optional[Union[datetime, str]] = None
    resources: Resources
    command: str


class RunningJob(Job):
    allocatedNodes: Optional[str] = None


class JobEfficiency(BaseModel):
    cpu: Optional[float] = None
    memory: Optional[float] = None
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







class TritonMetrics(BaseModel):
        account: Optional[str] = None
        instance: Optional[str] = None
        job: Optional[str] = None
        slurmjobid:  Optional[int] = None
        user: Optional[str] = None
        __name__: Optional[str] = None

class TimeStampValue(BaseModel):    
    timestamp: float
    value: Any

class SingleValue(TimeStampValue):
    metric: TritonMetrics


class VectorValue(BaseModel):    
    metric: TritonMetrics
    values: List[TimeStampValue]

class JobDataPoint(BaseModel):
    
class PrometheusSingleValue(BaseModel):    
    metric: TritonMetrics
    value: Tuple[float, str]

class PrometheusVectorValue(BaseModel):    
    metric: TritonMetrics
    values: List[Tuple[float, str]]
    def to_vector_value(self, value_type : Type | None = None) -> VectorValue:
        return VectorValue(
            metric=self.metric,
            values=[TimeStampValue(timestamp=ts, value=val if value_type is None else value_type(val)) for ts, val in self.values]
        )


class VectorResult(BaseModel):    
    value: List[SingleValue]

class PrometheusVectorResult(RootModel[List[PrometheusSingleValue]]):          
    root: list[PrometheusSingleValue]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def to_vector_result(self) -> VectorResult:
        return VectorResult(            
            value=[SingleValue(timestamp=res.value[0], value=res.value[1], metric=res.metric) for res in self.root]
        )
    
class MatrixResult(BaseModel):
    values: List[VectorValue]
    
PrometheusValueList = List[PrometheusSingleValue]

class PrometheusMatrixResult(RootModel[List[PrometheusVectorValue]]):
    root: list[PrometheusVectorValue]
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    def to_matrix_result(self, value_type : Type | None = None) -> MatrixResult:        
        return MatrixResult(            
            values=[vector.to_vector_value(value_type) for vector in self.root]
        )
    
