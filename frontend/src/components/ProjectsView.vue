<template>
  <div class="space-y-6 lg:space-y-10 pb-24 lg:pb-20">
    <header class="space-y-4">
      <div>
        <h2 class="text-2xl lg:text-3xl font-heading font-bold text-white">Gestão de Recorrência</h2>
        <p class="text-text-muted mt-1 lg:mt-2 text-sm lg:text-base">Acompanhe seus projetos ativos e receita mensal recorrente (MRR)</p>
      </div>
      
      <div class="flex gap-3 lg:gap-6">
        <div class="glass-card px-4 lg:px-8 py-3 lg:py-4 bg-primary/10 border-primary/20 flex-1 sm:flex-none">
          <span class="text-[10px] font-bold text-primary uppercase tracking-widest block mb-1">Total MRR</span>
          <span class="text-xl lg:text-2xl font-bold text-white">{{ formatCurrency(totalMRR) }}</span>
        </div>
        <div class="glass-card px-4 lg:px-8 py-3 lg:py-4 bg-secondary/10 border-secondary/20 flex-1 sm:flex-none">
          <span class="text-[10px] font-bold text-secondary uppercase tracking-widest block mb-1">Projetos Ativos</span>
          <span class="text-xl lg:text-2xl font-bold text-white">{{ activeProjects.length }}</span>
        </div>
      </div>
    </header>

    <div class="grid grid-cols-1 gap-4">
      <div v-if="activeProjects.length === 0" class="glass-card p-20 text-center space-y-4">
        <div class="w-20 h-20 bg-white/5 rounded-full flex items-center justify-center mx-auto text-4xl">💎</div>
        <h3 class="text-xl font-bold">Nenhum projeto recorrente ainda</h3>
        <p class="text-text-muted max-w-sm mx-auto">Feche um lead como "Ganhado" para transformá-lo em um projeto e começar a gerenciar sua recorrência.</p>
      </div>

      <div v-for="lead in activeProjects" :key="lead.id" class="glass-card p-4 lg:p-8 flex flex-col lg:flex-row lg:items-center justify-between group gap-4">
        <div class="flex items-center space-x-4 lg:space-x-6">
          <div class="w-12 h-12 lg:w-16 lg:h-16 bg-gradient-to-tr from-primary to-secondary rounded-2xl flex items-center justify-center text-xl lg:text-2xl font-bold shadow-glow group-hover:scale-105 transition-transform shrink-0">
            {{ lead.nome_empresa.charAt(0) }}
          </div>
          <div class="min-w-0">
            <h3 class="text-lg lg:text-xl font-bold text-white mb-1 truncate">{{ lead.nome_empresa }}</h3>
            <div class="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4 text-sm text-text-muted">
              <span class="flex items-center"><UserIcon class="w-4 h-4 mr-1.5" /> {{ lead.nome_cliente }}</span>
              <span class="flex items-center"><CalendarIcon class="w-4 h-4 mr-1.5" /> Ativo desde {{ formatDate(lead.ultima_interacao) }}</span>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between lg:justify-end gap-4 lg:gap-12 pl-16 lg:pl-0">
          <div class="text-right">
            <span class="text-[10px] font-bold text-text-dim uppercase tracking-widest block mb-1">Mensalidade</span>
            <span class="text-xl font-bold text-primary">{{ formatCurrency(lead.project?.valor_recorrente || 0) }}</span>
          </div>
          
          <div class="flex space-x-2">
            <button class="p-3 bg-white/5 hover:bg-white/10 rounded-xl transition-all border border-white/5 text-text-muted hover:text-white" title="Ver Detalhes">
              <ExternalLinkIcon class="w-5 h-5" />
            </button>
            <button class="p-3 bg-white/5 hover:bg-white/10 rounded-xl transition-all border border-white/5 text-text-muted hover:text-white" title="Configurar Cobrança">
              <CreditCardIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Dica Estratégica -->
    <div class="bg-primary/10 border border-primary/20 rounded-2xl lg:rounded-3xl p-6 lg:p-8 flex flex-col sm:flex-row gap-4 lg:gap-6 items-start sm:items-center max-w-3xl">
      <div class="w-16 h-16 rounded-2xl bg-primary/20 flex items-center justify-center text-3xl shrink-0">🚀</div>
      <div>
        <h3 class="text-xl font-bold mb-2">Dica do Guia</h3>
        <p class="text-text-muted text-sm leading-relaxed">
          "Transforme cada site entregue em uma fonte de renda passiva. O plano de manutenção (hospedagem + suporte) é o que vai te dar liberdade a longo prazo. 10 clientes pagando R$200/mês já garantem seus custos fixos."
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { 
  User as UserIcon, 
  Calendar as CalendarIcon, 
  ExternalLink as ExternalLinkIcon,
  CreditCard as CreditCardIcon
} from 'lucide-vue-next'
import { useLeadStore } from '../stores/leads'

const leadStore = useLeadStore()

const activeProjects = computed(() => {
  return leadStore.leads.filter(l => l.status === 'FECHADO')
})

const totalMRR = computed(() => {
  return activeProjects.value.reduce((acc, lead) => acc + (Number(lead.project?.valor_recorrente) || 0), 0)
})

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0
  }).format(value)
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}
</script>
