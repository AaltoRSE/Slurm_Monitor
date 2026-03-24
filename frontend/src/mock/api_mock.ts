import type { FinishedJob, GPUGraphData, Quota, RunningJob } from "../lib/types";
export const mock_server = true;
// Mock data for Slurm API
export const MOCK_DELAY = 500; // Simulate server delay
export const mockGraphData: GPUGraphData = {
  gpu_usage: [
    {
    metric: {
      account: "account",
      instance: "instance",
      job: "job",
      slurmjobid: 12345,
      user: "user",
      gpu: "0",
    },
    values: [
      { timestamp: 1700000015, value: 70.5 },
      { timestamp: 1700000030, value: 30.7 },
      { timestamp: 1700000045, value: 0.6 },
      { timestamp: 1700000060, value: 70.5 },
      { timestamp: 1700000090, value: 30.7 },
      { timestamp: 1700000120, value: 0.6 },
    ],
  },
  {
    metric: {
      account: "account",
      instance: "instance",
      job: "job",
      slurmjobid: 12345,
      user: "user",
      gpu: "1",
    },
    values: [
      { timestamp: 1700000015, value: 60.5 },
      { timestamp: 1700000030, value: 40.7 },
      { timestamp: 1700000045, value: 7.6 },
      { timestamp: 1700000060, value: 80.5 },
      { timestamp: 1700000090, value: 20.7 },
      { timestamp: 1700000120, value: 10.6 },
    ],
  },
  {
    metric: {
      account: "account",
      instance: "instance",
      job: "job",
      slurmjobid: 12345,
      user: "user",
      gpu: "1",
    },
    values: [
      { timestamp: 1700000135, value: 60.5 },
      { timestamp: 1700000150, value: 40.7 },
      { timestamp: 1700000165, value: 7.6 },
      { timestamp: 1700000180, value: 80.5 },
      { timestamp: 1700000195, value: 20.7 },
      { timestamp: 1700000210, value: 10.6 },
    ],
  }
  ],
  gpu_mem: [
{
    metric: {
      account: "account",
      instance: "instance",
      job: "job",
      slurmjobid: 12345,
      user: "user",
      gpu: "0",
    },
    values: [
      { timestamp: 1700100015, value: 1700000015 },
      { timestamp: 1700100030, value: 17000015 },
      { timestamp: 1700100045, value: 170000015 },
      { timestamp: 1700100060, value: 8200000015 },
      { timestamp: 1700100090, value: 100000015 },
      { timestamp: 1700100120, value: 700000015 },
    ],
  },
  {
    metric: {
      account: "account",
      instance: "instance",
      job: "job",
      slurmjobid: 12345,
      user: "user",
      gpu: "1",
    },
    values: [
      { timestamp: 1700010015, value: 2700000015 },
      { timestamp: 1700000030, value: 7000015 },
      { timestamp: 1700000045, value: 370000015 },
      { timestamp: 1700000060, value: 5200000015 },
      { timestamp: 1700000090, value: 400000015 },
      { timestamp: 1700000120, value: 600000015 },
    ],
  }
  ]
}

export  const mockCurrentJobs: Array<RunningJob> = [
  {
    id: "42392",
    name: "deep_learning_model",
    status: "running",
    startTime: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
    endTime: new Date(Date.now() + 7200000).toISOString(), // 2 hours from now
    nodes: 1,
    allocatedNodes: "dgx3",
    resources: {
      cpus: 4,
      memory: 209715200,
      gpu: {
        type: "v100",
        amount: 1,
      },
    },
    command: "python train.py --epochs 100 --batch-size 32",
    efficiency: {
      gpu: 5,
      gpu_total_mem: 9476736,
      gpu_individual_mem : 9476736,
    },
    gpu_recent_eff: 5,
    elapsed: 1600,
  },
  {
    id: "42490",
    name: "data_preprocessing",
    status: "queued",
    nodes: 1,
    startTime: new Date(Date.now() + 1800000).toISOString(), // 30 min from now (projected)
    endTime: new Date(Date.now() + 5400000).toISOString(), // 1.5 hours from now (projected)
    resources: {
      cpus: 12,
      memory: 25769803776,
    },
    command: "python preprocess.py --input dataset.csv --output processed.pkl",
    gpu_recent_eff: null,
    elapsed: 1500,
  },
  {
    id: "42391",
    name: "genome_assembly",
    status: "running",
    nodes: 1,
    startTime: new Date(Date.now() - 7200000).toISOString(), // 2 hours ago
    endTime: new Date(Date.now() + 14400000).toISOString(), // 4 hours from now
    resources: {
      cpus: 16,
      memory: 68719476736,
    },
    command: "./assembly --genome bacteria --threads 16 --memory 64G",
    gpu_recent_eff: null,
    elapsed: 2500,
  },
  {
    id: "42393",
    name: "molecular_dynamics",
    status: "queued",
    nodes: 2,
    startTime: new Date(Date.now() + 3600000).toISOString(), // 1 hour from now (projected)
    endTime: new Date(Date.now() + 36000000).toISOString(), // 10 hours from now (projected)
    resources: {
      cpus: 8,
      memory: 34359738368,
      gpu: {
        type: "a100",
        amount: 2,
      },
    },
    efficiency: {
      gpu: 5,
      gpu_total_mem: 0,
      gpu_individual_mem : 9476736,
    },
    command: "./namd2 +idlepoll simulation.conf",
    gpu_recent_eff: 5,
    elapsed: 20,
  },
];

// Mock job history data
export const mockJobHistory: Array<FinishedJob> = [
  {
    id: "42385",
    name: "parameter_sweep",
    status: "completed",
    nodes: 1,
    startTime: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
    endTime: new Date(Date.now() - 83400000).toISOString(), // 22 hours ago
    resources: {
      cpus: 4,
      memory: 12884901888,
      gpu: null
    },
    command: "python train.py --epochs 100 --batch-size 32",
    efficiency: {
      cpu: 95,
      memory: 78,
      gpu: null,
      gpu_total_mem: null,
      gpu_individual_mem : null,
    },
  },
  {
    id: "42386",
    name: "image_processing",
    status: "failed",
    nodes: 1,
    startTime: undefined, // 12 hours ago
    endTime: new Date(Date.now() - 41400000).toISOString(), // 11.5 hours ago
    resources: {
      cpus: 8,
      memory: 34359738368,
    },
    command: "python train.py --epochs 100 --batch-size 32",
    efficiency: {
      cpu: 45,
      memory: 30,
    },
  },
  {
    id: "42387",
    name: "neural_network_training",
    status: "completed",
    nodes: 2,
    startTime: new Date(Date.now() - 288000000).toISOString(), // 8 hours ago
    endTime: new Date(Date.now() - 180000000).toISOString(), // 5 hours agoresources:
    resources: {
      cpus: 8,
      memory: 34359738368,
      gpu: {
        type: "h200",
        amount: 2,
      },
    },
    command: "/usr/bin/sbatch -D /scratch/work/user/.ondemand/batch_connect/sys/bc_desktop/triton/output/0000-0000-000-000-000-00000 -J sys/dashboard/sys/bc_desktop/triton -o /scratch/work/user/.ondemand/batch_connect/sys/bc_desktop/triton/output/00000-000-00000-0000000000000-000/output.log -p interactive --export PATH,GNOME_SHELL_SESSION_MODE,GNOME_SESSION_MODE -N 1 -n 2 -t 2:00:00 --mem 8G --gpus 0 -A account --parsable",
    efficiency: {
      cpu: 92,
      memory: 85,
      gpu: 5,
      gpu_total_mem: 9476736,
      gpu_individual_mem : 9476736,
    },
  },
  {
    id: "42388",
    name: "statistical_analysis",
    status: "completed",

    nodes: 1,
    startTime: new Date(Date.now() - 10800000).toISOString(), // 3 hours ago
    endTime: new Date(Date.now() - 7200000).toISOString(), // 2 hours ago
    resources: {
      cpus: 8,
      memory: 34359738368,
      gpu: {
        type: "h100",
        amount: 1,
      },
    },
    command: "python train.py --epochs 100 --batch-size 32",
    efficiency: {
      cpu: 88,
      memory: 10,
      gpu: 33,
      gpu_total_mem: 68719476736,
      gpu_individual_mem : 68719476736,
    },

  },
];

// Mock quota data
export const mockQuotas: Array<Quota> = [
  {
    name: "Home Directory",
    path: "/home/user.name",
    used: 185000000,
    total: 500000000000,
    files: 0,
    used_files: 110000,
  },
  {
    name: "Project Storage",
    path: "/project/ml-research",
    used: 2700000,
    total: 50000000,
    files: 503000,
    used_files: 80000,
  },
  {
    name: "Scratch Space",
    path: "/scratch/user.name",
    used: 190000000,
    total: 200000000,
    files: 123000,
    used_files: 110000,
  },
];