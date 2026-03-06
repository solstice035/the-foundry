<script setup lang="ts">
import { ref, computed } from 'vue'
import { useFoundryStore } from '@/stores/foundry'
import { useFormatters } from '@/composables/useFormatters'
import FPanel from '@/components/ui/FPanel.vue'
import TagBadge from '@/components/ui/TagBadge.vue'
import Sparkline from '@/components/ui/Sparkline.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { C } from '@/design/tokens'

const store = useFoundryStore()
const { fmtDate } = useFormatters()

const selectedDate = ref<string>('')

const dates = computed(() => store.nightsSorted)

const currentDate = computed(() => selectedDate.value || dates.value[0] || '')
const night = computed(() => store.getNight(currentDate.value))
const trends = computed(() => night.value?.trends_top ?? [])
const meta = computed(() => night.value?.trends_meta)

// Aggregate: trends found per night for sparkline
const trendsPerNight = computed(() =>
  dates.value.map(d => store.getNight(d)?.trends_meta?.total_trends ?? 0).reverse()
)

// Lifecycle summary across all nights
const lifecycleTotals = computed(() => {
  const totals: Record<string, number> = {}
  for (const d of dates.value) {
    const m = store.getNight(d)?.trends_meta
    if (m?.lifecycle_summary) {
      for (const [status, count] of Object.entries(m.lifecycle_summary)) {
        totals[status] = (totals[status] ?? 0) + count
      }
    }
  }
  return totals
})

function lifecycleColor(status: string): string {
  switch (status) {
    case 'rising': return C.green
    case 'peaking': return C.molten
    case 'declining': return C.red
    case 'stable': return C.blue
    default: return C.slag
  }
}
</script>

<template>
  <div class="h-full overflow-auto p-4">
    <div class="flex items-end justify-between mb-4">
      <div>
        <div class="font-mono text-[0.6rem] text-foundry-molten tracking-[0.18em] mb-1">TREND INTELLIGENCE</div>
        <h2 class="font-display text-2xl text-foundry-white tracking-wide">ORE SEAM</h2>
      </div>
      <select
        v-model="selectedDate"
        class="font-mono text-[0.65rem] bg-foundry-panel border border-foundry-border text-foundry-slag px-2 py-1 tracking-wide"
      >
        <option value="">LATEST</option>
        <option v-for="d in dates" :key="d" :value="d">{{ d }}</option>
      </select>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-[1fr_280px] gap-3">
      <!-- Main: Trend table -->
      <div class="flex flex-col gap-3">
        <FPanel :label="`TRENDS — ${currentDate}`" noPad>
          <EmptyState v-if="!trends.length" message="No trends data for this night" />
          <div v-else class="flex-1 overflow-auto">
            <table class="w-full border-collapse">
              <thead>
                <tr class="border-b border-foundry-border">
                  <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">SOURCE</th>
                  <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">TITLE</th>
                  <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">LIFECYCLE</th>
                  <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-right">SCORE</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(trend, i) in trends" :key="i" class="border-b border-foundry-border/30">
                  <td class="px-3 py-2">
                    <TagBadge v-if="trend.source" :color="C.blue">{{ trend.source }}</TagBadge>
                  </td>
                  <td class="font-mono text-xs text-foundry-white/70 px-3 py-2">{{ trend.title }}</td>
                  <td class="px-3 py-2">
                    <TagBadge v-if="trend.lifecycle_status" :color="lifecycleColor(trend.lifecycle_status)">
                      {{ trend.lifecycle_status }}
                    </TagBadge>
                  </td>
                  <td class="font-mono text-xs text-foundry-molten px-3 py-2 text-right font-semibold">
                    {{ trend.final_score?.toFixed(1) ?? trend.buildability_score ?? '—' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </FPanel>

        <FPanel v-if="meta" label="SCAN METADATA">
          <div class="grid grid-cols-3 gap-4">
            <div class="text-center">
              <div class="font-mono text-lg font-bold text-foundry-molten">{{ meta.total_trends }}</div>
              <div class="font-mono text-[0.52rem] text-foundry-slag tracking-wide">TOTAL TRENDS</div>
            </div>
            <div class="text-center">
              <div class="font-mono text-lg font-bold text-foundry-white">{{ Object.keys(meta.lifecycle_summary).length }}</div>
              <div class="font-mono text-[0.52rem] text-foundry-slag tracking-wide">LIFECYCLE STATES</div>
            </div>
            <div class="text-center">
              <div class="font-mono text-lg font-bold text-foundry-blue">{{ meta.sources_scanned?.length ?? '—' }}</div>
              <div class="font-mono text-[0.52rem] text-foundry-slag tracking-wide">SOURCES</div>
            </div>
          </div>
        </FPanel>
      </div>

      <!-- Sidebar -->
      <div class="flex flex-col gap-3">
        <FPanel label="VOLUME TREND">
          <Sparkline :data="trendsPerNight" :color="C.brass" :height="48" />
          <div class="font-mono text-[0.52rem] text-foundry-slag mt-1">Trends found per night</div>
        </FPanel>

        <FPanel label="LIFECYCLE SUMMARY">
          <div class="space-y-1.5">
            <div v-for="(count, status) in lifecycleTotals" :key="String(status)" class="flex justify-between items-center">
              <TagBadge :color="lifecycleColor(String(status))">{{ String(status) }}</TagBadge>
              <span class="font-mono text-xs font-semibold" :style="{ color: lifecycleColor(String(status)) }">{{ count }}</span>
            </div>
          </div>
          <EmptyState v-if="!Object.keys(lifecycleTotals).length" message="No lifecycle data" />
        </FPanel>
      </div>
    </div>
  </div>
</template>
