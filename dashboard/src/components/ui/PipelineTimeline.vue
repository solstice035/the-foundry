<script setup lang="ts">
import { computed } from 'vue'
import type { PipelineState } from '@/types'

const props = defineProps<{
  state: PipelineState
}>()

const stages = ['scout', 'spec', 'builder', 'briefing'] as const

const stageData = computed(() =>
  stages.map(name => ({
    name,
    label: name.toUpperCase(),
    status: props.state.stages[name]?.status ?? 'pending',
  }))
)

function statusColor(status: string) {
  switch (status) {
    case 'complete': return 'bg-foundry-green'
    case 'running': case 'in_progress': return 'bg-foundry-molten animate-glow'
    case 'failed': case 'error': return 'bg-foundry-red'
    default: return 'bg-foundry-slag-dim'
  }
}
</script>

<template>
  <div class="flex items-center gap-1">
    <template v-for="(stage, i) in stageData" :key="stage.name">
      <div class="flex items-center gap-1.5">
        <div :class="['w-2 h-2 rounded-sm', statusColor(stage.status)]" />
        <span class="font-mono text-[0.55rem] text-foundry-slag tracking-wide">{{ stage.label }}</span>
      </div>
      <div v-if="i < stageData.length - 1" class="w-4 h-px bg-foundry-border" />
    </template>
  </div>
</template>
