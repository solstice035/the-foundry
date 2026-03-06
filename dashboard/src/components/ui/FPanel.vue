<script setup lang="ts">
defineProps<{
  label?: string
  labelRight?: boolean
  noPad?: boolean
}>()
</script>

<template>
  <div class="bg-foundry-panel border border-foundry-border flex flex-col overflow-hidden">
    <div v-if="label" class="px-3 py-1.5 border-b border-foundry-border flex justify-between items-center bg-foundry-border/20 shrink-0">
      <span class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.14em]">{{ label }}</span>
      <slot name="label-right" />
    </div>
    <div :class="['flex-1 overflow-hidden flex flex-col', noPad ? '' : 'p-3']">
      <slot />
    </div>
  </div>
</template>
