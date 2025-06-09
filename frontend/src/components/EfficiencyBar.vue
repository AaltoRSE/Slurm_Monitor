<template>
  <div
    class="efficiency-bar"
    :style="{
      backgroundColor: '#FFFFFF',
    }"
  >
    <div
      class="efficiency-bar-fill"
      :style="{
        width: `${value}%`,
      }"
    ></div>
    <span
      class="efficiency-bar-label"
      :style="{
        color: getColorForValue(value),
      }"
      >{{ formatNumber(value) }}%</span
    >
  </div>
</template>

<script lang="ts">
export default {
  name: "EfficiencyBar",
  props: {
    value: {
      type: Number,
      required: true,
    },
  },
  methods: {
    getColorForValue(value: number) {
      if (value < 30) return "var(--p-red-500)"; // Low efficiency - red
      if (value < 70) return "var(--p-orange-500)"; // Medium efficiency - amber
      return "var(--p-emerald-600)"; // High efficiency - green
    },
    formatNumber(value: number) {
      return new Intl.NumberFormat(navigator.language, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
      }).format(value);
    },
  },
  template: "#internal",
};
</script>

<style scoped>
.efficiency-bar {
  position: relative;
  width: 100%;
  height: 24px;
  border-radius: 6px;
  overflow: hidden;
  border-style: solid;
  border-color: var(--p-primary-100);
  border-width: 2px;
}

.efficiency-bar-fill {
  height: 100%;
  border-radius: 4px;
  background-color: var(--p-primary-100);
  transition: width 0.5s ease;
}

.efficiency-bar-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #000;
  font-size: 18px;
  font-weight: bold;
  text-shadow: 0 0 2px rgba(255, 255, 255, 0.7);
}
</style>
