<template>
  <div class="flex flex-row">
    <div class="flex flex-column">    
    <DataGraph class="graph" :data="gpuMemData" label="GPU Memory Usage" type="memory" />
    </div>
    <div class="flex flex-column">    
    <DataGraph class="graph" :data="gpuUsageData" :maxx="100" label="GPU Usage"  />
    </div>
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
<style>
.graph {
  width: 450px;
  height: 350px;
}
</style>
