<template>
  <div>
    <!-- Overlay -->
    <Transition name="fade">
      <div v-if="lead" @click="$emit('close')" class="fixed inset-0 bg-background/60 backdrop-blur-md z-[80]"></div>
    </Transition>

    <!-- Modal Card -->
    <Transition name="zoom">
      <div v-if="lead" class="fixed inset-0 z-[90] flex items-center justify-center p-0 lg:p-4 pointer-events-none">
        <div class="w-full h-full lg:h-auto lg:max-w-2xl bg-surface/95 backdrop-blur-xl shadow-2xl rounded-none lg:rounded-[2.5rem] flex flex-col border-0 lg:border border-white/10 overflow-hidden pointer-events-auto lg:max-h-[90vh]">
          
          <!-- Header (Editable Info) -->
          <header class="p-4 lg:p-8 border-b border-white/5 flex justify-between items-start bg-gradient-to-br from-primary/10 to-transparent">
            <div class="flex items-start space-x-3 lg:space-x-5 flex-1 min-w-0">
              <div class="w-12 h-12 lg:w-16 lg:h-16 bg-gradient-to-tr from-primary to-secondary rounded-2xl flex items-center justify-center shadow-glow shrink-0 mt-1">
                <span class="text-xl lg:text-3xl font-heading font-bold text-white">{{ editableLead.nome_empresa?.charAt(0) || '?' }}</span>
              </div>
              
              <div class="space-y-3 flex-1">
                <!-- Empresa -->
                <input 
                  v-model="editableLead.nome_empresa"
                  class="bg-transparent text-xl lg:text-3xl font-heading font-bold text-white leading-tight focus:outline-none border-b border-transparent focus:border-primary/30 w-full"
                  placeholder="Nome da Empresa"
                />
                
                <div class="flex flex-wrap gap-2 lg:gap-4 items-center">
                  <!-- Cliente -->
                  <div class="flex items-center text-base text-text-muted group">
                    <UserIcon class="w-4 h-4 mr-2 group-focus-within:text-primary transition-colors" />
                    <input 
                      v-model="editableLead.nome_cliente"
                      class="bg-transparent focus:outline-none border-b border-transparent focus:border-primary/30 w-40"
                      placeholder="Nome do Responsável"
                    />
                  </div>
                  
                  <!-- Telefone -->
                  <div class="flex items-center text-base text-text-muted group">
                    <PhoneIcon class="w-4 h-4 mr-2 group-focus-within:text-primary transition-colors" />
                    <input 
                      v-model="editableLead.telefone"
                      class="bg-transparent focus:outline-none border-b border-transparent focus:border-primary/30 w-40"
                      placeholder="(00) 00000-0000"
                    />
                  </div>

                  <!-- Nicho Badge (Selectable) -->
                  <select 
                    v-model="editableLead.nicho"
                    class="px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-xs font-bold text-primary uppercase tracking-widest focus:outline-none appearance-none cursor-pointer"
                  >
                    <option v-for="niche in settingsStore.niches" :key="niche.id" :value="niche.id">
                      {{ niche.label }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
            
            <div class="flex items-center gap-3">
              <button @click="handleDelete" class="p-3 bg-red-500/5 hover:bg-red-500/10 rounded-2xl transition-all border border-red-500/10 group" title="Remover Lead">
                <TrashIcon class="w-5 h-5 text-red-400 opacity-60 group-hover:opacity-100 transition-opacity" />
              </button>
              <button @click="$emit('close')" class="p-3 bg-white/5 hover:bg-white/10 rounded-2xl transition-all border border-white/5 group">
                <XIcon class="w-6 h-6 text-text-muted group-hover:text-white transition-colors" />
              </button>
            </div>
          </header>

          <div class="flex-1 overflow-y-auto p-4 lg:p-10 space-y-8 lg:space-y-12 scrollbar-hide pb-20 lg:pb-4">
            <!-- Pipeline Status -->
            <section>
              <h4 class="text-sm font-semibold text-text-dim uppercase tracking-widest mb-4">Pipeline Status</h4>
              <div class="flex flex-col sm:flex-row items-stretch sm:items-center p-1.5 bg-background rounded-2xl border border-white/5 gap-2 sm:gap-0">
                <select 
                  v-model="editableLead.status"
                  class="bg-primary/10 text-primary text-base font-bold border border-primary/20 px-6 py-3 rounded-xl focus:outline-none appearance-none cursor-pointer"
                >
                  <option value="PROSPECCAO">Garimpo</option>
                  <option value="CONTATO">Primeiro Contato</option>
                  <option value="BRIEFING">Reunião/Briefing</option>
                  <option value="PROPOSTA">Proposta Enviada</option>
                  <option value="AGUARDANDO">Aguardando Cliente</option>
                  <option value="FECHADO">Contrato Assinado</option>
                  <option value="PERDIDO">Perdido</option>
                </select>
                <div class="flex-1 px-4 text-xs lg:text-sm text-text-dim italic">
                  Última atualização: {{ formatDate(lead.ultima_interacao) }}
                </div>
              </div>

              <!-- Motivo de Espera (Conditional) -->
              <div v-if="editableLead.status === 'AGUARDANDO'" class="mt-4 animate-in fade-in slide-in-from-top-2 duration-300">
                <label class="block text-xs font-bold text-primary uppercase tracking-widest mb-2 ml-1">Motivo da Espera</label>
                <textarea 
                  v-model="editableLead.motivo_espera"
                  rows="2"
                  class="w-full bg-background border border-primary/20 rounded-xl px-4 py-3 text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all placeholder:text-text-dim/50"
                  placeholder="Explique por que este lead está em espera..."
                ></textarea>
              </div>
            </section>

            <!-- Metrics (With Editable Valor) -->
            <section class="grid grid-cols-1 sm:grid-cols-2 gap-4 lg:gap-6">
              <div class="p-4 lg:p-6 rounded-3xl border border-white/5 bg-background/50 group hover:border-primary/30 transition-colors">
                <label class="text-xs font-bold text-text-dim uppercase tracking-widest block mb-3">Presença Web</label>
                <div class="flex items-center space-x-3">
                  <div :class="editableLead.tem_site ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-red-500/10 text-red-400 border-red-500/20'" class="p-2.5 rounded-xl border cursor-pointer" @click="editableLead.tem_site = !editableLead.tem_site">
                    <GlobeIcon class="w-6 h-6" />
                  </div>
                  <span class="text-xl font-bold text-white">{{ editableLead.tem_site ? 'Tem Site' : 'Sem Site' }}</span>
                </div>
              </div>
              <div class="p-4 lg:p-6 rounded-3xl border border-white/5 bg-background/50 group hover:border-primary/30 transition-colors">
                <label class="text-xs font-bold text-text-dim uppercase tracking-widest block mb-3">Valor Estimado (R$)</label>
                <div class="flex items-center space-x-3">
                  <div class="p-2.5 rounded-xl border border-primary/20 bg-primary/10 text-primary">
                    <TrendingUpIcon class="w-6 h-6" />
                  </div>
                  <input 
                    type="number" 
                    v-model="editableLead.valor_estimado"
                    class="bg-transparent text-xl font-bold text-white focus:outline-none w-full"
                  />
                </div>
              </div>
            </section>

            <!-- Diagnóstico Técnico -->
            <section class="space-y-6">
              <h4 class="text-sm font-semibold text-text-dim uppercase tracking-widest flex items-center gap-2">
                <ShieldCheckIcon class="w-4 h-4" />
                Diagnóstico Técnico
              </h4>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 lg:gap-6">
                <div class="glass-card p-4 lg:p-6 space-y-4">
                  <div class="flex items-center justify-between">
                    <label class="text-xs font-bold text-text-dim uppercase">Performance (0-100)</label>
                    <input type="number" v-model="editableLead.nota_performance" placeholder="90" class="w-full bg-background border border-white/5 rounded-xl px-4 py-2 text-white focus:outline-none focus:border-primary/30" />
                  </div>
                  <div class="space-y-2">
                    <label class="text-xs font-bold text-text-dim uppercase block flex items-center gap-2">
                      <BarChartIcon class="w-3.5 h-3.5 text-primary" />
                      GA4 Property ID
                    </label>
                    <input type="text" v-model="editableLead.ga4_property_id" placeholder="Ex: 534388123" class="w-full bg-background border border-white/5 rounded-xl px-4 py-2 text-white focus:outline-none focus:border-primary/30" />
                  </div>
                </div>
                <div class="glass-card p-4 lg:p-6 space-y-4">
                  <div class="flex items-center justify-between">
                    <label class="text-xs font-bold text-text-dim uppercase">Tem Pixel?</label>
                    <input type="checkbox" v-model="editableLead.tem_pixel" class="w-5 h-5 accent-primary" />
                  </div>
                  <div class="space-y-2">
                    <label class="text-xs font-bold text-text-dim uppercase block">Nota Google (0-5)</label>
                    <input type="number" v-model="editableLead.nota_google_meu_negocio" step="0.1" placeholder="4.5" class="w-full bg-background border border-white/5 rounded-xl px-4 py-2 text-white focus:outline-none focus:border-primary/30" />
                  </div>
                </div>
              </div>
            </section>

            <!-- Action Items & Notes -->
            <section class="space-y-6">
              <div class="space-y-3">
                <label class="block text-base font-medium text-text-muted ml-1">Notas da Oportunidade</label>
                <textarea v-model="editableLead.notas" rows="5" class="w-full bg-background/50 border border-white/5 rounded-2xl p-6 text-white focus:outline-none focus:border-primary/30 focus:ring-1 focus:ring-primary/10 transition-all placeholder:text-text-dim text-base" placeholder="Descreva os pontos chave desta prospecção..."></textarea>
              </div>
              
              <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between p-4 lg:p-6 rounded-2xl border border-white/5 bg-background/30 gap-3 sm:gap-0">
                <div class="flex items-center space-x-3">
                  <CalendarIcon class="w-5 h-5 text-text-muted" />
                  <span class="text-base text-text-muted font-medium">Data de Follow-up</span>
                </div>
                <input type="date" v-model="editableLead.proximo_contato" class="bg-transparent text-base text-white focus:outline-none cursor-pointer" />
              </div>
            </section>

            <!-- Sales Toolkit -->
            <section class="space-y-6 pt-8 border-t border-white/5">
              <div class="flex items-center justify-between">
                <h4 class="text-sm font-semibold text-text-dim uppercase tracking-widest">Toolkit do Vendedor</h4>
                <span class="px-3 py-1 rounded-md bg-primary/10 text-xs text-primary font-bold border border-primary/20">
                  Dicas de {{ getNicheLabel(editableLead.nicho) }}
                </span>
              </div>

              <div class="space-y-3">
                <label class="flex items-center text-base font-medium text-text-muted ml-1">
                  <MessageSquareIcon class="w-5 h-5 mr-3 text-primary" />
                  Script de Abordagem Sugerido
                </label>
                <div class="bg-primary/5 border border-primary/10 rounded-2xl p-6 relative group">
                  <p class="text-base text-text-muted italic leading-relaxed pr-10">{{ getScript(editableLead.nicho) }}</p>
                  <button @click="copyText(getScript(editableLead.nicho))" class="absolute top-4 right-4 p-2 rounded-lg bg-white/5 hover:bg-white/10 text-text-muted hover:text-white transition-colors">
                    <CopyIcon class="w-4 h-4" />
                  </button>
                </div>
              </div>
            </section>
          </div>

          <footer class="p-4 lg:p-8 border-t border-white/5 bg-background/30 flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-4">
            <button @click="handleSave" :disabled="saving" class="flex-1 bg-white/5 hover:bg-white/10 text-white py-4 rounded-2xl font-bold transition-all border border-white/5 flex items-center justify-center gap-2">
              <span v-if="saving" class="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
              {{ saving ? 'Salvando...' : 'Salvar Alterações' }}
            </button>
            <button v-if="editableLead.status !== 'FECHADO'" @click="handleWin" :disabled="saving" class="flex-1 bg-primary hover:bg-primary/90 text-white py-4 rounded-2xl font-bold transition-all shadow-glow flex items-center justify-center gap-2">
              <TrophyIcon class="w-5 h-5" />
              Ganha (Closed Won)
            </button>
          </footer>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { 
  X as XIcon, 
  User as UserIcon, 
  Globe as GlobeIcon, 
  TrendingUp as TrendingUpIcon,
  Calendar as CalendarIcon,
  MessageSquare as MessageSquareIcon,
  Copy as CopyIcon,
  ShieldCheck as ShieldCheckIcon,
  Trash2 as TrashIcon,
  Trophy as TrophyIcon,
  Phone as PhoneIcon,
  BarChart3 as BarChartIcon
} from 'lucide-vue-next'
import { useLeadStore } from '../stores/leads'
import { useSettingsStore } from '../stores/settings'
import { useToastStore } from '../stores/toast'

const props = defineProps<{
  lead: any | null
}>()

const emit = defineEmits(['close'])
const leadStore = useLeadStore()
const settingsStore = useSettingsStore()
const toast = useToastStore()
const saving = ref(false)

const editableLead = ref<any>({})

watch(() => props.lead, (newLead) => {
  if (newLead) {
    editableLead.value = { ...newLead }
  }
}, { immediate: true })

const handleSave = async () => {
  if (!props.lead) return
  saving.value = true
  try {
    await leadStore.updateLead(props.lead.id, editableLead.value)
    toast.notify('Dados atualizados com sucesso!')
  } catch (err) {
    toast.notify('Erro ao salvar alterações.', 'error')
  } finally {
    saving.value = false
  }
}

const handleWin = async () => {
  if (!props.lead) return
  saving.value = true
  try {
    await leadStore.updateLead(props.lead.id, { ...editableLead.value, status: 'FECHADO' })
    
    // Confetti celebration!
    // @ts-ignore
    if (window.confetti) {
      // @ts-ignore
      window.confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#7c3aed', '#a855f7', '#ffffff']
      })
    }
    
    toast.notify('VITÓRIA! Contrato fechado! 🏆')
    emit('close')
  } catch (err) {
    toast.notify('Erro ao fechar contrato.', 'error')
  } finally {
    saving.value = false
  }
}

const handleDelete = async () => {
  if (!props.lead) return
  if (confirm(`Remover permanentemente "${editableLead.value.nome_empresa}"?`)) {
    try {
      await leadStore.deleteLead(props.lead.id)
      toast.notify('Lead removido.', 'info')
      emit('close')
    } catch (err) {
      toast.notify('Erro ao remover lead.', 'error')
    }
  }
}



const getScript = (nichoId: string) => {
  const niche = settingsStore.niches.find(n => n.id === nichoId)
  if (niche) return niche.script
  const outros = settingsStore.niches.find(n => n.id === 'OUTROS')
  return outros ? outros.script : 'Script não configurado.'
}

const getNicheLabel = (nichoId: string) => {
  const niche = settingsStore.niches.find(n => n.id === nichoId)
  return niche ? niche.label : nichoId
}

const copyText = (text: string) => {
  navigator.clipboard.writeText(text)
  toast.notify('Script copiado!')
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}
</script>

<style scoped>
.zoom-enter-active, .zoom-leave-active { transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.zoom-enter-from, .zoom-leave-to { transform: scale(0.9) translateY(20px); opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }

/* Input focus styles for header */
input:focus {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}
</style>
