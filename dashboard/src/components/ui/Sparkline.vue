<script setup lang="ts">
import { computed } from 'vue'
import { C } from '@/design/tokens'

const props = defineProps<{
  data: number[]
  color?: string
  height?: number
}>()

const h = computed(() => props.height ?? 32)
const lineColor = computed(() => props.color ?? C.molten)

const points = computed(() => {
  if (!props.data.length) return ''
  const max = Math.max(...props.data, 1)
  return props.data
    .map((v, i) => `${(i / Math.max(props.data.length - 1, 1)) * 100},${h.value - (v / max) * (h.value - 4)}`)
    .join(' ')
})

const fillPoints = computed(() => {
  if (!points.value) return ''
  return `0,${h.value} ${points.value} 100,${h.value}`
})
</script>

<template>
  <svg width="100%" :height="h" :viewBox="`0 0 100 ${h}`" preserveAspectRatio="none" class="block">
    <polyline :points="fillPoints" :fill="`${lineColor}10`" stroke="none" />
    <polyline :points="points" fill="none" :stroke="lineColor" stroke-width="1.5" vector-effect="non-scaling-stroke" />
  </svg>
</template>
