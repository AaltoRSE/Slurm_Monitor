import { defineStore } from "pinia";
import {
  fetchCurrentJobs,
  fetchJobHistory,
  fetchQuotas,
  fetchGPUDetails
} from "../services/api";
import type { FinishedJob, GPUGraphData, Quota, RunningJob } from "@/lib/types";



export const useJobStore = defineStore("job", {
  state: () => {
    return {
      currentJobs: [] as Array<RunningJob>,
      jobHistory: [] as Array<FinishedJob>,
      quotas: [] as Array<Quota>,
      loading: {
        currentJobs: false,
        jobHistory: false,
        quotas: false,
      },
      current_job: null as number | null,
      current_job_details: null as GPUGraphData | null,
      showJobDetails: false
    };
  },
  actions: {
    async fetchCurrentJobsData() {
      this.loading.currentJobs = true;
      try {
        this.currentJobs = await fetchCurrentJobs();
      } catch (error) {
        console.error("Error fetching current jobs:", error);
      } finally {
        this.loading.currentJobs = false;
      }
    },

    async fetchJobHistoryData() {
      this.loading.jobHistory = true;
      try {
        this.jobHistory = await fetchJobHistory();
      } catch (error) {
        console.error("Error fetching job history:", error);
      } finally {
        this.loading.jobHistory = false;
      }
    },

    async fetchQuotasData() {
      this.loading.quotas = true;
      try {
        this.quotas = await fetchQuotas();
        console.log(this.quotas);
      } catch (error) {
        console.error("Error fetching quotas:", error);
      } finally {
        this.loading.quotas = false;
      }
    },

    async fetchJobDetails(jobId: number) {
      console.log("Fetching job details for a job")
      this.current_job = jobId;
      this.current_job_details = null; // Clear previous details while loading new ones
      this.current_job_details = await fetchGPUDetails(jobId);
      console.log("New details are:")
      console.log(this.current_job_details)
    },
  },
});
