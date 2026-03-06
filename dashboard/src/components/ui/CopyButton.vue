<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  text: string
}>()

const copied = ref(false)

async function copy() {
  await navigator.clipboard.writeText(props.text)
  copied.value = true
  setTimeout(() => { copied.value = false }, 1500)
}
</script>

<template>
  <button
    @click="copy"
    class="font-mono text-[0.6rem] px-2 py-1 border border-foundry-border hover:border-foundry-molten/40 text-foundry-slag hover:text-foundry-molten transition-colors cursor-pointer"
  >
    {{ copied ? 'COPIED' : 'COPY' }}
  </button>
</template>
