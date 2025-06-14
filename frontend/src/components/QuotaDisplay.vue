<template>
  <div class="quota-container">
    <div v-if="loading" class="flex justify-content-center">
      <ProgressSpinner
        style="width: 50px; height: 50px"
        strokeWidth="8"
        fill="var(--surface-ground)"
        animationDuration=".5s"
      />
    </div>

    <div v-else class="grid">
      <div
        v-for="quota in quotas"
        :key="quota.name"
        class="col-12 md:col-6 lg:col-4 mb-3"
      >
        <div class="quota-card p-3">
          <div class="quota-header mb-2">
            <h3 class="text-lg font-semibold">{{ quota.name }}</h3>
            <span class="text-sm text-gray-500" v-if="quota.path">
              {{ quota.path }}
            </span>
          </div>
          Data:
          <div class="quota-meter mb-2">
            <ProgressBar
              :value="getPercentage(quota)"
              :class="getProgressBarClass(getPercentage(quota))"
            />
          </div>

          <div class="quota-details flex justify-content-between">
            <span class="text-sm">
              {{ formatValue(quota.used) }} / {{ formatValue(quota.total) }}
            </span>
            <span
              class="text-sm font-bold"
              :class="getTextColorClass(getPercentage(quota))"
            >
              {{ getPercentage(quota) }}%
            </span>
          </div>
          <div v-if="quota.files > 0">
            Files:
            <div class="quota-meter mb-2">
              <ProgressBar
                :value="getFilePercentage(quota)"
                :class="getProgressBarClass(getFilePercentage(quota))"
              />
            </div>
            <div class="quota-details flex justify-content-between">
              <span class="text-sm">
                {{ formatValue(quota.used_files).slice(0, -1) }} /
                {{ formatValue(quota.files).slice(0, -1) }}
              </span>
              <span
                class="text-sm font-bold"
                :class="getTextColorClass(getFilePercentage(quota))"
              >
                {{ getFilePercentage(quota) }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import ProgressBar from "primevue/progressbar";
import ProgressSpinner from "primevue/progressspinner";
import { filesize } from "filesize";
import type { Quota } from "@/lib/types";

defineProps({
  quotas: {
    type: Array<Quota>,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const getPercentage = (quota: Quota) => {
  return Math.round((quota.used / quota.total) * 100);
};

const getFilePercentage = (quota: Quota) => {
  return Math.round((quota.used_files / quota.files) * 100);
};

const formatValue = (value: number) => {
  return filesize(value);
};
const getProgressBarClass = (percentage: number) => {
  if (percentage > 90) return "p-progressbar-danger";
  if (percentage > 75) return "p-progressbar-warning";
  return "p-progressbar-success";
};

const getTextColorClass = (percentage: number) => {
  if (percentage > 90) return "text-red-500";
  if (percentage > 75) return "text-orange-500";
  return "text-green-500";
};
</script>

<style scoped>
.quota-card {
  background-color: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.p-progressbar {
  height: 10px;
}
</style>
<style>
.p-progressbar-success > .p-progressbar-value {
  background: #22c55e;
}

.p-progressbar-warning > .p-progressbar-value {
  background: #f59e0b;
}

.p-progressbar-danger > .p-progressbar-value {
  background: #ef4444;
}
</style>
