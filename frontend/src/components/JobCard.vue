<template>
  <div>
    <div class="flex align-items-center justify-content-between">
      <div>
        <h3 class="text-xl font-bold m-0">{{ job.name }}</h3>
        <div class="text-500">ID: {{ job.id }}</div>
      </div>
      <Tag :value="job.status" :severity="getStatusSeverity(job.status)" />
    </div>
    <div class="grid">
      <div class="col-6">
        <div class="mb-2">
          <i class="pi pi-calendar mr-2"></i>
          <span class="font-semibold">Start:</span>
          {{ formatDateTime(job.startTime) }}
          <span v-if="!isJobFinished(job.status)" class="text-xs text-500">(Projected)</span>
        </div>
        <div>
          <i class="pi pi-calendar-times mr-2"></i>
          <span class="font-semibold">End:</span>
          {{ formatDateTime(job.endTime) }}
          <span class="text-xs text-500">{{
            isJobFinished(job.status) ? "" : "(Projected)"
            }}</span>
        </div>
      </div>

      <div class="col-6">
        <div class="mb-2">
          <i class="pi pi-server mr-2"></i>
          <span class="font-semibold">CPUs:</span> {{ job.resources.cpus }}
        </div>
        <div class="mb-2">
          <i class="pi pi-database mr-2"></i>
          <span class="font-semibold">Memory:</span>
          {{ filesize(job.resources.memory) }}
        </div>
        <div v-if="job.resources.gpu">
          <div>
          <i class="pi pi-sliders-h mr-2"></i>
          <span class="font-semibold">GPU:</span>
          {{ job.resources.gpu.amount }}x
          {{ job.resources.gpu.type }}
        </div>
          <div>
          <i class="pi pi-sliders-h mr-2"></i>
          <span class="font-semibold">GPU Mem (per card):</span>
          {{ filesize(job.efficiency!.gpu_individual_mem!) }}          
        </div>
          <div>
          <i class="pi pi-sliders-h mr-2"></i>
          <span class="font-semibold">Total GPU Mem:</span>
          {{ filesize(job.efficiency!.gpu_total_mem!) }}          
          
        </div>
        </div>

      </div>

      <div v-if="'efficiency' in job" class="flex w-full">
        <div class="flex col-12 flex-column mt-3">
          <div class="flex text-lg font-medium mb-2">Resource Efficiency</div>
          <div class="flex flex-row w-full gap-4">
            <div v-if="'cpu' in job.efficiency!" class="flex-column w-5">
              <div v-if="'cpu' in job.efficiency!" class="mb-2">
                <span class="font-semibold mr-2">CPU:</span>
                <EfficiencyBar :value="(job as FinishedJob).efficiency.cpu!" />
              </div>
              <div v-if="'memory' in job.efficiency!" class="mb-2">
                <span class="font-semibold mr-2">Memory:</span>
                <EfficiencyBar :value="(job as FinishedJob).efficiency.memory!" />
              </div>
            </div>
            <div v-if="(job as FinishedJob).resources.gpu" class="flex flex-column w-5">
              <div v-if="(job as FinishedJob).resources.gpu && (job as FinishedJob).efficiency.gpu !== null"
                class="mb-2">
                <span class="font-semibold mr-2">GPU:
                  <Button @click="showGPUDetails(job.id)" icon="pi pi-info-circle" outlined rounded size="small"
                    aria-label="Job Details"></Button>
                </span>
                <div class="flex flex-row align-items-center gap-2">
                  <EfficiencyBar :value="(job as FinishedJob).efficiency.gpu!" />
                  
                </div>
              </div>
              <div v-if="(job as FinishedJob).resources.gpu && (job as FinishedJob).efficiency.gpu_mem_percentage !== null"
                class="mb-2">
                <span class="font-semibold mr-2">GPU Mem per card (max):</span>
                <div class="flex flex-row align-items-center gap-2">
                  <EfficiencyBar :value="(job as FinishedJob).efficiency.gpu_mem_percentage!" />                  
                </div>
              </div>
                <div v-if="(job as FinishedJob).resources.gpu && (job as FinishedJob).efficiency.gpu_total_mem_percentage !== null"
                class="mb-2">
                <span class="font-semibold mr-2">Total GPU Mem:</span>
                <div class="flex flex-row align-items-center gap-2">
                  <EfficiencyBar :value="(job as FinishedJob).efficiency.gpu_total_mem_percentage!" />
                  
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="p-2 border-top-1 border-300">
      <div class="command-preview overflow-hidden text-overflow-ellipsis white-space-nowrap">
        <i class="pi pi-code mr-2"> Command:</i>
        <span class="flex white-space-normal command-info">
          {{ job.command }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Tag from "primevue/tag";
import Button from "primevue/button";
import { filesize } from "filesize";

import { useJobStore } from "@/stores/jobStore";
import type { FinishedJob, RunningJob } from "@/lib/types";
import { formatDateTime, getStatusSeverity, isJobFinished } from "@/lib/utils";
import EfficiencyBar from "./EfficiencyBar.vue";
// Props
defineProps<{
  job: RunningJob | FinishedJob;
}>();

const jobStore = useJobStore();
const showGPUDetails = async (jobId: string) => {
  console.log(`Loading details for ${jobId}`)
  try {
    await jobStore.fetchJobDetails(Number(jobId))
      .then(() => {
        console.log("Done fetching")
      })
      .finally(() => {
        console.log("Realy done fetching")
      })
    jobStore.showJobDetails = true
  }
  catch {
    console.log("Some error occured")
  }
};
</script>

<style scoped>
.job-card {
  transition: all 0.2s;
}

.command-info {
  max-width: 600px;
}

.job-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.command-preview {
  max-width: 100%;
  cursor: help;
}

.h-1rem {
  height: 1rem;
}
</style>
