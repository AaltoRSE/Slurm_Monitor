<template>
  <div class="grid">
    <Card v-if="!showHistory" :class="showJobs ? 'col-12' : 'col-6'">
      <template #content>
        <JobsTable
          v-model:full="showJobs"
          :jobs="jobStore.currentJobs"
          :loading="jobStore.loading.currentJobs"
        />
      </template>
    </Card>

    <Card v-if="!showJobs" :class="showHistory ? 'col-12' : 'col-6'">
      <template #content>
        <JobHistory
          v-model:full="showHistory"
          :jobs="jobStore.jobHistory"
          :loading="jobStore.loading.jobHistory"
        />
      </template>
    </Card>

    <Card class="col-12">
      <template #title>Resource Quotas</template>
      <template #content>
        <QuotaDisplay
          :quotas="jobStore.quotas"
          :loading="jobStore.loading.quotas"
        />
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useJobStore } from "../stores/jobStore";
import Card from "primevue/card";
import Button from "primevue/button";
import JobsTable from "@/components/JobsTable.vue";
import JobHistory from "@/components/JobHistory.vue";
import QuotaDisplay from "@/components/QuotaDisplay.vue";
import { ref } from "vue";

const jobStore = useJobStore();
const showJobs = ref(false);
const showHistory = ref(false);
</script>
