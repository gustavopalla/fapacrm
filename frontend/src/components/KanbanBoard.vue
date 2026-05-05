<template>
  <div class="flex space-x-4 lg:space-x-6 h-full pb-20 lg:pb-4 overflow-x-auto snap-x snap-mandatory lg:snap-none scrollbar-hide -mx-4 px-4 lg:mx-0 lg:px-0">
    <KanbanColumn 
      v-for="column in columns" 
      :key="column.id"
      :title="column.title"
      :status="column.id"
      :leads="leadsByStatus[column.id] || []"
      @move="handleMove"
      @select="selectedLead = $event"
      class="snap-start"
    />
    
    <LeadDrawer :lead="selectedLead" @close="selectedLead = null" />

    <!-- Modal para Motivo de Espera -->
    <Teleport to="body">
      <div v-if="showReasonModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-background/80 backdrop-blur-sm" @click="cancelMove"></div>
        
        <div class="relative bg-surface/90 backdrop-blur-2xl rounded-3xl border border-white/10 shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-300">
          <header class="p-6 border-b border-white/5 flex justify-between items-center bg-gradient-to-r from-primary/10 to-transparent">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center">
                <ClockIcon class="w-6 h-6 text-primary" />
              </div>
              <div>
                <h3 class="text-xl font-heading font-bold text-white">Motivo da Espera</h3>
                <p class="text-xs text-text-muted mt-1">Por que este lead está aguardando?</p>
              </div>
            </div>
            <button @click="cancelMove" class="p-2 hover:bg-white/5 rounded-xl transition-colors">
              <XIcon class="w-5 h-5 text-text-muted" />
            </button>
          </header>
          
          <div class="p-6 space-y-4">
            <textarea 
              v-model="motivoText"
              rows="4"
              class="w-full bg-background border border-white/5 rounded-2xl px-4 py-3 text-white focus:border-primary/50 outline-none transition-all placeholder:text-text-dim/50 resize-none"
              placeholder="Ex: Aguardando aprovação do orçamento pelo sócio majoritário..."
              autofocus
            ></textarea>
            
            <div class="flex space-x-3 mt-2">
              <button 
                @click="cancelMove"
                class="flex-1 px-6 py-3 rounded-xl border border-white/5 text-text-muted font-bold hover:bg-white/5 transition-all"
              >
                Cancelar
              </button>
              <button 
                @click="confirmMove"
                :disabled="!motivoText.trim()"
                class="flex-1 px-6 py-3 rounded-xl bg-primary text-white font-bold shadow-lg shadow-primary/20 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:hover:scale-100"
              >
                Confirmar
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useLeadStore } from '../stores/leads'
import { Clock as ClockIcon, X as XIcon } from 'lucide-vue-next'
import KanbanColumn from './KanbanColumn.vue'
import LeadDrawer from './LeadDrawer.vue'

const leadStore = useLeadStore()
const selectedLead = ref<any>(null)
const showReasonModal = ref(false)
const motivoText = ref('')
const pendingMove = ref<{ leadId: number, newStatus: string } | null>(null)

const columns = [
  { id: 'PROSPECCAO', title: 'Garimpo' },
  { id: 'CONTATO', title: '1º Contato' },
  { id: 'BRIEFING', title: 'Briefing' },
  { id: 'PROPOSTA', title: 'Proposta' },
  { id: 'AGUARDANDO', title: 'Aguardando Cliente' },
  { id: 'FECHADO', title: 'Fechado' },
]

const leadsByStatus = computed(() => {
  return leadStore.leads.reduce((acc, lead) => {
    if (!acc[lead.status]) acc[lead.status] = []
    acc[lead.status].push(lead)
    return acc
  }, {} as Record<string, any[]>)
})

const handleMove = async ({ leadId, newStatus }: { leadId: number, newStatus: string }) => {
  if (newStatus === 'AGUARDANDO') {
    pendingMove.value = { leadId, newStatus }
    motivoText.value = ''
    showReasonModal.value = true
  } else {
    await leadStore.updateLeadStatus(leadId, newStatus)
  }
}

const confirmMove = async () => {
  if (pendingMove.value && motivoText.value.trim()) {
    await leadStore.updateLead(pendingMove.value.leadId, { 
      status: pendingMove.value.newStatus, 
      motivo_espera: motivoText.value 
    })
    showReasonModal.value = false
    pendingMove.value = null
    motivoText.value = ''
  }
}

const cancelMove = () => {
  showReasonModal.value = false
  pendingMove.value = null
  motivoText.value = ''
  // Recarrega para voltar o card se o drag tiver sido "concluído" no DOM mas não no banco
  leadStore.fetchLeads()
}

onMounted(() => {
  leadStore.fetchLeads()
})
</script>
