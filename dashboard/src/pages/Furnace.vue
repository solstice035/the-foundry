<script setup lang="ts">
import { computed } from 'vue'
import { useFoundryStore } from '@/stores/foundry'
import { useFormatters } from '@/composables/useFormatters'
import FPanel from '@/components/ui/FPanel.vue'
import GaugeBar from '@/components/ui/GaugeBar.vue'
import Sparkline from '@/components/ui/Sparkline.vue'
import StatBlock from '@/components/ui/StatBlock.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { C } from '@/design/tokens'

const store = useFoundryStore()
const { fmtDuration, fmtCost } = useFormatters()

// Latest night for "live" display
const latestDate = computed(() => store.nightsSorted[0])
const latestNight = computed(() => latestDate.value ? store.getNight(latestDate.value) : null)
const latestMetric = computed(() => latestDate.value ? store.getMetric(latestDate.value) : null)

// Pipeline stages with timing
const stageTimings = computed(() => {
  if (!latestNight.value?.state?.stages) return []
  return Object.entries(latestNight.value.state.stages).map(([name, stage]) => {
    let duration = 0
    if (stage.started_at && stage.completed_at) {
      duration = Math.round((new Date(stage.completed_at).getTime() - new Date(stage.started_at).getTime()) / 1000)
    } else if (stage.started_at && stage.compiled_at) {
      duration = Math.round((new Date(stage.compiled_at).getTime() - new Date(stage.started_at).getTime()) / 1000)
    }
    return { name, ...stage, duration }
  })
})

// Aggregate stage durations across all nights
const avgStageDurations = computed(() => {
  const totals: Record<string, { sum: number; count: number }> = {}
  for (const date of store.nightsSorted) {
    const night = store.getNight(date)
    if (!night?.state?.stages) continue
    for (const [name, stage] of Object.entries(night.state.stages)) {
      if (stage.started_at && (stage.completed_at || stage.compiled_at)) {
        const end = stage.completed_at ?? stage.compiled_at!
        const dur = Math.round((new Date(end).getTime() - new Date(stage.started_at).getTime()) / 1000)
        if (!totals[name]) totals[name] = { sum: 0, count: 0 }
        totals[name].sum += dur
        totals[name].count++
      }
    }
  }
  return Object.entries(totals).map(([name, { sum, count }]) => ({
    name,
    avg: Math.round(sum / count),
    total: sum,
    runs: count,
  }))
})

// Cost sparkline over time
const costOverTime = computed(() =>
  store.raw?.metrics
    .sort((a, b) => a.date.localeCompare(b.date))
    .map(m => m.cost_usd || 0) ?? []
)

// Duration sparkline over time
const durationOverTime = computed(() =>
  store.raw?.metrics
    .filter(m => m.type === 'success')
    .sort((a, b) => a.date.localeCompare(b.date))
    .map(m => m.total_duration_s || 0) ?? []
)

// Resource gauges
const successRate = computed(() => store.metrics?.successRate ?? 0)
const totalRuns = computed(() => store.metrics?.total ?? 0)

function stageStatusClass(status: string) {
  switch (status) {
    case 'complete': return 'text-foundry-green'
    case 'running': case 'in_progress': return 'text-foundry-molten animate-pulse'
    case 'failed': case 'error': return 'text-foundry-red'
    default: return 'text-foundry-slag-dim'
  }
}

function stageBarColor(status: string) {
  switch (status) {
    case 'complete': return C.green
    case 'running': case 'in_progress': return C.molten
    case 'failed': case 'error': return C.red
    default: return C.slagDim
  }
}
</script>

<template>
  <div class="h-full overflow-auto p-4">
    <div class="mb-4">
      <div class="font-mono text-[0.6rem] text-foundry-molten tracking-[0.18em] mb-1">PIPELINE SIMULATION</div>
      <h2 class="font-display text-2xl text-foundry-white tracking-wide">FURNACE</h2>
    </div>

    <EmptyState v-if="!latestNight" message="No pipeline data available" />

    <template v-else>
      <div class="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-3">
        <!-- Main: Pipeline stages -->
        <div class="flex flex-col gap-3">
          <!-- Live Terminal -->
          <FPanel :label="`PIPELINE — ${latestDate}`">
            <template #label-right>
              <span class="font-mono text-[0.55rem] tracking-wider"
                :class="latestNight.state?.pipeline_status === 'complete' || latestNight.state?.pipeline_complete
                  ? 'text-foundry-green' : 'text-foundry-molten animate-pulse'"
              >
                {{ latestNight.state?.pipeline_status?.toUpperCase() ?? latestNight.state?.outcome?.toUpperCase() ?? 'UNKNOWN' }}
              </span>
            </template>

            <div class="bg-foundry-bg p-4 font-mono text-xs space-y-3">
              <div v-for="stage in stageTimings" :key="stage.name" class="flex items-center gap-3">
                <!-- Stage indicator -->
                <div class="w-3 h-3 rounded-sm shrink-0"
                  :class="{
                    'bg-foundry-green': stage.status === 'complete',
                    'bg-foundry-molten animate-glow': stage.status === 'running' || stage.status === 'in_progress',
                    'bg-foundry-red': stage.status === 'failed' || stage.status === 'error',
                    'bg-foundry-slag-dim': !['complete','running','in_progress','failed','error'].includes(stage.status),
                  }"
                />

                <!-- Stage name -->
                <span class="w-20 text-foundry-slag tracking-wider">{{ stage.name.toUpperCase() }}</span>

                <!-- Progress bar -->
                <div class="flex-1 h-2 bg-foundry-slag-dim/50 relative">
                  <div
                    class="h-full transition-all duration-1000"
                    :style="{
                      width: stage.status === 'complete' ? '100%' : stage.status === 'running' ? '60%' : '0%',
                      background: stageBarColor(stage.status),
                      boxShadow: stage.status !== 'pending' ? `0 0 8px ${stageBarColor(stage.status)}30` : 'none',
                    }"
                  />
                </div>

                <!-- Duration -->
                <span class="w-16 text-right" :class="stageStatusClass(stage.status)">
                  {{ stage.duration > 0 ? fmtDuration(stage.duration) : '—' }}
                </span>

                <!-- Status -->
                <span class="w-16 text-right text-[0.6rem]" :class="stageStatusClass(stage.status)">
                  {{ stage.status }}
                </span>
              </div>
            </div>

            <!-- Summary line -->
            <div v-if="latestMetric" class="mt-3 flex gap-6 border-t border-foundry-border/30 pt-2">
              <span class="font-mono text-[0.6rem] text-foundry-slag">
                TOTAL: <span class="text-foundry-molten font-semibold">{{ fmtDuration(latestMetric.total_duration_s) }}</span>
              </span>
              <span class="font-mono text-[0.6rem] text-foundry-slag">
                COST: <span class="text-foundry-brass font-semibold">{{ fmtCost(latestMetric.cost_usd) }}</span>
              </span>
              <span v-if="latestMetric.project" class="font-mono text-[0.6rem] text-foundry-slag">
                OUTPUT: <span class="text-foundry-white font-semibold">{{ latestMetric.project }}</span>
              </span>
            </div>
          </FPanel>

          <!-- Average stage durations -->
          <FPanel label="AVERAGE STAGE DURATIONS">
            <div class="space-y-2">
              <div v-for="stage in avgStageDurations" :key="stage.name">
                <div class="flex justify-between mb-0.5">
                  <span class="font-mono text-[0.6rem] text-foundry-slag tracking-wide">{{ stage.name.toUpperCase() }}</span>
                  <span class="font-mono text-xs text-foundry-molten">{{ fmtDuration(stage.avg) }}</span>
                </div>
                <div class="h-1.5 bg-foundry-slag-dim/50">
                  <div
                    class="h-full bg-foundry-molten transition-all duration-700"
                    :style="{ width: `${Math.min((stage.avg / Math.max(...avgStageDurations.map(s => s.avg), 1)) * 100, 100)}%` }"
                  />
                </div>
              </div>
            </div>
          </FPanel>
        </div>

        <!-- Right sidebar: Resource gauges -->
        <div class="flex flex-col gap-3">
          <FPanel label="RESOURCE GAUGES">
            <div class="space-y-3">
              <GaugeBar
                label="SUCCESS"
                :value="store.metrics?.successCount ?? 0"
                :max="totalRuns"
                :color="C.green"
              />
              <GaugeBar
                label="FAILURES"
                :value="store.metrics?.failureCount ?? 0"
                :max="totalRuns"
                :color="C.red"
              />
              <GaugeBar
                label="STREAK"
                :value="store.metrics?.streak ?? 0"
                :max="totalRuns"
                :color="C.molten"
              />
            </div>
          </FPanel>

          <FPanel label="FORGE TEMPERATURE">
            <div class="flex flex-col items-center py-4">
              <div class="font-display text-5xl leading-none" :style="{ color: successRate > 80 ? C.molten : successRate > 50 ? C.brass : C.red }">
                {{ Math.round(successRate) }}%
              </div>
              <div class="font-mono text-[0.52rem] text-foundry-slag tracking-wider mt-2">SUCCESS RATE</div>
            </div>
          </FPanel>

          <FPanel label="COST TREND">
            <Sparkline :data="costOverTime" :color="C.brass" :height="40" />
          </FPanel>

          <FPanel label="DURATION TREND">
            <Sparkline :data="durationOverTime" :color="C.molten" :height="40" />
          </FPanel>

          <FPanel label="BUILD REPOS">
            <div class="font-display text-3xl text-foundry-white text-center py-2">
              {{ store.raw?.build_repos.length ?? 0 }}
            </div>
            <div class="font-mono text-[0.52rem] text-foundry-slag tracking-wider text-center">REPOS CREATED</div>
          </FPanel>
        </div>
      </div>
    </template>
  </div>
</template>
