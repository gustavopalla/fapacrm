<template>
  <div class="min-h-screen bg-background text-white flex font-body selection:bg-primary/30">
    <!-- Mobile Overlay -->
    <Transition name="fade">
      <div v-if="sidebarOpen && isMobile && !route.meta.public" @click="sidebarOpen = false" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-30 lg:hidden"></div>
    </Transition>

    <!-- Sidebar -->
    <aside v-if="!route.meta.public" 
      class="fixed lg:relative w-72 bg-surface/50 backdrop-blur-xl border-r border-white/5 flex flex-col z-40 h-full transition-transform duration-300 lg:translate-x-0"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
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
          v-slot="{ isActive }"
          @click="sidebarOpen = false">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <LayoutDashboardIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Pipeline</span>
        </router-link>

        <router-link to="/guia" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }"
          @click="sidebarOpen = false">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <BookOpenIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Guia de Vendas</span>
        </router-link>

        <router-link to="/projetos" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }"
          @click="sidebarOpen = false">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <ActivityIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Recorrência</span>
        </router-link>

        <router-link to="/clientes" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }"
          @click="sidebarOpen = false">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <UsersIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Clientes</span>
        </router-link>

        <router-link to="/analytics" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }"
          @click="sidebarOpen = false">
          <div v-if="isActive" class="absolute inset-y-0 left-0 w-1 bg-primary rounded-full"></div>
          <BarChartIcon class="w-5 h-5 transition-colors" :class="isActive ? 'text-primary' : 'text-text-muted group-hover:text-white'" />
          <span class="font-medium" :class="isActive ? 'text-white' : 'text-text-muted group-hover:text-white'">Analytics</span>
        </router-link>

        <router-link to="/configuracoes" class="flex items-center space-x-3 p-3.5 rounded-xl transition-all duration-200 group relative overflow-hidden" 
          active-class="bg-primary/10 text-primary border border-primary/20"
          v-slot="{ isActive }"
          @click="sidebarOpen = false">
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
    <main class="flex-1 flex flex-col relative overflow-hidden w-full lg:w-auto">
      <!-- Top header -->
      <header v-if="!route.meta.public" class="h-16 lg:h-20 bg-background/60 backdrop-blur-md border-b border-white/5 flex items-center justify-between px-4 lg:px-10 sticky top-0 z-10">
        <div class="flex items-center gap-3">
          <!-- Hamburger Menu (Mobile) -->
          <button @click="sidebarOpen = !sidebarOpen" class="lg:hidden p-2 hover:bg-white/5 rounded-xl transition-colors">
            <MenuIcon class="w-6 h-6 text-text-muted" />
          </button>
          <div>
            <h2 class="text-lg lg:text-xl font-heading font-semibold text-white">Funil de Vendas</h2>
            <p class="text-xs lg:text-sm text-text-muted hidden sm:block">Gerencie seus leads e oportunidades</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-2 lg:space-x-4">
          <div class="relative group hidden md:block">
            <SearchIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-dim group-focus-within:text-primary transition-colors" />
            <input 
              type="text" 
              placeholder="Pesquisar..." 
              class="bg-surface/50 border border-white/5 rounded-full pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 w-64 transition-all"
            />
          </div>
          <!-- Mobile search button -->
          <button @click="showMobileSearch = !showMobileSearch" class="md:hidden p-2 hover:bg-white/5 rounded-xl transition-colors">
            <SearchIcon class="w-5 h-5 text-text-muted" />
          </button>
          <button @click="showAddModal = true" class="bg-primary hover:bg-primary/90 text-white px-4 lg:px-6 py-2 lg:py-2.5 rounded-xl font-medium transition-all shadow-glow hover:scale-[1.02] active:scale-[0.98] text-sm lg:text-base">
            <span class="hidden sm:inline">+ Novo Lead</span>
            <span class="sm:hidden">+</span>
          </button>
        </div>
      </header>

      <!-- Mobile Search Bar -->
      <Transition name="slide-down">
        <div v-if="showMobileSearch && !route.meta.public" class="md:hidden px-4 py-3 bg-background/80 backdrop-blur-md border-b border-white/5">
          <div class="relative group">
            <SearchIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-dim group-focus-within:text-primary transition-colors" />
            <input 
              type="text" 
              placeholder="Pesquisar..." 
              class="bg-surface/50 border border-white/5 rounded-xl pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 w-full transition-all"
              autofocus
            />
          </div>
        </div>
      </Transition>
      
      <!-- Content Area -->
      <div class="flex-1 overflow-x-auto scrollbar-hide" :class="route.meta.public ? '' : 'p-4 lg:p-10'">
        <div class="mx-auto h-full" :class="route.meta.public ? 'w-full' : 'max-w-[1600px]'">
          <router-view />
        </div>
      </div>

      <!-- Bottom Navigation (Mobile) -->
      <nav v-if="!route.meta.public" class="lg:hidden fixed bottom-0 left-0 right-0 bg-surface/90 backdrop-blur-xl border-t border-white/5 z-20 safe-area-bottom">
        <div class="flex items-center justify-around px-2 py-1">
          <router-link to="/" class="flex flex-col items-center py-2 px-3 rounded-xl transition-all" 
            active-class="text-primary"
            v-slot="{ isActive }">
            <LayoutDashboardIcon class="w-5 h-5" :class="isActive ? 'text-primary' : 'text-text-muted'" />
            <span class="text-[10px] mt-1 font-medium" :class="isActive ? 'text-primary' : 'text-text-dim'">Pipeline</span>
          </router-link>
          <router-link to="/clientes" class="flex flex-col items-center py-2 px-3 rounded-xl transition-all"
            active-class="text-primary"
            v-slot="{ isActive }">
            <UsersIcon class="w-5 h-5" :class="isActive ? 'text-primary' : 'text-text-muted'" />
            <span class="text-[10px] mt-1 font-medium" :class="isActive ? 'text-primary' : 'text-text-dim'">Clientes</span>
          </router-link>
          <router-link to="/analytics" class="flex flex-col items-center py-2 px-3 rounded-xl transition-all"
            active-class="text-primary"
            v-slot="{ isActive }">
            <BarChartIcon class="w-5 h-5" :class="isActive ? 'text-primary' : 'text-text-muted'" />
            <span class="text-[10px] mt-1 font-medium" :class="isActive ? 'text-primary' : 'text-text-dim'">Analytics</span>
          </router-link>
          <router-link to="/projetos" class="flex flex-col items-center py-2 px-3 rounded-xl transition-all"
            active-class="text-primary"
            v-slot="{ isActive }">
            <ActivityIcon class="w-5 h-5" :class="isActive ? 'text-primary' : 'text-text-muted'" />
            <span class="text-[10px] mt-1 font-medium" :class="isActive ? 'text-primary' : 'text-text-dim'">Recorrência</span>
          </router-link>
          <router-link to="/guia" class="flex flex-col items-center py-2 px-3 rounded-xl transition-all"
            active-class="text-primary"
            v-slot="{ isActive }">
            <BookOpenIcon class="w-5 h-5" :class="isActive ? 'text-primary' : 'text-text-muted'" />
            <span class="text-[10px] mt-1 font-medium" :class="isActive ? 'text-primary' : 'text-text-dim'">Guia</span>
          </router-link>
        </div>
      </nav>
    </main>

    <AddLeadModal v-if="!route.meta.public" :show="showAddModal" @close="showAddModal = false" />
    <ToastNotification />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { 
  LayoutDashboard as LayoutDashboardIcon, 
  Users as UsersIcon, 
  Settings as SettingsIcon,
  Search as SearchIcon,
  BookOpen as BookOpenIcon,
  Activity as ActivityIcon,
  BarChart3 as BarChartIcon,
  Menu as MenuIcon
} from 'lucide-vue-next'

const route = useRoute()
import AddLeadModal from './components/AddLeadModal.vue'
import ToastNotification from './components/ToastNotification.vue'
import { useSettingsStore } from './stores/settings'

const settingsStore = useSettingsStore()
settingsStore.loadSettings()

const showAddModal = ref(false)
const sidebarOpen = ref(false)
const showMobileSearch = ref(false)
const isMobile = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth < 1024
  if (!isMobile.value) {
    sidebarOpen.value = false
  }
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Fade transition */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Slide-down transition */
.slide-down-enter-active, .slide-down-leave-active { transition: all 0.3s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-10px); }

/* Safe area for bottom nav on iOS */
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
</style>
