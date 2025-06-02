<script setup lang="ts">
import { Button, Popover } from 'primevue'
import { watch, ref, defineProps, type PropType } from 'vue'
import type { FinishedJob, Quota, RunningJob } from '@/lib/types'
import JobCard from './JobCard.vue'

const props = defineProps({
  jobData: {
    type: Object as PropType<RunningJob | FinishedJob>,
    required: true
  }
})

const hover = ref(false)
const openDetails = ref(false)
const showDetails = ref(false)
const detailsPopup = ref()
watch(openDetails, async (newValue, oldValue) => {
  console.log(`OpenDetails : ${oldValue} -> ${newValue}`)
  if (newValue) {
    if (!oldValue) {
      // wasn't clicked before and now is clicked
      showDetails.value = true
    } else {
      showDetails.value = false
    }
  } else {
    if (showDetails.value) {
      showDetails.value = false
    }
  }
})
watch(showDetails, async (newValue, oldValue) => {
  console.log(`showDetails : ${oldValue} -> ${newValue}`)
  if (!newValue) {
    // it was closed, so we have to "re-arm" the openDetails button
    openDetails.value = false
  }
  console.log(detailsPopup.value)
  if (newValue) {
    detailsPopup.value.show()
  } else {
    detailsPopup.value.hide()
  }
})

watch(hover, async (newValue, oldValue) => {
  console.log(`hover : ${oldValue} -> ${newValue}`)
  if (openDetails.value) {
    // it's actively open
    return
  }
  if (newValue) {
    showDetails.value = true
  } else {
    showDetails.value = false
  }
})
</script>

<template>
  <Button
    icon="pi pi-info-circle"
    @mouseover="hover = true"
    @mouseleave="hover = false"
    @click="showDetails = !showDetails"
    outlined
    rounded
    size="small"
    aria-label="Job Details"
  />
  <Popover ref="detailsPopup">
    <div>Here is just some overlay</div>
    <!--<JobCard :job="jobData"></JobCard>-->
  </Popover>
</template>
