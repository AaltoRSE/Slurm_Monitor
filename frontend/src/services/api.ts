import type { FinishedJob, Quota, RunningJob, GPUGraphData } from "@/lib/types";
import axios, { type AxiosResponse } from "axios";
import { mockGraphData, mockCurrentJobs, mockJobHistory, mockQuotas, mock_server, MOCK_DELAY } from "@/mock/api_mock";

const base_url = import.meta.env.VITE_BASE_URL;
// Mock current jobs data



const card_memory: Map<string, number> = new Map([
  ["a100", 80 * 1024 * 1024 * 1024],
  ["h100", 80 * 1024 * 1024 * 1024],
  ["h200", 141 * 1024 * 1024 * 1024],
  ["b300", 288 * 1024 * 1024 * 1024],
  ["h200_2g.35gb", 35 * 1024 * 1024 * 1024],
]);

const v100_32 = [ "dgx3",  "dgx5", "dgx6", "dgx7", "gpu1", "gpu2", "gpu3", "gpu4", "gpu5", "gpu6", "gpu7", "gpu8", "gpu9",
            "gpu10", "gpu28", "gpu29", "gpu30", "gpu31", "gpu32", "gpu33", "gpu34", "gpu35", "gpu36", "gpu37"];
const v100_16 = ["dgx1", "dgx2",  "dgx8", "dgx9", "dgx10", "dgx15", "dgx16", "dgx17", "dgx18", "dgx19", "dgx20", "dgx21", 
           "dgx22", "dgx23", "dgx24", "dgx25", "dgx26", "dgx27"];        

export const getCardMemory = (gpu_type: string, node_name: string): number => {
  if (gpu_type === "v100") {
    if (v100_32.includes(node_name)) {
      return 32 * 1024 * 1024 * 1024; // Number in bytes
    } else if (v100_16.includes(node_name)) { 
      return 16 * 1024 * 1024 * 1024;
    }
  }
  if (!gpu_type)
  {
    return card_memory.get("h200_2g.35gb") // Default to 35GB for unknown types without specified type
  }
  return card_memory.get(gpu_type) || 0; // Default to 0 if type is unknown
}


const expandData = (job: RunningJob | FinishedJob): RunningJob | FinishedJob => 
  {
    if (job.resources.gpu) {  
      const card_gpu_mem = getCardMemory(job.resources.gpu.type || "", job.allocatedNodes || "");      
      if (card_gpu_mem > 0) {
        if(job.efficiency) {
          console.log(typeof job.efficiency?.gpu_individual_mem === "number")
          console.log(job.efficiency?.gpu_individual_mem)
          job.efficiency.gpu_mem_percentage = typeof job.efficiency?.gpu_individual_mem === "number" ? (job.efficiency.gpu_individual_mem / card_gpu_mem) * 100 : null;
          job.efficiency.gpu_total_mem_percentage = typeof job.efficiency?.gpu_total_mem === "number" ? (job.efficiency.gpu_total_mem / (card_gpu_mem * job.resources.gpu.amount)) * 100 : null;
        }        
      }
    }
    if (job.endTime) {
      job.endTime = new Date(job.endTime);
    }
    if (job.startTime) {
      job.startTime = new Date(job.startTime);
    }
    return job
  }
// API mock functions
export const fetchCurrentJobs = async (): Promise<Array<RunningJob>> => {
  return new Promise((resolve) => {
    if (mock_server) {
      setTimeout(() => {
        resolve(mockCurrentJobs.map(expandData));
      }, MOCK_DELAY);
    } else {
      axios
        .get(`${base_url}/api/running_jobs`)
        .then((response: AxiosResponse) => {
          resolve((response.data as Array<RunningJob>).map(expandData));
        })
        .catch((e: any) => {
          console.error(e);
        });
    }
  });
};

export const fetchJobHistory = async (): Promise<Array<FinishedJob>> => {
  return new Promise((resolve) => {
    if (mock_server) {
      setTimeout(() => {
        resolve(mockJobHistory.map(expandData)as Array<FinishedJob>);
      }, MOCK_DELAY);
    } else {
      axios
        .get(`${base_url}/api/finished_jobs`)
        .then((response: AxiosResponse) => {
          resolve((response.data as Array<FinishedJob>).map(expandData)as Array<FinishedJob>);
        })
        .catch((e: any) => {
          console.error(e);
        });
    }
  });
};

export const fetchQuotas = async (): Promise<Array<Quota>> => {
  return new Promise((resolve) => {
    if (mock_server) {
      setTimeout(() => {
        resolve(mockQuotas);
      }, MOCK_DELAY);
    } else {
      axios
        .get(`${base_url}/api/quotas`)
        .then((response: AxiosResponse) => {
          resolve(response.data as Array<Quota>);
        })
        .catch((e: any) => {
          console.error(e);
        });
    }
  });
};


export const fetchGPUDetails = async (job_id: number): Promise<GPUGraphData> => {
  return new Promise((resolve) => {
    if (mock_server) {
      setTimeout(() => {
        resolve(mockGraphData);
      }, MOCK_DELAY);
    } else {
      axios
        .get(`${base_url}/api/gpu_data/${job_id}`)
        .then((response: AxiosResponse) => {
          resolve(response.data as GPUGraphData);
        })
        .catch((e: any) => {
          console.error(e);
        });
    }
  });
};
