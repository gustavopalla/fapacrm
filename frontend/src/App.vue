<template>
  <div class="min-h-screen bg-background text-white flex font-body selection:bg-primary/30">
    <!-- Sidebar -->
    <aside v-if="!route.meta.public" class="w-72 bg-surface/50 backdrop-blur-xl border-r border-white/5 flex flex-col z-20">
      <div class="p-8">
        <div class="flex items-center space-x-3 group cursor-pointer">
          <div class="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform duration-300 overflow-hidden">
            <img src="/image.png" alt="FAPA" class="w-full h-full object-contain" />
          </div>
          <div>
            <h1 class="text-xl font-heading font-bold text-white tracking-tight">Assessoria Fapa</h1>
            <p class="text-xs text-primary font-medium tracking-widest uppercase">CRM</p>
          </div>
        </div>
      </div>
      
      <nav class="flex-1 px-6 space-y-2 mt-4">
        <router-link to="/" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <LayoutDashboardIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Pipeline</span>
        </router-link>

        <router-link to="/guia" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <BookOpenIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Guia de Vendas</span>
        </router-link>

        <router-link to="/projetos" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <ActivityIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Recorrência</span>
        </router-link>

        <router-link to="/clientes" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <UsersIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Clientes</span>
        </router-link>

        <router-link to="/analytics" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <BarChartIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Analytics</span>
        </router-link>

        <router-link to="/configuracoes" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <SettingsIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Configurações</span>
        </router-link>
      </nav>

      <div class="p-6 border-t border-white/5">
        <div class="flex items-center space-x-3 p-2">
          <div class="w-10 h-10 rounded-full bg-surface border border-white/10 overflow-hidden">
            <img :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${settingsStore.profile.name}`" alt="User" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate text-white">{{ settingsStore.profile.name }}</p>
            <p class="text-xs text-text-dim truncate">{{ settingsStore.profile.role }}</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col relative overflow-hidden">
      <!-- Top header -->
      <header v-if="!route.meta.public" class="h-20 bg-background/60 backdrop-blur-md border-b border-white/5 flex items-center justify-between px-10 sticky top-0 z-10">
        <div>
          <h2 class="text-xl font-heading font-semibold text-white">Funil de Vendas</h2>
          <p class="text-sm text-text-muted">Gerencie seus leads e oportunidades</p>
        </div>
        
        <div class="flex items-center space-x-4">
          <div class="relative group">
            <SearchIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-dim group-focus-within:text-primary transition-colors" />
            <input 
              type="text" 
              placeholder="Pesquisar..." 
              class="bg-surface/50 border border-white/5 rounded-full pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 w-64 transition-all"
            />
          </div>
          <button @click="showAddModal = true" class="bg-primary hover:bg-primary/90 text-white px-6 py-2.5 rounded-xl font-medium transition-all shadow-glow hover:scale-[1.02] active:scale-[0.98]">
            + Novo Lead
          </button>
        </div>
      </header>
      
      <!-- Content Area -->
      <div class="flex-1 overflow-x-auto scrollbar-hide" :class="route.meta.public ? '' : 'p-10'">
        <div class="mx-auto h-full" :class="route.meta.public ? 'w-full' : 'max-w-[1600px]'">
          <router-view />
        </div>
      </div>
    </main>

    <AddLeadModal v-if="!route.meta.public" :show="showAddModal" @close="showAddModal = false" />
    <ToastNotification />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { 
  LayoutDashboard as LayoutDashboardIcon, 
  Users as UsersIcon, 
  Settings as SettingsIcon,
  Search as SearchIcon,
  BookOpen as BookOpenIcon,
  Activity as ActivityIcon,
  BarChart3 as BarChartIcon
} from 'lucide-vue-next'

const route = useRoute()
import AddLeadModal from './components/AddLeadModal.vue'
import ToastNotification from './components/ToastNotification.vue'
import { useSettingsStore } from './stores/settings'

const settingsStore = useSettingsStore()
settingsStore.loadSettings()

const showAddModal = ref(false)
</script>

<style>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
