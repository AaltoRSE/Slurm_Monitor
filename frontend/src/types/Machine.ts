export class Machine {
  cores: number;
  cores_used: number;
  gpus: number | undefined;
  gpus_used: number | undefined;
  gpu_type: string | undefined;
  memory: number;
  memory_used: number;
  status: string;
  constructor(
    cores: number,
    cores_used: number,
    memory: number,
    memory_used: number,
    status: string,
    gpus?: number,
    gpus_used?: number,
    gpu_type?: string
  ) {
    this.cores = cores;
    this.cores_used = cores_used;
    this.gpus = gpus;
    this.gpus_used = gpus_used;
    this.gpu_type = gpu_type;
    this.memory = memory;
    this.memory_used = memory_used;
    this.status = status;
  }
}
