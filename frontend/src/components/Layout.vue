<template>
  <div class="flex flex-column min-h-screen">
    <Header />
    <div class="flex-grow-1 p-4">
      <BaseView />
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from "./Header.vue";
import BaseView from "./BaseView.vue";
</script>
