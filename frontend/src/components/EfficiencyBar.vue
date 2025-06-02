<template>
  <div class="efficiency-bar">
    <div
      class="efficiency-bar-fill"
      :style="{
        width: `${value}%`,
        backgroundColor: getColorForValue(value),
      }"
    ></div>
    <span class="efficiency-bar-label">{{ value }}%</span>
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
      if (value < 30) return "#ef4444"; // Low efficiency - red
      if (value < 70) return "#f59e0b"; // Medium efficiency - amber
      return "#22c55e"; // High efficiency - green
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
  background-color: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.efficiency-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.efficiency-bar-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #000;
  font-size: 12px;
  font-weight: 600;
  text-shadow: 0 0 2px rgba(255, 255, 255, 0.7);
}
</style>
