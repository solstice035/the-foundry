<script setup lang="ts">
import { ref, computed } from 'vue'
import { useFoundryStore } from '@/stores/foundry'
import { useFormatters } from '@/composables/useFormatters'
import FPanel from '@/components/ui/FPanel.vue'
import TagBadge from '@/components/ui/TagBadge.vue'
import CopyButton from '@/components/ui/CopyButton.vue'
import StatBlock from '@/components/ui/StatBlock.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import { C } from '@/design/tokens'

const store = useFoundryStore()
const { fmtDate } = useFormatters()

const activeTab = ref<'x' | 'reddit'>('x')

const queue = computed(() => store.raw?.social.content_queue)
const voicePatterns = computed(() => store.raw?.social.voice_patterns)

const pending = computed(() => queue.value?.pending ?? [])
const approved = computed(() => queue.value?.approved ?? [])
const posted = computed(() => queue.value?.posted ?? [])

const stats = computed(() => ({
  pending: pending.value.length,
  approved: approved.value.length,
  posted: posted.value.length,
  total: (pending.value.length + approved.value.length + posted.value.length),
}))

function getTweets(draft: typeof pending.value[0]): string[] {
  return draft.platforms?.x?.tweets ?? []
}

function getReddit(draft: typeof pending.value[0]) {
  return draft.platforms?.reddit ?? null
}
</script>

<template>
  <div class="h-full overflow-auto p-4">
    <div class="flex items-end justify-between mb-4">
      <div>
        <div class="font-mono text-[0.6rem] text-foundry-molten tracking-[0.18em] mb-1">AMPLIFICATION</div>
        <h2 class="font-display text-2xl text-foundry-white tracking-wide">SOCIAL QUEUE</h2>
      </div>
      <div class="flex gap-4">
        <StatBlock :value="stats.pending" label="PENDING" :color="C.molten" size="sm" />
        <StatBlock :value="stats.approved" label="APPROVED" :color="C.green" size="sm" />
        <StatBlock :value="stats.posted" label="POSTED" :color="C.blue" size="sm" />
      </div>
    </div>

    <!-- Platform tabs -->
    <div class="flex gap-0.5 mb-4">
      <button
        v-for="tab in (['x', 'reddit'] as const)"
        :key="tab"
        @click="activeTab = tab"
        class="font-mono text-[0.65rem] font-medium px-4 py-1.5 border border-foundry-border cursor-pointer transition-colors tracking-wider"
        :class="activeTab === tab
          ? 'bg-foundry-molten/10 text-foundry-molten border-foundry-molten/30'
          : 'bg-transparent text-foundry-slag hover:text-foundry-white'"
      >
        {{ tab === 'x' ? 'X / TWITTER' : 'REDDIT' }}
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-[1fr_280px] gap-3">
      <!-- Draft cards -->
      <div class="space-y-3">
        <EmptyState v-if="!pending.length" message="No pending drafts in the queue" />

        <div
          v-for="draft in pending"
          :key="draft.id"
          class="bg-foundry-panel border border-foundry-border"
        >
          <!-- Draft header -->
          <div class="px-4 py-2 border-b border-foundry-border flex items-center justify-between bg-foundry-border/20">
            <div class="flex items-center gap-2">
              <span class="font-mono text-[0.58rem] text-foundry-slag tracking-wide">{{ draft.source_build }}</span>
              <TagBadge :color="C.molten">{{ draft.content_type }}</TagBadge>
              <TagBadge :color="draft.priority <= 1 ? C.green : C.slag">P{{ draft.priority }}</TagBadge>
            </div>
            <TagBadge :color="C.brass">{{ draft.estimated_engagement }}</TagBadge>
          </div>

          <!-- X content -->
          <div v-if="activeTab === 'x'" class="p-4">
            <div v-if="getTweets(draft).length" class="space-y-3">
              <div
                v-for="(tweet, i) in getTweets(draft)"
                :key="i"
                class="flex gap-3"
              >
                <div class="shrink-0 font-mono text-[0.55rem] text-foundry-slag-dim mt-0.5 w-4 text-right">{{ i + 1 }}</div>
                <div class="flex-1">
                  <p class="font-body text-sm text-foundry-white/80 leading-relaxed">{{ tweet }}</p>
                  <div class="flex justify-between items-center mt-1.5">
                    <span class="font-mono text-[0.55rem] text-foundry-slag">{{ tweet.length }}/280</span>
                    <CopyButton :text="tweet" />
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="font-mono text-xs text-foundry-slag">No X content for this draft</div>

            <div v-if="draft.platforms?.x?.best_posting_time" class="mt-3 pt-2 border-t border-foundry-border/30">
              <span class="font-mono text-[0.55rem] text-foundry-slag">BEST TIME: </span>
              <span class="font-mono text-[0.6rem] text-foundry-brass">{{ draft.platforms.x.best_posting_time }}</span>
            </div>
          </div>

          <!-- Reddit content -->
          <div v-if="activeTab === 'reddit'" class="p-4">
            <div v-if="getReddit(draft)">
              <div class="mb-2">
                <TagBadge :color="C.blue">{{ getReddit(draft)!.subreddit }}</TagBadge>
              </div>
              <div class="font-mono text-sm text-foundry-white font-medium mb-2">
                {{ getReddit(draft)!.title }}
              </div>
              <p class="font-body text-xs text-foundry-white/60 leading-relaxed whitespace-pre-wrap max-h-40 overflow-auto">
                {{ getReddit(draft)!.body }}
              </p>
              <div class="flex justify-end mt-2">
                <CopyButton :text="`${getReddit(draft)!.title}\n\n${getReddit(draft)!.body}`" />
              </div>
            </div>
            <div v-else class="font-mono text-xs text-foundry-slag">No Reddit content for this draft</div>
          </div>
        </div>
      </div>

      <!-- Sidebar: Voice patterns -->
      <div class="flex flex-col gap-3">
        <FPanel label="QUEUE STATS">
          <div class="space-y-1.5">
            <div v-for="row in [
              { l: 'PENDING', v: stats.pending, c: C.molten },
              { l: 'APPROVED', v: stats.approved, c: C.green },
              { l: 'POSTED', v: stats.posted, c: C.blue },
            ]" :key="row.l" class="flex justify-between">
              <span class="font-mono text-[0.6rem] text-foundry-slag">{{ row.l }}</span>
              <span class="font-mono text-xs font-semibold" :style="{ color: row.c }">{{ row.v }}</span>
            </div>
          </div>
        </FPanel>

        <FPanel v-if="voicePatterns?.patterns" label="VOICE PATTERNS">
          <div class="space-y-2">
            <div v-for="(value, key) in voicePatterns.patterns" :key="String(key)">
              <div class="font-mono text-[0.55rem] text-foundry-slag tracking-wide mb-0.5">{{ String(key).toUpperCase().replace(/_/g, ' ') }}</div>
              <div v-if="Array.isArray(value)" class="flex gap-1 flex-wrap">
                <TagBadge v-for="(v, i) in (value as string[]).slice(0, 5)" :key="i" :color="C.brass">{{ v }}</TagBadge>
              </div>
              <div v-else class="font-mono text-[0.6rem] text-foundry-white/60">
                {{ typeof value === 'object' ? JSON.stringify(value).slice(0, 100) : value }}
              </div>
            </div>
          </div>
        </FPanel>
      </div>
    </div>
  </div>
</template>
