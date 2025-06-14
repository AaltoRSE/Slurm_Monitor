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
          <span v-if="!isJobFinished(job.status)" class="text-xs text-500"
            >(Projected)</span
          >
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
          {{ job.resources.memory }} GB
        </div>
        <div v-if="job.resources.gpu">
          <i class="pi pi-sliders-h mr-2"></i>
          <span class="font-semibold">GPU:</span>
          {{ job.resources.gpu.amount }}x
          {{ job.resources.gpu.type }}
        </div>
      </div>

      <div v-if="'efficiency' in job">
        <div class="col-12 mt-3">
          <div class="text-lg font-medium mb-2">Resource Efficiency</div>
          <div class="mb-2">
            <span class="font-semibold mr-2">CPU:</span>
            <EfficiencyBar :value="(job as FinishedJob).efficiency.cpu" />
          </div>
          <div class="mb-2">
            <span class="font-semibold mr-2">Memory:</span>
            <EfficiencyBar :value="(job as FinishedJob).efficiency.memory" />
          </div>
          <div
            v-if="(job as FinishedJob).resources.gpu !== undefined && (job as FinishedJob).efficiency.gpu"
            class="mb-2"
          >
            <span class="font-semibold mr-2">GPU:</span>
            <EfficiencyBar :value="(job as FinishedJob).efficiency.gpu!" />
          </div>
        </div>
      </div>
    </div>
    <div class="p-2 border-top-1 border-300">
      <div
        class="command-preview overflow-hidden text-overflow-ellipsis white-space-nowrap"
      >
        <i class="pi pi-code mr-2"></i>
        {{ job.command }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Tag from "primevue/tag";
import type { FinishedJob, RunningJob } from "@/lib/types";
import { formatDateTime, getStatusSeverity, isJobFinished } from "@/lib/utils";
import EfficiencyBar from "./EfficiencyBar.vue";

// Props
defineProps<{
  job: RunningJob | FinishedJob;
}>();
</script>

<style scoped>
.job-card {
  transition: all 0.2s;
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
