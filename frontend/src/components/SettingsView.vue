<template>
  <div class="space-y-8 pb-20">
    <header>
      <h2 class="text-3xl font-heading font-bold text-white">Configurações</h2>
      <p class="text-text-muted mt-2">Personalize o CRM, os nichos de atuação e seus scripts de vendas.</p>
    </header>

    <div class="flex flex-col md:flex-row gap-8">
      <!-- Tabs Menu -->
      <nav class="w-full md:w-64 space-y-2 shrink-0">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all font-medium text-left"
          :class="activeTab === tab.id ? 'bg-primary/20 text-primary border border-primary/30' : 'text-text-muted hover:bg-white/5 hover:text-white border border-transparent'"
        >
          <component :is="tab.icon" class="w-5 h-5" />
          <span>{{ tab.label }}</span>
        </button>
      </nav>

      <!-- Content Area -->
      <div class="flex-1 glass-card p-8">
        
        <!-- Perfil -->
        <div v-if="activeTab === 'profile'" class="space-y-6 animate-in fade-in zoom-in-95 duration-300">
          <div class="border-b border-white/5 pb-4 mb-6">
            <h3 class="text-xl font-bold text-white">Perfil do Vendedor</h3>
            <p class="text-sm text-text-muted">Suas informações de contato e identificação.</p>
          </div>
          
          <div class="space-y-4 max-w-lg">
            <div class="space-y-2">
              <label class="block text-sm font-bold text-text-dim uppercase tracking-wider ml-1">Nome</label>
              <input v-model="profileForm.name" type="text" class="w-full bg-background border border-white/5 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50" />
            </div>
            <div class="space-y-2">
              <label class="block text-sm font-bold text-text-dim uppercase tracking-wider ml-1">Cargo</label>
              <input v-model="profileForm.role" type="text" class="w-full bg-background border border-white/5 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50" />
            </div>
            <div class="space-y-2">
              <label class="block text-sm font-bold text-text-dim uppercase tracking-wider ml-1">Link Padrão do WhatsApp</label>
              <input v-model="profileForm.whatsappLink" type="url" class="w-full bg-background border border-white/5 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50" placeholder="https://wa.me/..." />
            </div>
            
            <button @click="saveProfile" class="mt-6 bg-primary hover:bg-primary/90 text-white px-6 py-3 rounded-xl font-bold transition-all shadow-glow">
              Salvar Perfil
            </button>
          </div>
        </div>

        <!-- Nichos e Scripts -->
        <div v-if="activeTab === 'niches'" class="space-y-6 animate-in fade-in zoom-in-95 duration-300">
          <div class="flex items-center justify-between border-b border-white/5 pb-4 mb-6">
            <div>
              <h3 class="text-xl font-bold text-white">Nichos & Scripts</h3>
              <p class="text-sm text-text-muted">Gerencie os scripts de abordagem que aparecem no Toolkit para cada nicho.</p>
            </div>
            <button @click="showAddNiche = true" class="px-4 py-2 bg-primary/20 text-primary border border-primary/30 rounded-xl font-bold hover:bg-primary hover:text-white transition-all text-sm">
              + Novo Nicho
            </button>
          </div>

          <div v-if="showAddNiche" class="bg-background/50 border border-primary/30 p-6 rounded-2xl mb-8 space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-2">
                <label class="block text-sm font-bold text-text-dim uppercase tracking-wider ml-1">Identificador (ex: ADVOGADOS)</label>
                <input v-model="newNiche.id" type="text" class="w-full bg-surface border border-white/5 rounded-xl px-4 py-2 text-white uppercase focus:border-primary/50 outline-none" />
              </div>
              <div class="space-y-2">
                <label class="block text-sm font-bold text-text-dim uppercase tracking-wider ml-1">Rótulo de Exibição</label>
                <input v-model="newNiche.label" type="text" class="w-full bg-surface border border-white/5 rounded-xl px-4 py-2 text-white focus:border-primary/50 outline-none" placeholder="Escritórios de Advocacia" />
              </div>
            </div>
            <div class="space-y-2">
              <label class="block text-sm font-bold text-text-dim uppercase tracking-wider ml-1">Script de Abordagem Sugerido</label>
              <textarea v-model="newNiche.script" rows="3" class="w-full bg-surface border border-white/5 rounded-xl px-4 py-3 text-white focus:border-primary/50 outline-none placeholder:text-text-dim" placeholder="Oi doutor, vi seu escritório..."></textarea>
            </div>
            <div class="flex justify-end space-x-3 pt-2">
              <button @click="showAddNiche = false" class="px-4 py-2 rounded-xl text-text-muted hover:text-white transition-colors">Cancelar</button>
              <button @click="saveNewNiche" class="px-6 py-2 bg-primary hover:bg-primary/90 text-white rounded-xl font-bold shadow-glow transition-all">Adicionar Nicho</button>
            </div>
          </div>

          <div class="space-y-6">
            <div v-for="(niche, index) in settingsStore.niches" :key="niche.id" class="p-6 bg-background/30 rounded-2xl border border-white/5 space-y-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <span class="px-2 py-1 rounded bg-primary/10 text-primary text-xs font-bold font-mono tracking-wider">{{ niche.id }}</span>
                  <span class="font-bold text-lg text-white">{{ niche.label }}</span>
                </div>
                <button v-if="niche.id !== 'OUTROS'" @click="deleteNiche(niche.id)" class="p-2 text-text-dim hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors">
                  <TrashIcon class="w-4 h-4" />
                </button>
              </div>
              <div class="space-y-2">
                <label class="text-xs font-bold text-text-dim uppercase tracking-widest">Script</label>
                <textarea 
                  v-model="settingsStore.niches[index].script" 
                  @blur="settingsStore.saveNiches(settingsStore.niches)"
                  rows="3" 
                  class="w-full bg-surface border border-white/5 rounded-xl p-4 text-sm text-text-muted focus:text-white focus:border-primary/30 outline-none transition-colors"
                ></textarea>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { 
  User as UserIcon, 
  MessageSquare as MessageSquareIcon, 
  Trash as TrashIcon 
} from 'lucide-vue-next'
import { useSettingsStore, NicheConfig } from '../stores/settings'
import { useToastStore } from '../stores/toast'

const settingsStore = useSettingsStore()
const toast = useToastStore()

const activeTab = ref('profile')
const tabs = [
  { id: 'profile', label: 'Meu Perfil', icon: UserIcon },
  { id: 'niches', label: 'Nichos & Scripts', icon: MessageSquareIcon }
]

const profileForm = reactive({ name: '', role: '', whatsappLink: '' })

const showAddNiche = ref(false)
const newNiche = reactive<NicheConfig>({ id: '', label: '', script: '' })

onMounted(() => {
  settingsStore.loadSettings()
  profileForm.name = settingsStore.profile.name
  profileForm.role = settingsStore.profile.role
  profileForm.whatsappLink = settingsStore.profile.whatsappLink
})

const saveProfile = () => {
  settingsStore.saveProfile({ ...profileForm })
  toast.notify('Perfil atualizado com sucesso!')
}

const saveNewNiche = () => {
  if (!newNiche.id || !newNiche.label || !newNiche.script) {
    toast.notify('Preencha todos os campos do nicho.', 'error')
    return
  }
  settingsStore.addNiche({ 
    id: newNiche.id.toUpperCase().replace(/\s+/g, '_'), 
    label: newNiche.label, 
    script: newNiche.script 
  })
  toast.notify('Novo nicho cadastrado!')
  showAddNiche.value = false
  newNiche.id = ''
  newNiche.label = ''
  newNiche.script = ''
}

const deleteNiche = (id: string) => {
  if (confirm('Tem certeza que deseja remover este nicho?')) {
    settingsStore.removeNiche(id)
    toast.notify('Nicho removido.', 'info')
  }
}
</script>
