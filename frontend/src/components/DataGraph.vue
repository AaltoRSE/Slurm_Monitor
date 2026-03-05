<template>    
    <div>
        <div v-if="chartData" class="graph">
            <Chart class="graph" type="line" :width="450" :height="350" :data="chartData" :options="chartOptions" />
        </div>
        <div v-else class="graph">
            <ProgressSpinner />
        </div>        
    </div>
</template>

<script setup lang="ts">
import { ref, computed, VueElement } from 'vue';
import Chart from 'primevue/chart';
import Card from 'primevue/card';
import ProgressSpinner from 'primevue/progressspinner';
import type { VectorValue } from '../lib/types';

const props = defineProps<{ data: VectorValue[], label: string, type?: string, maxx?: Number }>();

const chartData = computed(() => {
    if (!props.data || props.data.length === 0) return null;
    return {
        datasets: props.data.map((vec, idx) => ({
            label: vec.metric.gpu ? `GPU ${vec.metric.gpu}` : `GPU ${idx + 1}`,
            data: vec.values.map(v => ({ x: v.timestamp*1000, y: v.value }))
        }))
    };
});

const chartOptions = computed(() => {
    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: props.label || 'Data Graph',
            },
            zoom: {
                pan: {
                    enabled: true,
                    mode: 'xy',
                },
                zoom: {
                    wheel: {
                        enabled: true,
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'xy',
                }
            }
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
    }
    if (props.maxx) {
        options.scales.y.max = props.maxx;        
    }
    if (props.type === 'memory') {

        options.scales.y.ticks = {
      callback: function(value) {
        if (value === 0) return '0 B';
        const units = ['B', 'KB', 'MB', 'GB', 'TB'];
        let i = 0;
        let val = value;
        while (val >= 1024 && i < units.length - 1) {
          val /= 1024;
          i++;
        }
        return val.toFixed(2) + ' ' + units[i];
      }
    }
    }
    return options;
})
</script>

<style scoped>
.p-card {
    margin: 1rem;
}
</style>
