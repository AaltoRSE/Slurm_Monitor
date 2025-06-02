<template>
  <ThemeSwitcher />
  <div class="card">
    <Chart
      type="bar"
      :data="chartData"
      :options="chartOptions"
      class="h-[30rem]"
    />
  </div>
</template>

<script lang="ts">
import Chart from "primevue/chart";
import { Partition } from "../types/Partition";
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    partitions: {
      type: Array<Partition>,
      required: true,
    },
  },
  components: { Chart },
  computed: {
    chartData(): Object {
      const documentStyle = getComputedStyle(document.documentElement);

      return {
        labels: this.partitions.map((part: Partition) => part.name),
        datasets: [
          {
            label: "draining",
            backgroundColor: documentStyle.getPropertyValue("--p-cyan-500"),
            borderColor: documentStyle.getPropertyValue("--p-cyan-500"),
          },
        ],
      };
    },
  },
  methods: {
    setChartData(): Object {
      const documentStyle = getComputedStyle(document.documentElement);

      return {
        labels: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
        ],
        datasets: [
          {
            label: "My First dataset",
            backgroundColor: documentStyle.getPropertyValue("--p-cyan-500"),
            borderColor: documentStyle.getPropertyValue("--p-cyan-500"),
            data: [65, 59, 80, 81, 56, 55, 40],
          },
          {
            label: "My Second dataset",
            backgroundColor: documentStyle.getPropertyValue("--p-gray-500"),
            borderColor: documentStyle.getPropertyValue("--p-gray-500"),
            data: [28, 48, 40, 19, 86, 27, 90],
          },
        ],
      };
    },
    setChartOptions(): Object {
      const documentStyle = getComputedStyle(document.documentElement);
      const textColor = documentStyle.getPropertyValue("--p-text-color");
      const textColorSecondary = documentStyle.getPropertyValue(
        "--p-text-muted-color"
      );
      const surfaceBorder = documentStyle.getPropertyValue(
        "--p-content-border-color"
      );

      return {
        indexAxis: "y",
        maintainAspectRatio: false,
        aspectRatio: 0.8,
        plugins: {
          legend: {
            labels: {
              color: textColor,
            },
          },
        },
        scales: {
          x: {
            stacked: true,
            ticks: {
              color: textColorSecondary,
              font: {
                weight: 500,
              },
            },
            grid: {
              display: false,
              drawBorder: false,
            },
          },
          y: {
            stacked: true,
            ticks: {
              color: textColorSecondary,
            },
            grid: {
              color: surfaceBorder,
              drawBorder: false,
            },
          },
        },
      };
    },
  },
});
</script>
