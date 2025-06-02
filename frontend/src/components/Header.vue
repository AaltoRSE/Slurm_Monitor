<template>
  <header
    class="flex align-items-center justify-content-between p-3 bg-primary text-white"
  >
    <div class="flex align-items-center gap-2">
      <i class="pi pi-server text-xl"></i>
      <h1 class="text-xl font-bold m-0">Slurm Cluster Status</h1>
    </div>
    <div>
      <span class="font-semibold mr-2">{{ username }}</span>
      <Avatar :image="userAvatar" size="small" shape="circle" />
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Avatar from "primevue/avatar";

const username = ref("User.Name");
const userAvatar = ref(
  "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"
);
</script>
