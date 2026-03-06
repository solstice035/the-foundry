<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { useFoundryStore } from '@/stores/foundry'
import AnvilLogo from '@/components/ui/AnvilLogo.vue'
import LiveClock from '@/components/ui/LiveClock.vue'

const store = useFoundryStore()
const route = useRoute()

const navItems = [
  { to: '/', label: 'FORGE', name: 'forge-floor' },
  { to: '/armoury', label: 'ARMOURY', name: 'armoury' },
  { to: '/ore', label: 'ORE', name: 'ore-seam' },
  { to: '/blueprints', label: 'BLUEPRINTS', name: 'blueprints' },
  { to: '/ledger', label: 'LEDGER', name: 'ledger' },
  { to: '/rejections', label: 'SLAG', name: 'rejections' },
  { to: '/social', label: 'SOCIAL', name: 'social' },
  { to: '/furnace', label: 'FURNACE', name: 'furnace' },
]

onMounted(() => {
  store.fetchData()
  store.startPolling()
})
</script>

<template>
  <div class="h-screen flex flex-col bg-foundry-bg overflow-hidden">
    <!-- Top Bar -->
    <header class="shrink-0 border-b border-foundry-border bg-foundry-panel flex items-center px-4 h-10 gap-4">
      <RouterLink to="/" class="flex items-center gap-2 no-underline">
        <AnvilLogo :size="18" />
        <span class="font-display text-lg text-foundry-white tracking-[0.08em] leading-none">THE FOUNDRY</span>
      </RouterLink>

      <nav class="flex items-center gap-0.5 ml-4">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :to="item.to"
          class="font-mono text-[0.6rem] font-medium px-2.5 py-1 tracking-[0.08em] no-underline transition-colors"
          :class="route.name === item.name || (item.name === 'forge-floor' && route.path === '/')
            ? 'text-foundry-molten bg-foundry-molten/10'
            : 'text-foundry-slag hover:text-foundry-white'"
        >
          {{ item.label }}
        </RouterLink>
      </nav>

      <div class="ml-auto flex items-center gap-3">
        <LiveClock />
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 overflow-hidden">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>

    <!-- Status Bar -->
    <footer class="shrink-0 border-t border-foundry-border bg-foundry-panel/50 flex items-center px-4 h-6 gap-4">
      <span class="font-mono text-[0.52rem] text-foundry-slag tracking-wide">
        <template v-if="store.loading">LOADING...</template>
        <template v-else-if="store.error">ERROR: {{ store.error }}</template>
        <template v-else-if="store.metrics">
          {{ store.metrics.successCount }} FORGED / {{ store.metrics.total }} NIGHTS / STREAK {{ store.metrics.streak }}
        </template>
      </span>
      <span v-if="store.lastFetched" class="ml-auto font-mono text-[0.48rem] text-foundry-slag-dim">
        LAST FETCH {{ store.lastFetched.toLocaleTimeString() }}
      </span>
    </footer>
  </div>
</template>
