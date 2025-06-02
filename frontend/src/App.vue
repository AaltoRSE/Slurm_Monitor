<template>
  <div class="app-container">
    <Layout />
    <Toast position="bottom-right" />
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import Toast from "primevue/toast";
import Layout from "./components/Layout.vue";
import { useJobStore } from "./stores/jobStore";

const jobStore = useJobStore();

onMounted(() => {
  // Initialize data
  jobStore.fetchCurrentJobsData();
  jobStore.fetchJobHistoryData();
  jobStore.fetchQuotasData();
});
</script>

<style>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
