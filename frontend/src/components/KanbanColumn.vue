<template>
  <div class="flex-shrink-0 w-80 flex flex-col bg-surface/30 backdrop-blur-md rounded-2xl border border-white/5 shadow-xl h-full">
    <!-- Header da Coluna -->
    <div class="p-5 flex items-center justify-between border-b border-white/5">
      <div class="flex items-center space-x-2.5">
        <div class="w-2 h-2 rounded-full bg-primary shadow-[0_0_8px_rgba(124,58,237,0.5)]"></div>
        <h3 class="font-heading font-semibold text-sm text-white/90 uppercase tracking-widest">{{ title }}</h3>
      </div>
      <span class="bg-white/5 px-2.5 py-1 rounded-lg text-[10px] font-mono text-text-muted border border-white/5">
        {{ leads.length }}
      </span>
    </div>

    <!-- Lista de Cards -->
    <draggable
      class="flex-1 p-4 space-y-4 overflow-y-auto min-h-[150px] scrollbar-hide custom-drag-area"
      :list="leads"
      group="leads"
      item-key="id"
      ghost-class="ghost-card"
      drag-class="drag-card"
      @change="onDragChange"
    >
      <template #item="{ element }">
        <LeadCard :lead="element" @click="$emit('select', element)" />
      </template>
    </draggable>
  </div>
</template>

<script setup lang="ts">
import draggable from 'vuedraggable'
import LeadCard from './LeadCard.vue'

const props = defineProps<{
  title: string
  status: string
  leads: any[]
}>()

const emit = defineEmits(['move', 'select'])

const onDragChange = (evt: any) => {
  if (evt.added) {
    emit('move', { leadId: evt.added.element.id, newStatus: props.status })
  }
}
</script>

<style scoped>
.ghost-card {
  opacity: 0.3;
  background: var(--color-primary);
  border: 2px dashed var(--color-primary);
}

.drag-card {
  transform: rotate(2deg);
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.custom-drag-area {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.custom-drag-area::-webkit-scrollbar {
  display: none;
}
</style>
