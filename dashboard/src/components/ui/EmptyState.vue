<script setup lang="ts">
defineProps<{
  message?: string
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-12 text-center">
    <div class="text-foundry-slag-dim text-3xl mb-3">&#9776;</div>
    <p class="font-mono text-xs text-foundry-slag tracking-wide">{{ message ?? 'No data available' }}</p>
  </div>
</template>
