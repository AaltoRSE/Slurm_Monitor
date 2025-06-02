import type { FinishedJob, Quota, RunningJob } from "@/lib/types";
import axios from "axios";
// Mock data for Slurm API
const MOCK_DELAY = 500; // Simulate server delay

// Mock current jobs data
const mockCurrentJobs: Array<RunningJob> = [
  {
    id: "42389",
    name: "deep_learning_model",
    status: "running",
    startTime: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
    endTime: new Date(Date.now() + 7200000).toISOString(), // 2 hours from now
    nodes: 1,
    resources: {
      cpus: 4,
      memory: 32,
      gpu: {
        type: "NVIDIA A100",
        amount: 1,
      },
    },
    command: "python train.py --epochs 100 --batch-size 32",
  },
  {
    id: "42390",
    name: "data_preprocessing",
    status: "queued",
    nodes: 1,
    startTime: new Date(Date.now() + 1800000).toISOString(), // 30 min from now (projected)
    endTime: new Date(Date.now() + 5400000).toISOString(), // 1.5 hours from now (projected)
    resources: {
      cpus: 12,
      memory: 24,
    },
    command: "python preprocess.py --input dataset.csv --output processed.pkl",
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
      memory: 48,
    },
    command: "./assembly --genome bacteria --threads 16 --memory 64G",
  },
  {
    id: "42392",
    name: "molecular_dynamics",
    status: "queued",
    nodes: 2,
    startTime: new Date(Date.now() + 3600000).toISOString(), // 1 hour from now (projected)
    endTime: new Date(Date.now() + 36000000).toISOString(), // 10 hours from now (projected)
    resources: {
      cpus: 8,
      memory: 32,
      gpu: {
        type: "NVIDIA A100",
        amount: 2,
      },
    },
    command: "./namd2 +idlepoll simulation.conf",
  },
];

// Mock job history data
const mockJobHistory: Array<FinishedJob> = [
  {
    id: "42385",
    name: "parameter_sweep",
    status: "completed",
    nodes: 1,
    startTime: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
    endTime: new Date(Date.now() - 79200000).toISOString(), // 22 hours ago
    resources: {
      cpus: 4,
      memory: 12,
    },
    command: "python train.py --epochs 100 --batch-size 32",
    efficiency: {
      cpu: 95,
      memory: 78,
    },
  },
  {
    id: "42386",
    name: "image_processing",
    status: "failed",
    nodes: 1,
    startTime: new Date(Date.now() - 43200000).toISOString(), // 12 hours ago
    endTime: new Date(Date.now() - 41400000).toISOString(), // 11.5 hours ago
    resources: {
      cpus: 8,
      memory: 32,
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
    startTime: new Date(Date.now() - 28800000).toISOString(), // 8 hours ago
    endTime: new Date(Date.now() - 18000000).toISOString(), // 5 hours agoresources:
    resources: {
      cpus: 8,
      memory: 32,
      gpu: {
        type: "NVIDIA A100",
        amount: 2,
      },
    },
    command: "python train.py --epochs 100 --batch-size 32",
    efficiency: {
      cpu: 92,
      memory: 85,
      gpu: 97,
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
      memory: 32,
      gpu: {
        type: "NVIDIA A100",
        amount: 2,
      },
    },
    command: "python train.py --epochs 100 --batch-size 32",
    efficiency: {
      cpu: 88,
      memory: 45,
      gpu: 33,
    },
  },
];

// Mock quota data
const mockQuotas: Array<Quota> = [
  {
    name: "Home Directory",
    path: "/home/user.name",
    used: 185000000,
    total: 500000000000,
    files: 123000,
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

// API mock functions
export const fetchCurrentJobs = async (): Promise<Array<RunningJob>> => {
  return new Promise((resolve) => {
    axios
      .get("/api/running_jobs")
      .then((response) => {
        resolve(response.data as Array<RunningJob>);
      })
      .catch((e) => {
        console.error(e);
      });
  });
};

export const fetchJobHistory = async (): Promise<Array<FinishedJob>> => {
  return new Promise((resolve) => {
    axios
      .get("/api/finished_jobs")
      .then((response) => {
        resolve(response.data as Array<FinishedJob>);
      })
      .catch((e) => {
        console.error(e);
      });
  });
};

export const fetchQuotas = async (): Promise<Array<Quota>> => {
  return new Promise((resolve) => {
    axios
      .get("/api/quotas")
      .then((response) => {
        resolve(response.data as Array<Quota>);
      })
      .catch((e) => {
        console.error(e);
      });
  });
};
