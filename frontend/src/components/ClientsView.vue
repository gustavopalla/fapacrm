<template>
  <div class="space-y-8 pb-20">
    <header class="flex justify-between items-end">
      <div>
        <h2 class="text-3xl font-heading font-bold text-white">Base de Clientes</h2>
        <p class="text-text-muted mt-2">Visualize e gerencie todos os negócios mapeados no seu ecossistema</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <!-- Search Bar -->
        <div class="relative group">
          <SearchIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-dim group-focus-within:text-primary transition-colors" />
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Pesquisar empresa ou cliente..." 
            class="bg-surface/50 border border-white/5 rounded-xl pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 w-80 transition-all"
          />
        </div>

        <!-- Niche Filter -->
        <select 
          v-model="filterNicho"
          class="bg-surface/50 border border-white/5 rounded-xl px-4 py-2.5 text-sm text-text-muted focus:outline-none focus:border-primary/50 transition-all appearance-none cursor-pointer"
        >
          <option value="ALL">Todos os Nichos</option>
          <option v-for="niche in settingsStore.niches" :key="niche.id" :value="niche.id">
            {{ niche.label }}
          </option>
        </select>

        <button @click="exportCSV" class="p-2.5 bg-white/5 hover:bg-white/10 rounded-xl border border-white/5 text-text-muted hover:text-white transition-all" title="Exportar CSV">
          <DownloadIcon class="w-5 h-5" />
        </button>
      </div>
    </header>

    <!-- Stats Overview -->
    <div class="grid grid-cols-4 gap-6">
      <div v-for="stat in stats" :key="stat.label" class="glass-card p-6">
        <span class="text-[10px] font-bold text-text-dim uppercase tracking-widest block mb-2">{{ stat.label }}</span>
        <div class="flex items-baseline space-x-2">
          <span class="text-2xl font-bold text-white">{{ stat.value }}</span>
          <span v-if="stat.sub" class="text-xs text-text-muted">{{ stat.sub }}</span>
        </div>
      </div>
    </div>

    <!-- Clients Table -->
    <div class="glass-card overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-white/5 text-[10px] font-bold text-text-dim uppercase tracking-widest border-b border-white/5">
            <th class="px-8 py-5">Empresa / Nicho</th>
            <th class="px-8 py-5">Responsável</th>
            <th class="px-8 py-5">Status Pipeline</th>
            <th class="px-8 py-5 text-right">Valor Estimado</th>
            <th class="px-8 py-5 text-center">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/5">
          <tr v-for="lead in filteredLeads" :key="lead.id" class="group hover:bg-primary/5 transition-colors cursor-pointer" @click="selectedLead = lead">
            <td class="px-8 py-5">
              <div class="flex items-center space-x-4">
                <div class="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-lg font-bold group-hover:bg-primary/20 group-hover:text-primary transition-all">
                  {{ lead.nome_empresa.charAt(0) }}
                </div>
                <div>
                  <div class="font-bold text-white group-hover:text-primary transition-colors">{{ lead.nome_empresa }}</div>
                  <div class="text-[10px] text-text-dim font-bold uppercase tracking-wider mt-0.5">{{ lead.nicho }}</div>
                </div>
              </div>
            </td>
            <td class="px-8 py-5 text-sm text-text-muted">
              {{ lead.nome_cliente }}
            </td>
            <td class="px-8 py-5">
              <span 
                class="px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest border"
                :class="statusColors[lead.status] || 'bg-white/5 border-white/10 text-text-muted'"
              >
                {{ lead.status }}
              </span>
            </td>
            <td class="px-8 py-5 text-right font-mono text-sm text-text-muted">
              {{ formatCurrency(lead.valor_estimado) }}
            </td>
            <td class="px-8 py-5">
              <div class="flex justify-center items-center space-x-2">
                <button class="p-2 hover:bg-white/10 rounded-lg text-text-dim hover:text-white transition-all">
                  <ExternalLinkIcon class="w-4 h-4" />
                </button>
                <a :href="`https://wa.me/?text=Olá ${lead.nome_cliente}, tudo bem?`" target="_blank" class="p-2 hover:bg-green-500/10 rounded-lg text-text-dim hover:text-green-400 transition-all" @click.stop>
                  <MessageCircleIcon class="w-4 h-4" />
                </a>
                <button @click.stop="handleDeleteRequest(lead)" class="p-2 hover:bg-red-500/10 rounded-lg text-text-dim hover:text-red-400 transition-all" title="Excluir Cliente">
                  <TrashIcon class="w-4 h-4" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="filteredLeads.length === 0" class="p-20 text-center">
        <div class="text-4xl mb-4">🔍</div>
        <h3 class="text-xl font-bold text-white">Nenhum cliente encontrado</h3>
        <p class="text-text-muted max-w-sm mx-auto mt-2">Tente ajustar seus filtros ou termos de pesquisa.</p>
      </div>
    </div>

    <!-- Reusing LeadDrawer for details -->
    <LeadDrawer :lead="selectedLead" @close="selectedLead = null" />

    <!-- Notifications Toast -->
    <div class="fixed bottom-6 right-6 z-50 flex flex-col gap-3">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        class="bg-surface border border-white/10 shadow-xl rounded-xl p-4 flex items-center gap-4 min-w-[300px] animate-fade-in-up"
      >
        <div class="flex-1">
          <p class="text-sm text-white font-medium">{{ notification.message }}</p>
        </div>
        <button 
          @click="undoDelete(notification)"
          class="text-xs font-bold bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded-lg transition-colors"
        >
          Desfazer
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { 
  Search as SearchIcon, 
  Download as DownloadIcon,
  ExternalLink as ExternalLinkIcon,
  MessageCircle as MessageCircleIcon,
  Trash as TrashIcon
} from 'lucide-vue-next'
import { useLeadStore } from '../stores/leads'
import { useSettingsStore } from '../stores/settings'
import LeadDrawer from './LeadDrawer.vue'

const leadStore = useLeadStore()
const settingsStore = useSettingsStore()
const searchQuery = ref('')
const filterNicho = ref('ALL')
const selectedLead = ref<any>(null)

const pendingDeletions = ref<number[]>([])
const notifications = ref<any[]>([])

const statusColors: Record<string, string> = {
  'PROSPECCAO': 'bg-blue-500/10 border-blue-500/20 text-blue-400',
  'CONTATO': 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400',
  'BRIEFING': 'bg-purple-500/10 border-purple-500/20 text-purple-400',
  'PROPOSTA': 'bg-orange-500/10 border-orange-500/20 text-orange-400',
  'FECHADO': 'bg-green-500/10 border-green-500/20 text-green-400',
  'PERDIDO': 'bg-red-500/10 border-red-500/20 text-red-400',
}

const filteredLeads = computed(() => {
  return leadStore.leads.filter(lead => {
    if (pendingDeletions.value.includes(lead.id)) return false;

    const matchesSearch = 
      lead.nome_empresa.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      lead.nome_cliente.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesNicho = filterNicho.value === 'ALL' || lead.nicho === filterNicho.value
    
    return matchesSearch && matchesNicho
  })
})

const stats = computed(() => [
  { label: 'Total de Empresas', value: leadStore.leads.length },
  { label: 'Nichos Ativos', value: new Set(leadStore.leads.map(l => l.nicho)).size },
  { label: 'Taxa de Fechamento', value: `${calculateWinRate()}%`, sub: 'Geral' },
  { label: 'Valor em Pipeline', value: formatCurrency(calculateTotalPipeline()), sub: 'Estimado' }
])

const calculateWinRate = () => {
  if (leadStore.leads.length === 0) return 0
  const won = leadStore.leads.filter(l => l.status === 'FECHADO').length
  return Math.round((won / leadStore.leads.length) * 100)
}

const calculateTotalPipeline = () => {
  return leadStore.leads.reduce((acc, l) => acc + Number(l.valor_estimado), 0)
}

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0
  }).format(value)
}

const exportCSV = () => {
  const headers = ['Empresa', 'Cliente', 'Nicho', 'Status', 'Valor Estimado', 'Tem Site']
  const rows = filteredLeads.value.map(l => [
    l.nome_empresa,
    l.nome_cliente,
    l.nicho,
    l.status,
    l.valor_estimado,
    l.tem_site ? 'Sim' : 'Não'
  ])
  
  const csvContent = "data:text/csv;charset=utf-8," 
    + headers.join(",") + "\n"
    + rows.map(e => e.join(",")).join("\n");
    
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "meus_clientes_crm.csv");
  document.body.appendChild(link);
  link.click();
}

const handleDeleteRequest = (lead: any) => {
  if (selectedLead.value?.id === lead.id) {
    selectedLead.value = null
  }
  
  pendingDeletions.value.push(lead.id)
  
  const notificationId = Date.now()
  const timerId = setTimeout(async () => {
    // Execute actual deletion
    await leadStore.deleteLead(lead.id)
    // Remove notification
    notifications.value = notifications.value.filter(n => n.id !== notificationId)
    // Remove from pending array
    pendingDeletions.value = pendingDeletions.value.filter(id => id !== lead.id)
  }, 5000)

  notifications.value.push({
    id: notificationId,
    leadId: lead.id,
    message: `Cliente ${lead.nome_empresa} removido.`,
    timerId
  })
}

const undoDelete = (notification: any) => {
  clearTimeout(notification.timerId)
  pendingDeletions.value = pendingDeletions.value.filter(id => id !== notification.leadId)
  notifications.value = notifications.value.filter(n => n.id !== notification.id)
}
</script>

<style scoped>
/* Custom style for search input focusing */
input:focus {
  background: rgba(22, 22, 26, 0.8);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out forwards;
}
</style>
