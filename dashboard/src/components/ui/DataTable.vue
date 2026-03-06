<script setup lang="ts">
defineProps<{
  columns: { key: string; label: string; align?: string; width?: string }[]
  rows: Record<string, unknown>[]
  clickable?: boolean
}>()

defineEmits<{
  rowClick: [row: Record<string, unknown>]
}>()
</script>

<template>
  <div class="overflow-auto flex-1">
    <table class="w-full border-collapse">
      <thead>
        <tr class="border-b border-foundry-border">
          <th
            v-for="col in columns"
            :key="col.key"
            class="font-mono text-[0.58rem] font-medium text-foundry-slag tracking-[0.1em] px-3 py-2 text-left"
            :class="{ 'text-right': col.align === 'right', 'text-center': col.align === 'center' }"
            :style="col.width ? { width: col.width } : {}"
          >
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, i) in rows"
          :key="i"
          class="border-b border-foundry-border/50 transition-colors"
          :class="clickable ? 'hover:bg-foundry-molten/5 cursor-pointer' : ''"
          @click="clickable && $emit('rowClick', row)"
        >
          <td
            v-for="col in columns"
            :key="col.key"
            class="font-mono text-xs text-foundry-white/80 px-3 py-2"
            :class="{ 'text-right': col.align === 'right', 'text-center': col.align === 'center' }"
          >
            <slot :name="col.key" :value="row[col.key]" :row="row">
              {{ row[col.key] ?? '—' }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
