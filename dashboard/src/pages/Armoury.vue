<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useFoundryStore } from '@/stores/foundry'
import { useFormatters } from '@/composables/useFormatters'
import FPanel from '@/components/ui/FPanel.vue'
import StatusDot from '@/components/ui/StatusDot.vue'
import TagBadge from '@/components/ui/TagBadge.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { C } from '@/design/tokens'

const store = useFoundryStore()
const router = useRouter()
const { fmtDate, fmtDuration, fmtCost } = useFormatters()

const sortBy = ref<'date' | 'cost' | 'duration'>('date')
const filterSource = ref<string>('')

const allSources = computed(() => {
  const sources = new Set<string>()
  store.raw?.metrics.forEach(m => { if (m.source) sources.add(m.source) })
  return [...sources].sort()
})

const builds = computed(() => {
  let list = store.buildList
  if (filterSource.value) {
    list = list.filter(b => b.metric?.source === filterSource.value)
  }
  if (sortBy.value === 'cost') {
    return [...list].sort((a, b) => (b.metric?.cost_usd ?? 0) - (a.metric?.cost_usd ?? 0))
  }
  if (sortBy.value === 'duration') {
    return [...list].sort((a, b) => (b.metric?.total_duration_s ?? 0) - (a.metric?.total_duration_s ?? 0))
  }
  return list
})
</script>

<template>
  <div class="h-full overflow-auto p-4">
    <div class="flex items-end justify-between mb-4">
      <div>
        <div class="font-mono text-[0.6rem] text-foundry-molten tracking-[0.18em] mb-1">BUILD COLLECTION</div>
        <h2 class="font-display text-2xl text-foundry-white tracking-wide">ARMOURY</h2>
      </div>

      <!-- Filter bar -->
      <div class="flex gap-2 items-center">
        <select
          v-model="filterSource"
          class="font-mono text-[0.65rem] bg-foundry-panel border border-foundry-border text-foundry-slag px-2 py-1 tracking-wide"
        >
          <option value="">ALL SOURCES</option>
          <option v-for="s in allSources" :key="s" :value="s">{{ s.toUpperCase() }}</option>
        </select>
        <div class="flex">
          <button
            v-for="opt in ([['date', 'DATE'], ['cost', 'COST'], ['duration', 'TIME']] as const)"
            :key="opt[0]"
            @click="sortBy = opt[0]"
            class="font-mono text-[0.6rem] px-2.5 py-1 border border-foundry-border cursor-pointer transition-colors"
            :class="sortBy === opt[0]
              ? 'bg-foundry-molten/10 text-foundry-molten border-foundry-molten/30'
              : 'bg-transparent text-foundry-slag hover:text-foundry-white'"
          >
            {{ opt[1] }}
          </button>
        </div>
      </div>
    </div>

    <EmptyState v-if="!builds.length" message="No builds match the current filter" />

    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
      <div
        v-for="b in builds"
        :key="b.date"
        class="bg-foundry-panel border border-foundry-border hover:border-foundry-molten/30 cursor-pointer transition-colors group"
        @click="router.push({ name: 'proving-ground', params: { date: b.date } })"
      >
        <div class="p-3">
          <div class="flex justify-between items-start mb-2">
            <div>
              <div class="font-mono text-sm font-semibold text-foundry-white group-hover:text-foundry-molten transition-colors">
                {{ b.night.build?.project_name ?? b.date }}
              </div>
              <div class="font-mono text-[0.6rem] text-foundry-slag-dim mt-0.5">{{ fmtDate(b.date, 'long') }}</div>
            </div>
            <StatusDot :status="b.night.build?.status === 'success' ? 'forged' : 'rejected'" />
          </div>

          <p class="font-body text-xs text-foundry-white/60 leading-relaxed mb-3 line-clamp-2">
            {{ b.night.build?.description ?? 'No description' }}
          </p>

          <div class="flex gap-1 flex-wrap mb-3">
            <TagBadge v-if="b.metric?.source" :color="C.blue">{{ b.metric.source }}</TagBadge>
            <TagBadge v-if="b.metric?.category" :color="C.brass">{{ b.metric.category }}</TagBadge>
            <template v-if="b.night.build?.tech_stack && typeof b.night.build.tech_stack === 'object'">
              <TagBadge v-for="(v, k) in b.night.build.tech_stack" :key="String(k)">{{ v }}</TagBadge>
            </template>
          </div>

          <div class="flex justify-between items-center border-t border-foundry-border/50 pt-2">
            <span class="font-mono text-[0.62rem] font-medium text-foundry-molten">
              {{ b.metric ? fmtDuration(b.metric.total_duration_s) : '—' }}
            </span>
            <span class="font-mono text-[0.62rem] font-medium text-foundry-brass">
              {{ b.metric ? fmtCost(b.metric.cost_usd) : '—' }}
            </span>
            <span class="font-mono text-[0.6rem] text-foundry-slag">
              → PROVE
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
