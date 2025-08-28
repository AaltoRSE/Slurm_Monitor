type Job = {
  id: string;
  name: string;
  status: string;
  startTime?: string;
  endTime: string;
  nodes: number;
  resources: {
    cpus: number;
    memory: number;
    gpu?: {
      type?: string;
      amount: number;
    };
  };
  command: string;
};
export type RunningJob = Job & {
  allocatedNodes?: string;
};

export type FinishedJob = RunningJob & {
  efficiency: {
    cpu: number;
    memory: number;
    gpu?: number;
  };
};

export type Quota = {
  name: string;
  path: string;
  used: number;
  total: number;
  files: number;
  used_files: number;
};
