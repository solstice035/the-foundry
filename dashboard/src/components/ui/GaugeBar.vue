<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  value: number
  max: number
  color?: string
  label?: string
}>()

const pct = computed(() => props.max > 0 ? (props.value / props.max) * 100 : 0)
const barColor = computed(() => props.color ?? '#2D8A4E')
</script>

<template>
  <div class="flex items-center gap-2">
    <span v-if="label" class="font-mono text-[0.6rem] font-medium text-foundry-slag min-w-[52px] tracking-wide">{{ label }}</span>
    <div class="flex-1 h-[3px] bg-foundry-slag-dim">
      <div
        class="h-full transition-[width] duration-700 ease-out"
        :style="{ width: `${pct}%`, background: barColor, boxShadow: `0 0 6px ${barColor}40` }"
      />
    </div>
    <span class="font-mono text-[0.6rem] font-semibold min-w-[36px] text-right" :style="{ color: barColor }">
      {{ value }}/{{ max }}
    </span>
  </div>
</template>
