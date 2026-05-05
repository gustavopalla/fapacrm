<template>
  <div class="flex space-x-6 h-full pb-4">
    <KanbanColumn 
      v-for="column in columns" 
      :key="column.id"
      :title="column.title"
      :status="column.id"
      :leads="leadsByStatus[column.id] || []"
      @move="handleMove"
      @select="selectedLead = $event"
    />
    
    <LeadDrawer :lead="selectedLead" @close="selectedLead = null" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useLeadStore } from '../stores/leads'
import KanbanColumn from './KanbanColumn.vue'
import LeadDrawer from './LeadDrawer.vue'

const leadStore = useLeadStore()
const selectedLead = ref<any>(null)

const columns = [
  { id: 'PROSPECCAO', title: 'Garimpo' },
  { id: 'CONTATO', title: '1º Contato' },
  { id: 'BRIEFING', title: 'Briefing' },
  { id: 'PROPOSTA', title: 'Proposta' },
  { id: 'FECHADO', title: 'Fechado' },
]

const leadsByStatus = computed(() => {
  return leadStore.leads.reduce((acc, lead) => {
    if (!acc[lead.status]) acc[lead.status] = []
    acc[lead.status].push(lead)
    return acc
  }, {} as Record<string, any[]>)
})

const handleMove = ({ leadId, newStatus }: { leadId: number, newStatus: string }) => {
  leadStore.updateLeadStatus(leadId, newStatus)
}

onMounted(() => {
  leadStore.fetchLeads()
})
</script>
