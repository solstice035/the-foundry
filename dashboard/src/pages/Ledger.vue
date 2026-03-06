<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useFoundryStore } from '@/stores/foundry'
import { useFormatters } from '@/composables/useFormatters'
import FPanel from '@/components/ui/FPanel.vue'
import StatusDot from '@/components/ui/StatusDot.vue'
import StatBlock from '@/components/ui/StatBlock.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { C } from '@/design/tokens'

const store = useFoundryStore()
const router = useRouter()
const { fmtDate, fmtDuration, fmtCost } = useFormatters()

const rows = computed(() =>
  store.nightsSorted.map(date => {
    const night = store.getNight(date)
    const metric = store.getMetric(date)
    return {
      date,
      project: night?.build?.project_name ?? '—',
      status: metric?.type ?? 'idle',
      duration: metric?.total_duration_s ?? 0,
      cost: metric?.cost_usd ?? 0,
      source: metric?.source ?? '—',
      decision: night?.spec?.decision ?? '—',
    }
  })
)
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden p-4">
    <div class="flex items-end justify-between mb-4">
      <div>
        <div class="font-mono text-[0.6rem] text-foundry-molten tracking-[0.18em] mb-1">COMPLETE RECORD</div>
        <h2 class="font-display text-2xl text-foundry-white tracking-wide">LEDGER</h2>
      </div>
      <div v-if="store.metrics" class="flex gap-6">
        <StatBlock :value="store.metrics.total" label="TOTAL NIGHTS" :color="C.white" size="sm" />
        <StatBlock :value="store.metrics.successCount" label="FORGED" :color="C.green" size="sm" />
        <StatBlock :value="store.metrics.failureCount" label="FAILED" :color="C.red" size="sm" />
        <StatBlock :value="fmtCost(store.metrics.totalCost)" label="TOTAL COST" :color="C.brass" size="sm" />
      </div>
    </div>

    <FPanel label="ALL NIGHTS" noPad class="flex-1">
      <EmptyState v-if="!rows.length" message="No nights recorded" />
      <div v-else class="flex-1 overflow-auto">
        <table class="w-full border-collapse">
          <thead>
            <tr class="border-b border-foundry-border">
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left w-8"></th>
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">DATE</th>
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">PROJECT</th>
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">STATUS</th>
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">DECISION</th>
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-right">DURATION</th>
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-right">COST</th>
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">SOURCE</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="row in rows"
              :key="row.date"
              class="border-b border-foundry-border/30 hover:bg-foundry-molten/5 cursor-pointer transition-colors"
              @click="router.push({ name: 'proving-ground', params: { date: row.date } })"
            >
              <td class="px-3 py-2"><StatusDot :status="row.status" /></td>
              <td class="font-mono text-xs text-foundry-white/80 px-3 py-2">{{ fmtDate(row.date) }}</td>
              <td class="font-mono text-xs text-foundry-white px-3 py-2 font-medium">{{ row.project }}</td>
              <td class="font-mono text-xs px-3 py-2"
                :class="row.status === 'success' ? 'text-foundry-green' : row.status === 'failure' ? 'text-foundry-red' : 'text-foundry-slag-dim'"
              >
                {{ row.status.toUpperCase() }}
              </td>
              <td class="font-mono text-xs text-foundry-slag px-3 py-2">{{ row.decision }}</td>
              <td class="font-mono text-xs text-foundry-molten px-3 py-2 text-right">
                {{ row.duration > 0 ? fmtDuration(row.duration) : '—' }}
              </td>
              <td class="font-mono text-xs text-foundry-brass px-3 py-2 text-right">
                {{ row.cost > 0 ? fmtCost(row.cost) : '—' }}
              </td>
              <td class="font-mono text-xs text-foundry-slag px-3 py-2">{{ row.source }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </FPanel>
  </div>
</template>
