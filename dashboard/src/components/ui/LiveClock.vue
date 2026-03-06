<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const time = ref(new Date())
let interval: ReturnType<typeof setInterval>

onMounted(() => {
  interval = setInterval(() => { time.value = new Date() }, 1000)
})
onUnmounted(() => clearInterval(interval))

function pad(n: number) { return String(n).padStart(2, '0') }
</script>

<template>
  <span class="font-mono font-semibold text-xs text-foundry-molten tracking-wider">
    {{ pad(time.getHours()) }}:{{ pad(time.getMinutes()) }}<span :class="time.getSeconds() % 2 ? 'opacity-30' : 'opacity-100'">:</span>{{ pad(time.getSeconds()) }}
  </span>
</template>
