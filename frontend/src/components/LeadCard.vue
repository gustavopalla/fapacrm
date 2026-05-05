<template>
  <div class="glass-card p-5 cursor-grab active:cursor-grabbing group relative overflow-hidden">
    <!-- Background glow effect on hover -->
    <div class="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
    
    <div class="relative z-10">
      <div class="flex justify-between items-start mb-4">
        <h4 class="font-heading font-bold text-white group-hover:text-primary transition-colors leading-tight">
          {{ lead.nome_empresa }}
        </h4>
        <div v-if="!lead.tem_site" class="bg-red-500/10 text-red-400 p-1.5 rounded-lg border border-red-500/20 shadow-sm" title="Sem Site">
          <GlobeIcon class="w-3.5 h-3.5" />
        </div>
        <div v-else class="bg-green-500/10 text-green-400 p-1.5 rounded-lg border border-green-500/20 shadow-sm" title="Com Site">
          <CheckIcon class="w-3.5 h-3.5" />
        </div>
      </div>
      
      <div class="flex items-center text-xs text-text-muted space-x-2.5 mb-5">
        <div class="w-6 h-6 rounded-full bg-surface border border-white/10 flex items-center justify-center overflow-hidden">
          <UserIcon class="w-3 h-3 text-text-dim" />
        </div>
        <span class="font-medium flex-1 truncate">{{ lead.nome_cliente }}</span>
        <span class="px-1.5 py-0.5 rounded bg-white/5 border border-white/10 text-[9px] font-bold text-text-muted uppercase">
          {{ lead.nicho }}
        </span>
      </div>

      <div class="flex items-center justify-between pt-4 border-t border-white/5">
        <div class="flex flex-col">
          <span class="text-[10px] text-text-dim uppercase tracking-wider font-semibold">Valor</span>
          <span class="text-sm font-bold text-primary">
            {{ formatCurrency(lead.valor_estimado) }}
          </span>
        </div>
        <div class="flex flex-col items-end">
          <span class="text-[10px] text-text-dim uppercase tracking-wider font-semibold">Último Contato</span>
          <span class="text-[11px] font-mono text-text-muted">
            {{ formatDate(lead.ultima_interacao) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Subtle border highlight -->
    <div class="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-primary/20 to-transparent"></div>
  </div>
</template>

<script setup lang="ts">
import { Globe as GlobeIcon, User as UserIcon, Check as CheckIcon } from 'lucide-vue-next'

defineProps<{
  lead: any
}>()

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    maximumFractionDigits: 0
  }).format(value)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })
}
</script>
