<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: string
  size?: number
}>()

const color = computed(() => {
  switch (props.status) {
    case 'forged': case 'success': case 'complete': return 'bg-foundry-green shadow-[0_0_6px_rgba(45,138,78,0.5)]'
    case 'rejected': case 'failure': case 'failed': return 'bg-foundry-red shadow-[0_0_6px_rgba(196,48,48,0.5)]'
    case 'running': case 'in_progress': return 'bg-foundry-molten shadow-[0_0_6px_rgba(232,96,10,0.5)] animate-glow'
    default: return 'bg-foundry-slag-dim'
  }
})
</script>

<template>
  <div :class="['shrink-0 rounded-sm', color]" :style="{ width: `${size ?? 6}px`, height: `${size ?? 6}px` }" />
</template>
