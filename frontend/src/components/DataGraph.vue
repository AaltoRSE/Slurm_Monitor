<template>    
    <div>
        <div v-if="chartData" class="graph">
            <div class="ml-3 mr-3 flex flex-row justify-content-between">
                <PrimeVueButton rounded size="small" v-tooltip="'Reset Zoom'" @click="resetZoom" icon="pi pi-refresh"></PrimeVueButton>
                <PrimeVueButton rounded size="small" v-tooltip="'Pop Out'" @click="popoutGraph" icon="pi pi-window-maximize"></PrimeVueButton>
            </div>
            <Chart ref="chartRef" class="graph" type="line" :width="450" :height="350" :data="chartData" :options="chartOptions" />
        </div>
        <div v-else class="graph">
            <ProgressSpinner />
        </div>        
    </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import Chart from 'primevue/chart';
import PrimeVueButton from 'primevue/button';
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
                zoom: {
                    wheel: {
                        enabled: true,
                    },
                    drag: {
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
    } as any
    if (props.maxx) {
        options.scales.y.max = props.maxx;        
    }
    if (props.type === 'memory') {

        options.scales.y.ticks = {
      callback: function(value : any) {
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

const chartRef = ref<any>(null);

function resetZoom() {
        const ch = chartRef.value?.chart;
        if (ch && typeof ch.resetZoom === 'function') {
                try { ch.resetZoom(); } catch (e) { /* ignore */ }
                return;
        }
        if (ch && typeof ch.reset === 'function') {
                try { ch.reset(); } catch (e) { /* ignore */ }
        }
}

function popoutGraph() {
        if (!chartData.value) return;
        const data = chartData.value;
        const label = props.label || 'Graph';
        const type = props.type || '';
        const maxx = props.maxx || null;

        const wAny: any = window.open('', '_blank', 'width=1000,height=700');
        if (!wAny) return;
        const doc = wAny.document;
        doc.title = label;
        // basic styles
        const style = doc.createElement('style');
        style.textContent = 'html,body{height:100%;margin:0}#chart{width:100%;height:100%}';
        doc.head.appendChild(style);
        // canvas
        const canvas = doc.createElement('canvas');
        canvas.id = 'chart';
        doc.body.appendChild(canvas);

        // expose data/config on new window
        wAny.__chartData = data;
        wAny.__chartLabel = label;
        wAny.__chartType = type;
        wAny.__chartMaxx = maxx;

        function loadScript(src: string) {
            return new Promise<void>((resolve, reject) => {
                const s = doc.createElement('script');
                s.src = src;
                s.onload = () => resolve();
                s.onerror = () => reject(new Error('failed to load ' + src));
                doc.head.appendChild(s);
            });
        }

        // load Chart.js and plugins sequentially, then init
        loadScript('https://cdn.jsdelivr.net/npm/chart.js').then(() =>
            loadScript('https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@2')
        ).then(() =>
            loadScript('https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@3')
        ).then(() => {
            try {
                const chartJs = (wAny as any).Chart;
                const ctx = (doc.getElementById('chart') as HTMLCanvasElement).getContext('2d');
                const options: any = {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' },
                        title: { display: true, text: label },
                        zoom: {
                            zoom: { wheel: { enabled: true }, drag: { enabled: true }, pinch: { enabled: true }, mode: 'xy' }
                        }
                    },
                    scales: {
                        x: {
                            type: 'time',
                            time: { tooltipFormat: 'yyyy-MM-dd HH:mm:ss', displayFormats: { minute: 'HH:mm', hour: 'HH:mm', day: 'MMM d' } },
                            position: 'bottom'
                        },
                        y: { type: 'linear' }
                    }
                };
                if (maxx) options.scales.y.max = maxx;
                if (type === 'memory') {
                    options.scales.y.ticks = {
                        callback: function(value: any) {
                            if (value === 0) return '0 B';
                            const units = ['B','KB','MB','GB','TB']; let i=0; let val = value;
                            while (val >= 1024 && i < units.length-1) { val /= 1024; i++; }
                            return val.toFixed(2) + ' ' + units[i];
                        }
                    };
                }
                const cfg = { type: 'line', data: data, options };
                new chartJs(ctx, cfg);
            } catch (e) {
                // ignore
            }
        }).catch(() => {
            // loading failed
        });
}
</script>

<style scoped>
.p-card {
    margin: 1rem;
}

.graph-toolbar {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}
.graph-btn {
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    padding: 0.35rem 0.6rem;
    border-radius: 4px;
    cursor: pointer;
}
.graph-btn:hover {
    background: #e5e7eb;
}
</style>
