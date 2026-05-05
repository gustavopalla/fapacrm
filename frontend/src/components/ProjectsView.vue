<template>
  <div class="space-y-10 pb-20">
    <header class="flex justify-between items-end">
      <div>
        <h2 class="text-3xl font-heading font-bold text-white">Gestão de Recorrência</h2>
        <p class="text-text-muted mt-2">Acompanhe seus projetos ativos e receita mensal recorrente (MRR)</p>
      </div>
      
      <div class="flex gap-6">
        <div class="glass-card px-8 py-4 bg-primary/10 border-primary/20">
          <span class="text-[10px] font-bold text-primary uppercase tracking-widest block mb-1">Total MRR</span>
          <span class="text-2xl font-bold text-white">{{ formatCurrency(totalMRR) }}</span>
        </div>
        <div class="glass-card px-8 py-4 bg-secondary/10 border-secondary/20">
          <span class="text-[10px] font-bold text-secondary uppercase tracking-widest block mb-1">Projetos Ativos</span>
          <span class="text-2xl font-bold text-white">{{ activeProjects.length }}</span>
        </div>
      </div>
    </header>

    <div class="grid grid-cols-1 gap-4">
      <div v-if="activeProjects.length === 0" class="glass-card p-20 text-center space-y-4">
        <div class="w-20 h-20 bg-white/5 rounded-full flex items-center justify-center mx-auto text-4xl">💎</div>
        <h3 class="text-xl font-bold">Nenhum projeto recorrente ainda</h3>
        <p class="text-text-muted max-w-sm mx-auto">Feche um lead como "Ganhado" para transformá-lo em um projeto e começar a gerenciar sua recorrência.</p>
      </div>

      <div v-for="lead in activeProjects" :key="lead.id" class="glass-card p-8 flex items-center justify-between group">
        <div class="flex items-center space-x-6">
          <div class="w-16 h-16 bg-gradient-to-tr from-primary to-secondary rounded-2xl flex items-center justify-center text-2xl font-bold shadow-glow group-hover:scale-105 transition-transform">
            {{ lead.nome_empresa.charAt(0) }}
          </div>
          <div>
            <h3 class="text-xl font-bold text-white mb-1">{{ lead.nome_empresa }}</h3>
            <div class="flex items-center space-x-4 text-sm text-text-muted">
              <span class="flex items-center"><UserIcon class="w-4 h-4 mr-1.5" /> {{ lead.nome_cliente }}</span>
              <span class="flex items-center"><CalendarIcon class="w-4 h-4 mr-1.5" /> Ativo desde {{ formatDate(lead.ultima_interacao) }}</span>
            </div>
          </div>
        </div>

        <div class="flex items-center space-x-12">
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
    <div class="bg-primary/10 border border-primary/20 rounded-3xl p-8 flex gap-6 items-center max-w-3xl">
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
