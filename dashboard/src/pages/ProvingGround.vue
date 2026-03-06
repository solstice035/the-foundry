<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFoundryStore } from '@/stores/foundry'
import { useFormatters } from '@/composables/useFormatters'
import FPanel from '@/components/ui/FPanel.vue'
import StatusDot from '@/components/ui/StatusDot.vue'
import StatBlock from '@/components/ui/StatBlock.vue'
import GaugeBar from '@/components/ui/GaugeBar.vue'
import PipelineTimeline from '@/components/ui/PipelineTimeline.vue'
import TagBadge from '@/components/ui/TagBadge.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { C } from '@/design/tokens'

const route = useRoute()
const router = useRouter()
const store = useFoundryStore()
const { fmtDate, fmtDuration, fmtCost } = useFormatters()

const date = computed(() => route.params.date as string)
const night = computed(() => store.getNight(date.value))
const metric = computed(() => store.getMetric(date.value))

const status = computed(() => {
  if (metric.value?.type === 'success') return 'forged'
  if (metric.value?.type === 'failure') return 'rejected'
  return 'idle'
})

const specFeatures = computed(() => night.value?.spec?.spec?.features ?? [])

const techStack = computed(() => {
  const ts = night.value?.build?.tech_stack
  if (!ts) return []
  if (typeof ts === 'object') return Object.entries(ts).map(([k, v]) => `${k}: ${v}`)
  return [String(ts)]
})
</script>

<template>
  <div class="h-full overflow-auto p-4">
    <div class="flex items-center gap-3 mb-4">
      <button @click="router.back()" class="font-mono text-xs text-foundry-slag hover:text-foundry-molten cursor-pointer">&larr; BACK</button>
      <StatusDot :status="status" :size="8" />
      <div>
        <div class="font-mono text-[0.6rem] text-foundry-molten tracking-[0.18em]">PROVING GROUND</div>
        <h2 class="font-display text-2xl text-foundry-white tracking-wide">
          {{ night?.build?.project_name ?? date }}
        </h2>
      </div>
      <span class="font-mono text-xs text-foundry-slag ml-2">{{ fmtDate(date, 'long') }}</span>
    </div>

    <EmptyState v-if="!night" message="No data for this night" />

    <template v-else>
      <div class="grid grid-cols-1 lg:grid-cols-[1fr_340px] gap-3">
        <!-- Left Column -->
        <div class="flex flex-col gap-3">
          <FPanel label="OVERVIEW">
            <div class="flex gap-5 flex-wrap mb-3">
              <StatBlock v-if="metric" :value="fmtDuration(metric.total_duration_s)" label="FORGE TIME" />
              <StatBlock v-if="metric" :value="fmtCost(metric.cost_usd)" label="COST" :color="C.brass" />
              <StatBlock v-if="metric?.engagement_score" :value="metric.engagement_score.toFixed(1)" label="ENGAGEMENT" :color="C.blue" />
              <StatBlock v-if="metric?.buildability_score" :value="metric.buildability_score.toFixed(1)" label="BUILDABILITY" :color="C.green" />
            </div>
            <p v-if="night.build?.description" class="font-body text-sm text-foundry-white/70 leading-relaxed mb-3">{{ night.build.description }}</p>
            <p v-else-if="night.spec?.reasoning" class="font-body text-sm text-foundry-white/70 leading-relaxed mb-3">{{ night.spec.reasoning }}</p>
            <div v-if="techStack.length" class="flex gap-1 flex-wrap">
              <TagBadge v-for="t in techStack" :key="t">{{ t }}</TagBadge>
            </div>
          </FPanel>

          <FPanel v-if="night.build?.features_implemented?.length" label="FEATURES IMPLEMENTED">
            <div class="space-y-1">
              <div v-for="(feat, i) in night.build.features_implemented" :key="i" class="flex gap-2 py-1 border-b border-foundry-border/30 last:border-0">
                <span class="text-foundry-green text-xs shrink-0">&#10003;</span>
                <span class="font-mono text-xs text-foundry-white/70">{{ feat }}</span>
              </div>
            </div>
          </FPanel>

          <FPanel v-if="specFeatures.length" label="BLUEPRINT SPEC">
            <div class="space-y-1">
              <div v-for="(feat, i) in specFeatures" :key="i" class="flex gap-2 py-1 border-b border-foundry-border/30 last:border-0">
                <span class="text-foundry-brass text-xs shrink-0">&#9670;</span>
                <span class="font-mono text-xs text-foundry-white/60">{{ feat }}</span>
              </div>
            </div>
          </FPanel>

          <FPanel v-if="night.spec?.rejected_alternatives?.length" label="REJECTED ALTERNATIVES">
            <div class="space-y-2">
              <div v-for="alt in night.spec.rejected_alternatives" :key="alt.id" class="border-l-2 border-foundry-red/40 pl-3 py-1">
                <div class="font-mono text-xs text-foundry-white/80 font-medium">{{ alt.title }}</div>
                <div class="font-mono text-[0.65rem] text-foundry-slag mt-0.5">{{ alt.rejection_reason }}</div>
              </div>
            </div>
          </FPanel>

          <FPanel v-if="night.build?.notes" label="SMITH'S NOTES">
            <p class="font-mono text-xs text-foundry-white/60 leading-relaxed whitespace-pre-wrap">{{ night.build.notes }}</p>
          </FPanel>
        </div>

        <!-- Right Column -->
        <div class="flex flex-col gap-3">
          <FPanel v-if="night.state" label="PIPELINE">
            <PipelineTimeline :state="night.state" />
            <div class="mt-3 space-y-1.5">
              <div v-for="(stage, name) in night.state.stages" :key="String(name)" class="flex justify-between items-center">
                <span class="font-mono text-[0.6rem] text-foundry-slag tracking-wide">{{ String(name).toUpperCase() }}</span>
                <span class="font-mono text-[0.58rem]" :class="stage.status === 'complete' ? 'text-foundry-green' : stage.status === 'failed' ? 'text-foundry-red' : 'text-foundry-slag-dim'">{{ stage.status }}</span>
              </div>
            </div>
          </FPanel>

          <FPanel v-if="night.build?.build" label="BUILD DETAILS">
            <div class="space-y-1.5">
              <div class="flex justify-between">
                <span class="font-mono text-[0.6rem] text-foundry-slag">TOOL</span>
                <span class="font-mono text-xs text-foundry-white/80">{{ night.build.build.tool }}</span>
              </div>
              <div class="flex justify-between">
                <span class="font-mono text-[0.6rem] text-foundry-slag">MODEL</span>
                <span class="font-mono text-xs text-foundry-white/80">{{ night.build.build.model }}</span>
              </div>
              <div class="flex justify-between">
                <span class="font-mono text-[0.6rem] text-foundry-slag">DURATION</span>
                <span class="font-mono text-xs text-foundry-molten">{{ fmtDuration(night.build.build.duration_seconds) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="font-mono text-[0.6rem] text-foundry-slag">COST</span>
                <span class="font-mono text-xs text-foundry-brass">{{ night.build.build.cost }}</span>
              </div>
              <div v-if="night.build.build.commits" class="flex justify-between">
                <span class="font-mono text-[0.6rem] text-foundry-slag">COMMITS</span>
                <span class="font-mono text-xs text-foundry-white/80">{{ night.build.build.commits }}</span>
              </div>
            </div>
          </FPanel>

          <FPanel v-if="night.build?.tests" label="TEST RESULTS">
            <GaugeBar label="PASSED" :value="night.build.tests.passed ?? 0" :max="night.build.tests.total ?? 0" :color="C.green" />
          </FPanel>

          <FPanel v-if="night.trends_top?.length" label="ORE SOURCE">
            <div class="space-y-1">
              <div v-for="(trend, i) in night.trends_top.slice(0, 5)" :key="i" class="flex gap-2 items-start py-1 border-b border-foundry-border/30 last:border-0">
                <TagBadge v-if="trend.source" :color="C.blue" class="shrink-0">{{ trend.source }}</TagBadge>
                <span class="font-mono text-[0.65rem] text-foundry-white/70 flex-1">{{ trend.title }}</span>
                <span v-if="trend.final_score" class="font-mono text-[0.6rem] text-foundry-molten shrink-0">{{ trend.final_score.toFixed(1) }}</span>
              </div>
            </div>
          </FPanel>

          <FPanel v-if="night.build?.repo_url || metric?.repo_url" label="REPOSITORY">
            <a :href="night.build?.repo_url ?? metric?.repo_url" target="_blank" class="font-mono text-xs text-foundry-blue hover:text-foundry-molten transition-colors break-all">
              {{ night.build?.repo_url ?? metric?.repo_url }}
            </a>
          </FPanel>
        </div>
      </div>
    </template>
  </div>
</template>
