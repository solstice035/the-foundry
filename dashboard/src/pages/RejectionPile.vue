<script setup lang="ts">
import { computed } from 'vue'
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
const { fmtDate, fmtDuration } = useFormatters()

// Failure nights (pipeline failures)
const failureNights = computed(() =>
  store.nightsSorted
    .filter(date => {
      const m = store.getMetric(date)
      return m?.type === 'failure'
    })
    .map(date => ({
      date,
      metric: store.getMetric(date)!,
      night: store.getNight(date),
    }))
)

// Nights where spec rejected all
const rejectedNights = computed(() =>
  store.nightsSorted
    .filter(date => {
      const night = store.getNight(date)
      return night?.spec?.decision === 'reject_all'
    })
    .map(date => ({
      date,
      night: store.getNight(date)!,
      reasoning: store.getNight(date)?.spec?.reasoning,
    }))
)

// All rejected alternatives across nights (with date context)
const rejectedAlternatives = computed(() => {
  const alts: { date: string; id: string; title: string; rejection_reason: string }[] = []
  for (const date of store.nightsSorted) {
    const night = store.getNight(date)
    if (night?.spec?.rejected_alternatives) {
      for (const alt of night.spec.rejected_alternatives) {
        alts.push({ date, ...alt })
      }
    }
  }
  return alts
})
</script>

<template>
  <div class="h-full overflow-auto p-4">
    <div class="mb-4">
      <div class="font-mono text-[0.6rem] text-foundry-molten tracking-[0.18em] mb-1">FAILURES & REJECTIONS</div>
      <h2 class="font-display text-2xl text-foundry-white tracking-wide">REJECTION PILE</h2>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-3">
      <!-- Pipeline Failures -->
      <FPanel label="PIPELINE FAILURES" noPad>
        <EmptyState v-if="!failureNights.length" message="No pipeline failures recorded" />
        <div v-else class="flex-1 overflow-auto">
          <div
            v-for="f in failureNights"
            :key="f.date"
            class="px-4 py-3 border-b border-foundry-border/30 hover:bg-foundry-red/5 cursor-pointer transition-colors"
            @click="router.push({ name: 'proving-ground', params: { date: f.date } })"
          >
            <div class="flex items-center gap-2 mb-1">
              <StatusDot status="failure" />
              <span class="font-mono text-xs text-foundry-white font-medium">{{ f.date }}</span>
              <span class="font-mono text-[0.6rem] text-foundry-red ml-auto">FAILURE</span>
            </div>
            <div class="font-mono text-[0.65rem] text-foundry-slag">
              Duration: {{ fmtDuration(f.metric.total_duration_s) }}
              <span v-if="f.metric.project"> | Project: {{ f.metric.project }}</span>
            </div>
          </div>
        </div>
      </FPanel>

      <!-- Rejected Nights (spec rejected all) -->
      <FPanel label="SPEC REJECTIONS" noPad>
        <EmptyState v-if="!rejectedNights.length" message="No nights where all trends were rejected" />
        <div v-else class="flex-1 overflow-auto">
          <div
            v-for="r in rejectedNights"
            :key="r.date"
            class="px-4 py-3 border-b border-foundry-border/30 hover:bg-foundry-red/5 cursor-pointer transition-colors"
            @click="router.push({ name: 'proving-ground', params: { date: r.date } })"
          >
            <div class="flex items-center gap-2 mb-1">
              <StatusDot status="rejected" />
              <span class="font-mono text-xs text-foundry-white font-medium">{{ r.date }}</span>
              <TagBadge :color="C.red">REJECT ALL</TagBadge>
            </div>
            <p v-if="r.reasoning" class="font-mono text-[0.65rem] text-foundry-slag leading-relaxed mt-1">
              {{ r.reasoning }}
            </p>
          </div>
        </div>
      </FPanel>
    </div>

    <!-- All Rejected Alternatives -->
    <FPanel label="REJECTED ALTERNATIVES BY NIGHT" noPad class="mt-3">
      <EmptyState v-if="!rejectedAlternatives.length" message="No rejected alternatives recorded" />
      <div v-else class="flex-1 overflow-auto max-h-[400px]">
        <table class="w-full border-collapse">
          <thead>
            <tr class="border-b border-foundry-border">
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">DATE</th>
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">TITLE</th>
              <th class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left">REASON</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(alt, i) in rejectedAlternatives" :key="i" class="border-b border-foundry-border/30">
              <td class="font-mono text-xs text-foundry-slag px-3 py-2 whitespace-nowrap">{{ alt.date }}</td>
              <td class="font-mono text-xs text-foundry-white/70 px-3 py-2">{{ alt.title }}</td>
              <td class="font-mono text-[0.65rem] text-foundry-slag px-3 py-2">{{ alt.rejection_reason }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </FPanel>
  </div>
</template>
