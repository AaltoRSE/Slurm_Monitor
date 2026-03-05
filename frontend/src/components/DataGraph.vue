<template>
  <Card>
    <div v-if="chartData">
      <Chart type="line" :data="chartData" :options="chartOptions" />
    </div>
    <div v-else>
      <ProgressSpinner />
    </div>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import Chart from 'primevue/chart';
import Card from 'primevue/card';
import ProgressSpinner from 'primevue/progressspinner';
import type { VectorValue } from '../lib/types';

const props = defineProps<{ data: VectorValue[], label : string, unit : string}>();

const chartData = computed(() => {
  if (!props.data || props.data.length === 0) return null;    
  return {    
    datasets: props.data.map((vec, idx) => ({      
      label: vec.metric.gpu ? `GPU ${vec.metric.gpu}` : `GPU ${idx + 1}`,
      data: vec.values.map(v => ({ x: new Date(v.timestamp * 1000), y: v.value }))
    }))
  };
});

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: props.label || 'Data Graph',
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Time',
      },
      type: 'time'
    },
    y: {
      title: {
        display: true,
        text: props.unit || 'Value',
      },
    },
  },
};
</script>

<style scoped>
.p-card {
  margin: 1rem;
}
</style>
