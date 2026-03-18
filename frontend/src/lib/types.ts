type Job = {
  id: string;
  name: string;
  status: string;
  startTime?: string | Date;
  endTime: string | Date;
  nodes: number;
  resources: {
    cpus: number;
    memory: number;
    gpu?: {
      type?: string;
      amount: number;
    } | null;
  };
  command: string;  
};
export type RunningJob = Job & {
  allocatedNodes?: string;
  efficiency?: EfficiencyData;
};

export type EfficiencyData = {
    cpu?: number;
    memory?: number;
    gpu?: number | null;
    gpu_total_mem?: number | null;
    gpu_individual_mem?: number | null;
    gpu_mem_percentage?: number | null;
    gpu_total_mem_percentage?: number | null;
}

export type TritonMetrics = {
        account?: string;
        instance?: string;
        job?: string;
        slurmjobid?: number;
        user?: string;
        gpu?: string;        
}

export type VectorValue = {
  metric : TritonMetrics;
  values: Array<{ timestamp: number; value: any }>;
};

export type GPUGraphData = {
  gpu_usage: Array<VectorValue>;
  gpu_mem: Array<VectorValue>;
};

export type FinishedJob = RunningJob & {
  efficiency: EfficiencyData;
};

export type Quota = {
  name: string;
  path: string;
  used: number;
  total: number;
  files: number;
  used_files: number;
};
