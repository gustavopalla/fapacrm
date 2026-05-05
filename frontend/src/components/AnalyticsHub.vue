<template>
  <div class="h-full flex flex-col space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-heading font-bold text-white">Analytics</h1>
        <p class="text-sm text-text-muted mt-1">Selecione um cliente para visualizar o painel de métricas.</p>
      </div>
      
      <!-- Global Status -->
      <div class="flex items-center gap-3 bg-surface/40 backdrop-blur-md px-4 py-2 rounded-xl border border-white/5">
        <div :class="ga4Status.authenticated ? 'bg-green-500' : 'bg-red-500'" class="w-2 h-2 rounded-full shadow-glow"></div>
        <span class="text-xs font-bold text-white uppercase tracking-widest">
          {{ ga4Status.authenticated ? 'Google Analytics Conectado' : 'Google Analytics Desconectado' }}
        </span>
        <button 
          v-if="!ga4Status.authenticated" 
          @click="handleAuthorize" 
          class="ml-2 px-3 py-1 bg-primary text-[10px] font-bold text-white rounded-md hover:bg-primary/80 transition-colors uppercase"
        >
          Autorizar
        </button>
      </div>
    </div>

    <div v-if="leadsStore.loading" class="flex-1 flex items-center justify-center">
      <div class="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full"></div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div 
        v-for="lead in leadsStore.leads" 
        :key="lead.id"
        class="bg-surface/40 backdrop-blur-md border border-white/5 rounded-2xl p-6 hover:bg-surface/60 transition-all duration-300 group flex flex-col"
      >
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center border border-primary/20 text-primary group-hover:scale-110 transition-transform">
              <span class="font-heading font-bold text-lg">{{ (lead.nome_cliente || 'C').charAt(0) }}</span>
            </div>
            <div>
              <h3 class="font-semibold text-white group-hover:text-primary transition-colors">{{ lead.nome_empresa || lead.nome_cliente }}</h3>
              <p class="text-sm text-text-muted">{{ lead.status }}</p>
            </div>
          </div>
          
          <!-- Property Badge -->
          <div v-if="lead.ga4_property_id" class="px-2 py-1 rounded bg-green-500/10 text-green-500 text-[10px] font-bold border border-green-500/20" title="GA4 Configurado">
            LIVE
          </div>
          <div v-else class="px-2 py-1 rounded bg-white/5 text-text-muted text-[10px] font-bold border border-white/10" title="Usando Dados Mockados">
            MOCK
          </div>
        </div>
        
        <div class="mt-auto pt-4 border-t border-white/5 flex gap-3">
          <router-link :to="`/analytics/${lead.id}`" class="flex-1 text-center py-2 bg-primary/10 hover:bg-primary/20 text-primary rounded-lg text-sm font-medium transition-colors">
            Ver Dashboard
          </router-link>
          <router-link :to="`/public/report/${lead.id}`" target="_blank" class="px-3 flex items-center justify-center bg-surface border border-white/10 hover:border-primary/50 text-text-muted hover:text-white rounded-lg transition-colors tooltip-trigger" title="Link Público do Cliente">
            <ExternalLinkIcon class="w-4 h-4" />
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useLeadStore } from '../stores/leads'
import { ExternalLink as ExternalLinkIcon } from 'lucide-vue-next'

const leadsStore = useLeadStore()
const ga4Status = ref({ authenticated: false, has_client_secret: false })

const checkStatus = async () => {
  try {
    const response = await fetch('/api/analytics/status/')
    ga4Status.value = await response.json()
  } catch (error) {
    console.error('Erro ao checar status GA4', error)
  }
}

const handleAuthorize = async () => {
  try {
    // No backend, o authorize abre o navegador e retorna após o login (ou timeout)
    // Para uma experiência melhor, poderíamos ter uma aba de "Aguardando..."
    window.open('/api/analytics/authorize/', '_blank')
    
    // Polling simples para atualizar o status
    const interval = setInterval(async () => {
      await checkStatus()
      if (ga4Status.value.authenticated) clearInterval(interval)
    }, 2000)
    
    setTimeout(() => clearInterval(interval), 60000) // Para após 1 min
  } catch (error) {
    console.error('Erro ao autorizar', error)
  }
}

onMounted(() => {
  if (leadsStore.leads.length === 0) {
    leadsStore.fetchLeads()
  }
  checkStatus()
})
</script>
