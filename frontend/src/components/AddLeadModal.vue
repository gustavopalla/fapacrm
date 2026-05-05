<template>
  <div v-if="show" class="fixed inset-0 bg-background/80 backdrop-blur-md z-[60] flex items-end sm:items-center justify-center p-0 sm:p-4">
    <div class="bg-surface/90 backdrop-blur-2xl rounded-t-3xl sm:rounded-3xl border border-white/10 shadow-2xl w-full sm:max-w-md overflow-hidden animate-in fade-in zoom-in duration-300 max-h-[95vh] sm:max-h-[90vh] flex flex-col">
      <header class="p-4 lg:p-8 border-b border-white/5 flex justify-between items-center bg-gradient-to-r from-primary/10 to-transparent shrink-0">
        <div>
          <h3 class="text-xl font-heading font-bold text-white">Novo Lead</h3>
          <p class="text-xs text-text-muted mt-1">Adicione uma nova oportunidade ao funil</p>
        </div>
        <button @click="$emit('close')" class="text-text-muted hover:text-white p-2 hover:bg-white/5 rounded-xl transition-all">
          <XIcon class="w-6 h-6" />
        </button>
      </header>
      
      <form @submit.prevent="handleSubmit" class="p-4 lg:p-8 space-y-4 lg:space-y-6 overflow-y-auto flex-1">
        <div class="space-y-2">
          <label class="block text-sm font-medium text-text-muted ml-1">Empresa</label>
          <input 
            v-model="form.nome_empresa" 
            required 
            type="text" 
            class="w-full bg-background/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 placeholder:text-text-dim transition-all" 
            placeholder="Ex: Padaria do Zé" 
          />
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-medium text-text-muted ml-1">Nome do Cliente</label>
          <input 
            v-model="form.nome_cliente" 
            required 
            type="text" 
            class="w-full bg-background/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 placeholder:text-text-dim transition-all" 
            placeholder="Ex: José Silva" 
          />
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-medium text-text-muted ml-1">WhatsApp / Telefone</label>
          <input 
            v-model="form.telefone" 
            type="text" 
            class="w-full bg-background/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 placeholder:text-text-dim transition-all" 
            placeholder="Ex: (11) 98888-7777" 
          />
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-medium text-text-muted ml-1">Nicho / Segmento</label>
          <select 
            v-model="form.nicho" 
            class="w-full bg-background/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 transition-all appearance-none"
          >
            <option v-for="niche in settingsStore.niches" :key="niche.id" :value="niche.id">
              {{ niche.label }}
            </option>
          </select>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-text-muted ml-1">Valor Est. (R$)</label>
            <input 
              v-model="form.valor_estimado" 
              type="number" 
              step="1" 
              class="w-full bg-background/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 transition-all" 
            />
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-text-muted ml-1">GA4 Property ID</label>
            <input 
              v-model="form.ga4_property_id" 
              type="text" 
              class="w-full bg-background/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 transition-all" 
              placeholder="Ex: 534388123"
            />
          </div>
        </div>

        <div class="flex items-end pb-3">
          <label class="flex items-center space-x-3 cursor-pointer group ml-1">
            <div class="relative flex items-center">
              <input 
                v-model="form.tem_site" 
                type="checkbox" 
                class="peer appearance-none w-5 h-5 bg-background/50 border border-white/10 rounded-lg checked:bg-primary checked:border-primary transition-all cursor-pointer" 
              />
              <CheckIcon class="absolute w-3.5 h-3.5 text-white opacity-0 peer-checked:opacity-100 pointer-events-none left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 transition-opacity" />
            </div>
            <span class="text-sm text-text-muted group-hover:text-white transition-colors">Já tem site?</span>
          </label>
        </div>

        <button 
          type="submit" 
          :disabled="loading" 
          class="w-full bg-primary hover:bg-primary/90 text-white py-4 rounded-2xl font-bold transition-all shadow-glow hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 disabled:hover:scale-100 flex items-center justify-center space-x-2"
        >
          <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          <span>{{ loading ? 'Processando...' : 'Adicionar Oportunidade' }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { X as XIcon, Check as CheckIcon } from 'lucide-vue-next'
import { useLeadStore } from '../stores/leads'
import { useSettingsStore } from '../stores/settings'

defineProps<{ show: boolean }>()
const emit = defineEmits(['close'])
const leadStore = useLeadStore()
const settingsStore = useSettingsStore()
const loading = ref(false)

const form = reactive({
  nome_empresa: '',
  nome_cliente: '',
  telefone: '',
  valor_estimado: 0,
  tem_site: false,
  status: 'PROSPECCAO',
  nicho: 'OUTROS',
  ga4_property_id: ''
})

const handleSubmit = async () => {
  loading.value = true
  try {
    await leadStore.createLead({ ...form })
    emit('close')
    // Reset form
    form.nome_empresa = ''
    form.nome_cliente = ''
    form.telefone = ''
    form.valor_estimado = 0
    form.tem_site = false
    form.nicho = 'OUTROS'
    form.ga4_property_id = ''
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>
