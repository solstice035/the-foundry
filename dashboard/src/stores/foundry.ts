import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { DashboardData, MetricsEntry, NightData } from '@/types'

export const useFoundryStore = defineStore('foundry', () => {
  const raw = ref<DashboardData | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)
  const lastFetched = ref<Date | null>(null)
  let pollTimer: ReturnType<typeof setInterval> | null = null

  async function fetchData() {
    try {
      const res = await fetch('/dashboard-data.json')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      raw.value = await res.json()
      error.value = null
      lastFetched.value = new Date()
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  }

  function startPolling() {
    stopPolling()
    const tick = () => {
      const h = new Date().getHours()
      const m = new Date().getMinutes()
      const inBriefingWindow = (h === 7 && m >= 50) || h === 8 && m <= 30
      const interval = inBriefingWindow ? 60_000 : 300_000
      pollTimer = setTimeout(() => {
        fetchData().then(tick)
      }, interval)
    }
    tick()
  }

  function stopPolling() {
    if (pollTimer) {
      clearTimeout(pollTimer)
      pollTimer = null
    }
  }

  const nightsSorted = computed(() => {
    if (!raw.value) return []
    return Object.keys(raw.value.nights).sort().reverse()
  })

  const metrics = computed(() => {
    if (!raw.value) return null
    const m = raw.value.metrics
    const successes = m.filter(e => e.type === 'success')
    const failures = m.filter(e => e.type === 'failure')
    const totalCost = successes.reduce((s, e) => s + (e.cost_usd || 0), 0)
    const totalDuration = successes.reduce((s, e) => s + (e.total_duration_s || 0), 0)

    // Streak: count consecutive successes from most recent
    const sorted = [...m].sort((a, b) => b.date.localeCompare(a.date))
    let streak = 0
    for (const e of sorted) {
      if (e.type === 'success') streak++
      else break
    }

    return {
      total: m.length,
      successCount: successes.length,
      failureCount: failures.length,
      successRate: m.length > 0 ? (successes.length / m.length) * 100 : 0,
      avgCost: successes.length > 0 ? totalCost / successes.length : 0,
      totalCost,
      avgDuration: successes.length > 0 ? totalDuration / successes.length : 0,
      streak,
    }
  })

  const buildList = computed(() => {
    if (!raw.value) return []
    return nightsSorted.value
      .map(date => {
        const night = raw.value!.nights[date]
        const metric = raw.value!.metrics.find(m => m.date === date)
        return { date, night, metric }
      })
      .filter(b => b.night.build)
  })

  function getNight(date: string): NightData | null {
    return raw.value?.nights[date] ?? null
  }

  function getMetric(date: string): MetricsEntry | undefined {
    return raw.value?.metrics.find(m => m.date === date)
  }

  return {
    raw, loading, error, lastFetched,
    nightsSorted, metrics, buildList,
    fetchData, startPolling, stopPolling,
    getNight, getMetric,
  }
})
