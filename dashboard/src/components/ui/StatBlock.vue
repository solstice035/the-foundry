<script setup lang="ts">
defineProps<{
  value: string | number
  label: string
  color?: string
  size?: 'sm' | 'md' | 'lg'
}>()
</script>

<template>
  <div class="text-center">
    <div
      class="font-mono font-bold leading-none"
      :class="{
        'text-base': size === 'sm',
        'text-xl': !size || size === 'md',
        'text-2xl': size === 'lg',
      }"
      :style="{ color: color ?? '#E8600A' }"
    >
      {{ value }}
    </div>
    <div class="font-mono text-[0.52rem] text-foundry-slag tracking-[0.1em] mt-1 font-medium">{{ label }}</div>
  </div>
</template>
