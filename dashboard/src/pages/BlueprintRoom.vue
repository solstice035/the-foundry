<script setup lang="ts">
import { computed, ref } from 'vue'
import { useFoundryStore } from '@/stores/foundry'
import { useFormatters } from '@/composables/useFormatters'
import FPanel from '@/components/ui/FPanel.vue'
import TagBadge from '@/components/ui/TagBadge.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { C } from '@/design/tokens'

const store = useFoundryStore()
const { fmtDate } = useFormatters()

const expanded = ref<string | null>(null)

const specs = computed(() =>
  store.nightsSorted
    .map(date => {
      const night = store.getNight(date)
      if (!night?.spec) return null
      return {
        date,
        decision: night.spec.decision,
        title: night.spec.selected_trend_title ?? night.build?.project_name ?? night.spec.spec?.project_name ?? date,
        reasoning: night.spec.reasoning,
        features: night.spec.spec?.features ?? [],
        stack: night.spec.spec?.stack,
        rejected: night.spec.rejected_alternatives ?? [],
      }
    })
    .filter(Boolean) as {
      date: string; decision: string; title: string; reasoning?: string;
      features: string[]; stack?: string[] | Record<string, string>;
      rejected: { id: string; title: string; rejection_reason: string }[]
    }[]
)

function toggle(date: string) {
  expanded.value = expanded.value === date ? null : date
}

function stackTags(stack: string[] | Record<string, string> | undefined): string[] {
  if (!stack) return []
  if (Array.isArray(stack)) return stack
  return Object.values(stack)
}
</script>

<template>
  <div class="h-full overflow-auto p-4">
    <div class="mb-4">
      <div class="font-mono text-[0.6rem] text-foundry-molten tracking-[0.18em] mb-1">SPECIFICATIONS</div>
      <h2 class="font-display text-2xl text-foundry-white tracking-wide">BLUEPRINT ROOM</h2>
    </div>

    <EmptyState v-if="!specs.length" message="No specifications recorded" />

    <div v-else class="space-y-2">
      <div
        v-for="spec in specs"
        :key="spec.date"
        class="bg-foundry-panel border border-foundry-border"
      >
        <!-- Header (always visible) -->
        <button
          @click="toggle(spec.date)"
          class="w-full text-left px-4 py-3 flex items-center gap-3 cursor-pointer hover:bg-foundry-border/10 transition-colors"
        >
          <span class="font-mono text-[0.6rem] text-foundry-slag min-w-[80px]">{{ spec.date }}</span>
          <span class="font-mono text-sm text-foundry-white font-semibold flex-1">{{ spec.title }}</span>
          <TagBadge
            :color="spec.decision === 'approved' ? C.green : spec.decision === 'reject_all' ? C.red : C.slag"
          >
            {{ spec.decision }}
          </TagBadge>
          <span class="font-mono text-xs text-foundry-slag transition-transform" :class="expanded === spec.date ? 'rotate-90' : ''">
            &#9654;
          </span>
        </button>

        <!-- Expanded detail -->
        <div v-if="expanded === spec.date" class="border-t border-foundry-border px-4 py-3 space-y-3">
          <!-- Reasoning -->
          <div v-if="spec.reasoning">
            <div class="font-mono text-[0.55rem] text-foundry-slag tracking-[0.1em] mb-1">REASONING</div>
            <p class="font-body text-xs text-foundry-white/60 leading-relaxed">{{ spec.reasoning }}</p>
          </div>

          <!-- Features -->
          <div v-if="spec.features.length">
            <div class="font-mono text-[0.55rem] text-foundry-slag tracking-[0.1em] mb-1">PLANNED FEATURES</div>
            <div class="space-y-0.5">
              <div v-for="(f, i) in spec.features" :key="i" class="flex gap-2">
                <span class="text-foundry-brass text-xs shrink-0">&#9670;</span>
                <span class="font-mono text-xs text-foundry-white/60">{{ f }}</span>
              </div>
            </div>
          </div>

          <!-- Stack -->
          <div v-if="stackTags(spec.stack).length">
            <div class="font-mono text-[0.55rem] text-foundry-slag tracking-[0.1em] mb-1">STACK</div>
            <div class="flex gap-1 flex-wrap">
              <TagBadge v-for="t in stackTags(spec.stack)" :key="t" :color="C.blue">{{ t }}</TagBadge>
            </div>
          </div>

          <!-- Rejected alternatives -->
          <div v-if="spec.rejected.length">
            <div class="font-mono text-[0.55rem] text-foundry-slag tracking-[0.1em] mb-1">REJECTED ALTERNATIVES ({{ spec.rejected.length }})</div>
            <div class="space-y-1.5">
              <div v-for="alt in spec.rejected" :key="alt.id" class="border-l-2 border-foundry-red/30 pl-3">
                <div class="font-mono text-xs text-foundry-white/70">{{ alt.title }}</div>
                <div class="font-mono text-[0.6rem] text-foundry-slag mt-0.5">{{ alt.rejection_reason }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
