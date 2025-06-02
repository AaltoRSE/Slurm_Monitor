import { defineStore } from 'pinia'
import { fetchCurrentJobs, fetchJobHistory, fetchQuotas } from '../services/api'
import type { FinishedJob, Quota, RunningJob } from '@/lib/types'

export const useJobStore = defineStore('job', {
  state: () => {
    return {
      currentJobs: [] as Array<RunningJob>,
      jobHistory: [] as Array<FinishedJob>,
      quotas: [] as Array<Quota>,
      loading: {
        currentJobs: false,
        jobHistory: false,
        quotas: false
      }
    }
  },
  actions: {
    async fetchCurrentJobsData() {
      this.loading.currentJobs = true
      try {
        this.currentJobs = await fetchCurrentJobs()
      } catch (error) {
        console.error('Error fetching current jobs:', error)
      } finally {
        this.loading.currentJobs = false
      }
    },

    async fetchJobHistoryData() {
      this.loading.jobHistory = true
      try {
        this.jobHistory = await fetchJobHistory()
      } catch (error) {
        console.error('Error fetching job history:', error)
      } finally {
        this.loading.jobHistory = false
      }
    },

    async fetchQuotasData() {
      this.loading.quotas = true
      try {
        this.quotas = await fetchQuotas()
        console.log(this.quotas)
      } catch (error) {
        console.error('Error fetching quotas:', error)
      } finally {
        this.loading.quotas = false
      }
    }
  }
})
