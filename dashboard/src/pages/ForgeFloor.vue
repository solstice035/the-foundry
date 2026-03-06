<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useFoundryStore } from '@/stores/foundry'
import { useFormatters } from '@/composables/useFormatters'
import FPanel from '@/components/ui/FPanel.vue'
import StatusDot from '@/components/ui/StatusDot.vue'
import StatBlock from '@/components/ui/StatBlock.vue'
import GaugeBar from '@/components/ui/GaugeBar.vue'
import Sparkline from '@/components/ui/Sparkline.vue'
import PipelineTimeline from '@/components/ui/PipelineTimeline.vue'
import TagBadge from '@/components/ui/TagBadge.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { C } from '@/design/tokens'

const store = useFoundryStore()
const router = useRouter()
const { fmtDate, fmtDuration, fmtCost } = useFormatters()

const selectedIdx = ref(0)

const builds = computed(() => store.buildList)
const selected = computed(() => builds.value[selectedIdx.value] ?? null)

// Sparkline data: cost per build over time
const costSpark = computed(() =>
  store.raw?.metrics
    .filter(m => m.type === 'success')
    .sort((a, b) => a.date.localeCompare(b.date))
    .map(m => m.cost_usd || 0) ?? []
)

// Sparkline data: duration per build
const durationSpark = computed(() =>
  store.raw?.metrics
    .filter(m => m.type === 'success')
    .sort((a, b) => a.date.localeCompare(b.date))
    .map(m => m.total_duration_s || 0) ?? []
)

function nightStatus(date: string): string {
  const m = store.getMetric(date)
  return m?.type === 'success' ? 'forged' : m?.type === 'failure' ? 'rejected' : 'idle'
}
</script>

<template>
  <div v-if="store.loading" class="flex items-center justify-center h-full">
    <span class="font-mono text-sm text-foundry-slag animate-pulse">Loading forge data...</span>
  </div>

  <div v-else-if="!builds.length" class="flex items-center justify-center h-full">
    <EmptyState message="No builds forged yet. The anvil is cold." />
  </div>

  <div v-else class="grid grid-cols-[240px_1fr_280px] h-full overflow-hidden">
    <!-- Left: Ingot Rack -->
    <div class="flex flex-col border-r border-foundry-border bg-foundry-panel">
      <div class="px-3 py-2 border-b border-foundry-border bg-foundry-border/20">
        <span class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.14em]">INGOT RACK</span>
      </div>
      <div class="flex-1 overflow-auto p-1.5">
        <button
          v-for="(b, i) in builds"
          :key="b.date"
          @click="selectedIdx = i"
          class="w-full text-left p-2.5 block mb-0.5 border-l-2 cursor-pointer"
          :class="selectedIdx === i
            ? 'bg-foundry-molten/10 border-foundry-molten'
            : 'bg-transparent border-transparent hover:bg-foundry-border/20'"
        >
          <div class="flex justify-between items-center mb-1">
            <span class="font-mono text-[0.78rem] font-semibold" :class="selectedIdx === i ? 'text-foundry-white' : 'text-foundry-slag'">
              {{ b.night.build?.project_name ?? b.date }}
            </span>
            <StatusDot :status="nightStatus(b.date)" />
          </div>
          <div class="font-mono text-[0.6rem] text-foundry-slag-dim mb-1">{{ fmtDate(b.date, 'long') }}</div>
          <div class="flex gap-2.5">
            <span class="font-mono text-[0.62rem] font-medium text-foundry-molten">
              {{ b.metric ? fmtDuration(b.metric.total_duration_s) : '—' }}
            </span>
            <span class="font-mono text-[0.62rem] font-medium text-foundry-green">
              {{ b.metric ? fmtCost(b.metric.cost_usd) : '—' }}
            </span>
          </div>
        </button>
      </div>
      <!-- Rack summary -->
      <div class="p-2.5 border-t border-foundry-border bg-foundry-border/20">
        <div v-if="store.metrics" class="space-y-0.5">
          <div class="flex justify-between" v-for="stat in [
            { l: 'FORGED', v: store.metrics.successCount, c: 'text-foundry-white' },
            { l: 'STREAK', v: store.metrics.streak, c: 'text-foundry-molten' },
            { l: 'AVG TIME', v: fmtDuration(Math.round(store.metrics.avgDuration)), c: 'text-foundry-molten' },
            { l: 'AVG COST', v: fmtCost(store.metrics.avgCost), c: 'text-foundry-slag' },
          ]" :key="stat.l">
            <span class="font-mono text-[0.58rem] text-foundry-slag tracking-wide">{{ stat.l }}</span>
            <span class="font-mono text-[0.65rem] font-semibold" :class="stat.c">{{ stat.v }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Center: Detail -->
    <div class="grid grid-rows-[auto_1fr] gap-px overflow-hidden">
      <FPanel :label="`INGOT: ${(selected?.night.build?.project_name ?? '').toUpperCase()}`">
        <template #label-right>
          <span class="font-mono text-[0.55rem] font-semibold tracking-[0.1em] border px-2 py-0.5"
            :class="selected?.night.build?.status === 'success'
              ? 'text-foundry-green border-foundry-green'
              : 'text-foundry-red border-foundry-red'"
          >
            {{ selected?.night.build?.status === 'success' ? 'QUENCHED' : 'FAILED' }}
          </span>
        </template>

        <div class="flex gap-5 flex-wrap">
          <div class="flex-1 min-w-[280px]">
            <p class="font-body text-sm text-foundry-white/70 leading-relaxed mb-2.5">
              {{ selected?.night.build?.description ?? selected?.night.spec?.reasoning ?? 'No description' }}
            </p>
            <div class="flex gap-1 flex-wrap">
              <TagBadge v-if="selected?.night.build?.tech_stack">
                {{ typeof selected.night.build.tech_stack === 'object'
                  ? Object.values(selected.night.build.tech_stack).join(' / ')
                  : selected.night.build.tech_stack }}
              </TagBadge>
              <TagBadge v-if="selected?.metric?.category" :color="C.brass">{{ selected.metric.category }}</TagBadge>
              <TagBadge v-if="selected?.metric?.source" :color="C.blue">{{ selected.metric.source }}</TagBadge>
            </div>
          </div>
          <div class="flex gap-5 items-start">
            <StatBlock
              :value="selected?.metric ? fmtDuration(selected.metric.total_duration_s) : '—'"
              label="FORGE TIME"
            />
            <StatBlock
              :value="selected?.metric ? fmtCost(selected.metric.cost_usd) : '—'"
              label="COST"
              :color="C.brass"
            />
          </div>
        </div>

        <!-- Gauge bars -->
        <div class="mt-3 space-y-1.5" v-if="selected?.night.build?.tests">
          <GaugeBar
            label="TESTS"
            :value="selected.night.build.tests.passed ?? 0"
            :max="selected.night.build.tests.total ?? 0"
            :color="C.green"
          />
        </div>

        <div class="mt-3">
          <button
            @click="router.push({ name: 'proving-ground', params: { date: selected?.date } })"
            class="font-mono text-[0.7rem] font-medium px-3.5 py-1 bg-transparent text-foundry-molten border border-foundry-molten/30 hover:border-foundry-molten hover:bg-foundry-molten/5 cursor-pointer tracking-wide transition-colors"
          >
            DEEP DIVE →
          </button>
        </div>
      </FPanel>

      <!-- Features list -->
      <FPanel label="FEATURES FORGED" noPad>
        <div class="flex-1 overflow-auto p-3">
          <div v-if="selected?.night.build?.features_implemented?.length">
            <div
              v-for="(feat, i) in selected.night.build.features_implemented"
              :key="i"
              class="flex gap-2 py-1 border-b border-foundry-border/30 last:border-0"
            >
              <span class="text-foundry-green text-xs shrink-0">&#10003;</span>
              <span class="font-mono text-xs text-foundry-white/70">{{ feat }}</span>
            </div>
          </div>
          <EmptyState v-else message="No features data for this build" />
        </div>
      </FPanel>
    </div>

    <!-- Right: KPIs + Sparklines + Pipeline -->
    <div class="flex flex-col border-l border-foundry-border overflow-auto">
      <!-- KPI stats -->
      <FPanel label="FORGE METRICS">
        <div class="grid grid-cols-2 gap-4" v-if="store.metrics">
          <StatBlock :value="store.metrics.successCount" label="FORGED" :color="C.green" />
          <StatBlock :value="`${Math.round(store.metrics.successRate)}%`" label="SUCCESS" :color="C.molten" />
          <StatBlock :value="fmtCost(store.metrics.totalCost)" label="TOTAL COST" :color="C.brass" />
          <StatBlock :value="store.metrics.streak" label="STREAK" :color="C.molten" />
        </div>
      </FPanel>

      <!-- Sparklines -->
      <FPanel label="COST TREND">
        <Sparkline :data="costSpark" :color="C.brass" :height="36" />
      </FPanel>

      <FPanel label="DURATION TREND">
        <Sparkline :data="durationSpark" :color="C.molten" :height="36" />
      </FPanel>

      <!-- Pipeline for selected night -->
      <FPanel label="PIPELINE" v-if="selected?.night.state">
        <PipelineTimeline :state="selected.night.state" />
        <div class="mt-2 font-mono text-[0.55rem] text-foundry-slag">
          {{ selected.night.state.outcome ?? selected.night.state.pipeline_status ?? 'unknown' }}
        </div>
      </FPanel>

      <!-- Night log (last 7) -->
      <FPanel label="RECENT NIGHTS" noPad>
        <div class="flex-1 overflow-auto">
          <div
            v-for="date in store.nightsSorted.slice(0, 7)"
            :key="date"
            class="flex items-center gap-2 px-3 py-1.5 border-b border-foundry-border/30 hover:bg-foundry-border/10 cursor-pointer"
            @click="router.push({ name: 'proving-ground', params: { date } })"
          >
            <StatusDot :status="nightStatus(date)" />
            <span class="font-mono text-[0.65rem] text-foundry-white/80 flex-1">{{ fmtDate(date) }}</span>
            <span class="font-mono text-[0.6rem] text-foundry-slag">
              {{ store.getNight(date)?.build?.project_name ?? '—' }}
            </span>
          </div>
        </div>
      </FPanel>
    </div>
  </div>
</template>
