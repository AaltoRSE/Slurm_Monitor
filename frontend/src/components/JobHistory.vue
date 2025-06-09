<template>
  <div>
    <DataTable
      :value="jobs"
      :loading="loading"
      stripedRows
      :paginator="jobs.length > 10"
      :rows="10"
      paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
      :rowsPerPageOptions="[10, 20, 50]"
      sortField="endTime"
      :sortOrder="-1"
      :tableStyle="`min-width: ${full ? 80.5 : 12.5} rem`"
    >
      <template #empty> No job history found </template>

      <template #loading>
        <ProgressSpinner
          style="width: 50px; height: 50px"
          strokeWidth="8"
          fill="var(--surface-ground)"
          animationDuration=".5s"
        />
      </template>

      <Column field="id" header="Job ID" sortable style="min-width: 6.5rem" />
      <Column
        v-if="full"
        field="name"
        header="Job Name"
        sortable
        style="min-width: 10rem"
      />
      <Column field="status" header="Status" sortable style="min-width: 3rem">
        <template #body="slotProps">
          <Tag
            :value="slotProps.data.status"
            :severity="getStatusSeverity(slotProps.data.status)"
          />
        </template>
      </Column>
      <Column
        v-if="full"
        field="startTime"
        header="Start Time"
        sortable
        style="min-width: 14rem"
      >
        <template #body="slotProps">
          {{ formatDateTime(slotProps.data.startTime) }}
        </template>
      </Column>
      <Column
        v-if="full"
        field="endTime"
        header="End Time"
        sortable
        style="min-width: 14rem"
      >
        <template #body="slotProps">
          {{ formatDateTime(slotProps.data.endTime) }}
        </template>
      </Column>

      <Column v-if="full" header="CPU Usage" style="min-width: 10rem">
        <template #body="slotProps">
          <EfficiencyBar
            v-if="
              slotProps.data.efficiency &&
              slotProps.data.efficiency.cpu !== null
            "
            :value="slotProps.data.efficiency.cpu"
          />
          <span v-else>N/A</span>
        </template>
      </Column>

      <Column v-if="full" header="Memory Usage" style="min-width: 10rem">
        <template #body="slotProps">
          <EfficiencyBar
            v-if="
              slotProps.data.efficiency &&
              slotProps.data.efficiency.memory !== null
            "
            :value="slotProps.data.efficiency.memory"
          />
          <span v-else>N/A</span>
        </template>
      </Column>

      <Column v-if="full" header="GPU Usage" style="min-width: 10rem">
        <template #body="slotProps">
          <EfficiencyBar
            v-if="slotProps.data.resources.gpu"
            :value="slotProps.data.efficiency.gpu"
          />
          <span v-else>N/A</span>
        </template>
      </Column>
      <Column header="Details" style="min-width: 3rem">
        <template #body="slotProps">
          <Button
            @click="handleClick($event, slotProps.data)"
            @mouseleave="handleMouseLeave($event, slotProps.data)"
            @mouseover="handleMouseEnter($event, slotProps.data)"
            icon="pi pi-info-circle"
            outlined
            rounded
            size="small"
            aria-label="Job Details"
          ></Button>
        </template>
      </Column>
    </DataTable>
    <Popover
      @hide="onDetailHide"
      @show="onShow"
      ref="JobDetails"
      :style="{ pointerEvents: keepDisplay ? 'auto' : 'none' }"
    >
      <JobCard v-if="selectedJob" :job="selectedJob"></JobCard>
    </Popover>
  </div>
</template>

<script setup lang="ts">
import { defineProps, nextTick, ref } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Tag from "primevue/tag";
import ProgressSpinner from "primevue/progressspinner";
import EfficiencyBar from "./EfficiencyBar.vue";
import { Button, Popover } from "primevue";
import JobCard from "./JobCard.vue";
import type { RunningJob, FinishedJob } from "@/lib/types";
import { formatDateTime, getStatusSeverity } from "@/lib/utils";
const selectedJob = ref<FinishedJob | RunningJob | null>(null);
const keepDisplay = ref(false);
const JobDetails = ref();

defineProps({
  jobs: {
    type: Array<RunningJob | FinishedJob>,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  full: {
    type: Boolean,
    default: true,
  },
});

const handleMouseEnter = (event: any, jobData: FinishedJob) => {
  console.log("Shooting mouse enter");
  if (keepDisplay.value) {
    // we have something else displayed at the moment, so ignore this.
    return;
  }
  // also do nothing if something is already selected
  if (selectedJob.value) {
    return;
  }
  toggleJobDetails(event, jobData);
};

const handleMouseLeave = (event: any, jobData: FinishedJob) => {
  if (keepDisplay.value) {
    // we have something else displayed at the moment, so ignore this.
    return;
  }
  if (selectedJob.value) {
    // leave should only call selection if we have one selected
    toggleJobDetails(event, jobData);
  }
};
const handleClick = (event: any, jobData: FinishedJob) => {
  // if jobData wasn't set or was set to something else, we want to display
  // the clicked element and keep it, otherwise we want to toggle it
  if (selectedJob.value == null || selectedJob.value?.id != jobData.id) {
    // we change from nothing or to a different element.
    keepDisplay.value = true;
    //I think we need to reset the display data here.
    selectedJob.value = null;
  } else {
    // we keep being in the same element, thus just toggle.
    keepDisplay.value = !keepDisplay.value;
  }

  if (keepDisplay.value) {
    if (!selectedJob.value) {
      toggleJobDetails(event, jobData);
    }
  } else {
    // we don't want to keep the display
    if (selectedJob.value) {
      // and we have something selected. So unselect it.
      toggleJobDetails(event, jobData);
    }
  }
};
const onDetailHide = () => {
  keepDisplay.value = false;
  selectedJob.value = null;
};
const onShow = () => {
  console.log("Got Show event");
};
const toggleJobDetails = (event: any, jobData: FinishedJob) => {
  const currentKeepDisplay = keepDisplay.value;
  if (selectedJob.value) {
    JobDetails.value.hide();
  }
  if (selectedJob.value?.id === jobData.id) {
    selectedJob.value = null;
  } else {
    selectedJob.value = jobData;
    nextTick(() => {
      selectedJob.value = jobData;
      keepDisplay.value = currentKeepDisplay;
      JobDetails.value.show(event);
    });
  }
};
</script>
