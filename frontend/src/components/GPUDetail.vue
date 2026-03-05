<template>
  <div>
    <h2>GPU Memory Usage</h2>
    <DataGraph :data="gpuMemData" label="GPU Memory Usage" unit="MiB" />
    <h2>GPU Usage</h2>
    <DataGraph :data="gpuUsageData" label="GPU Usage" unit="%" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import DataGraph from './DataGraph.vue';
import type { GPUGraphData } from '../lib/types';

const props = defineProps<{ data?: GPUGraphData }>();

const gpuMemData = computed(() => props.data?.gpu_mem || []);
const gpuUsageData = computed(() => props.data?.gpu_usage || []);

</script>

<style scoped>
h2 {
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}
</style>
