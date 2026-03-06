<script setup lang="ts">
defineProps<{
  color?: string
}>()
</script>

<template>
  <span
    class="font-mono text-[0.6rem] px-2 py-0.5 bg-foundry-slag-dim/50 inline-block tracking-wide"
    :style="{ color: color ?? '#6B6B73' }"
  >
    <slot />
  </span>
</template>
