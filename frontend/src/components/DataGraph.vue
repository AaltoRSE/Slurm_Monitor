<template>
  <div>
    <div v-if="chartData">
      <Chart type="line" :data="chartData" :options="chartOptions" />
    </div>
    <div v-else>
      <ProgressSpinner />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, VueElement } from 'vue';
import Chart from 'primevue/chart';
import ProgressSpinner from 'primevue/progressspinner';
import type { VectorValue } from '../lib/types';
import "chartjs-adapter-date-fns"

const props = defineProps<{ data: VectorValue[], label : string, unit : string, maxx? : Number}>();

const chartData = computed(() => {
  if (!props.data || props.data.length === 0) return null;    
  return {    
    datasets: props.data.map((vec, idx) => ({      
      label: vec.metric.gpu ? `GPU ${vec.metric.gpu}` : `GPU ${idx + 1}`,
      data: vec.values.map(v => ({ x: v.timestamp, y: v.value }))
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
          type: "time",
          time: {
            tooltipFormat: "yyyy-MM-dd HH:mm:ss",
            displayFormats: {
              minute: "HH:mm",
              hour: "HH:mm",
              day: "MMM d"
            }
          },
          position: "bottom"
        },
        y: {
          type: "linear"
        }
      }
    
};
</script>

<style scoped>
.p-card {
  margin: 1rem;
}
</style>
