<template>
  <div>
    <h2>GPU Memory Usage</h2>
    <DataGraph :data="gpuMemData" label="GPU Memory Usage" unit="MiB" />
    <h2>GPU Usage</h2>
    <DataGraph :data="gpuUsageData" :maxx="100" label="GPU Usage" unit="%" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import DataGraph from './DataGraph.vue';
import { useJobStore } from '@/stores/jobStore';
const jobStore = useJobStore()
const gpuMemData = computed(() => jobStore.current_job_details?.gpu_mem || []);
const gpuUsageData = computed(() => jobStore.current_job_details?.gpu_usage || []);

</script>

<style scoped>
h2 {
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}
</style>
