<script setup lang="ts">
import { C } from '@/design/tokens'

defineProps<{ size?: number }>()
</script>

<template>
  <svg :width="size ?? 22" :height="(size ?? 22) * 0.75" viewBox="0 0 64 48" fill="none">
    <path d="M14 30h36l3 6H11l3-6z" :fill="C.molten" opacity="0.85"/>
    <path d="M18 22h28v8H18z" :fill="C.molten"/>
    <path d="M22 17h20l3 5H19l3-5z" :fill="C.molten"/>
    <path d="M42 18h10l5 4H45z" :fill="C.molten" opacity="0.7"/>
    <rect x="29" y="18" width="3" height="3" :fill="C.bg"/>
    <path d="M9 36h46v3H9z" :fill="C.molten" opacity="0.5"/>
    <circle cx="45" cy="11" r="1.2" :fill="C.white" opacity="0.8"/>
    <circle cx="48" cy="8" r="0.8" :fill="C.white" opacity="0.5"/>
  </svg>
</template>
