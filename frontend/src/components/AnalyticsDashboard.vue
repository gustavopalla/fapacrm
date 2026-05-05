<template>
  <div class="h-full flex flex-col space-y-6 text-white pb-10">
    
    <!-- Modais -->
    <WeeklyReportModal 
      :show="showReportModal" 
      :data="reportData" 
      @close="showReportModal = false" 
    />

    <SocialMediaInputModal 
      :show="showSocialInputModal" 
      :is-loading="isGeneratingSocialReport"
      @close="showSocialInputModal = false"
      @generate="generateSocialReport"
    />

    <SocialMediaPreviewModal 
      :show="showSocialPreviewModal"
      :html-content="socialReportHtml"
      @close="showSocialPreviewModal = false"
    />

    <!-- Header Interno -->
    <div v-if="!isPublic" class="flex items-center justify-between">
      <div>
        <div class="flex items-center space-x-2 text-sm text-text-muted mb-2">
          <router-link to="/analytics" class="hover:text-white transition-colors">Analytics</router-link>
          <span>/</span>
          <span class="text-primary">{{ clientName }}</span>
        </div>
        <h1 class="text-2xl font-heading font-bold text-white">Dashboard de Desempenho</h1>
      </div>
      
      <div class="flex items-center space-x-4">
        <!-- Filtros -->
        <select v-model="filterDevice" @change="applyFilters" class="bg-surface/50 border border-white/5 px-4 py-2.5 rounded-xl text-sm font-medium outline-none focus:border-primary/50 transition-colors">
          <option value="all">Todos Dispositivos</option>
          <option value="mobile">Mobile (Celular)</option>
          <option value="desktop">Desktop</option>
        </select>
        
        <select v-model="filterDays" @change="applyFilters" class="bg-surface/50 border border-white/5 px-4 py-2.5 rounded-xl text-sm font-medium outline-none focus:border-primary/50 transition-colors">
          <option value="7">Últimos 7 dias</option>
          <option value="30">Últimos 30 dias</option>
          <option value="365">Este Ano</option>
        </select>

        <button 
          @click="applyFilters" 
          :disabled="isLoadingData"
          class="p-2.5 bg-surface/50 border border-white/5 rounded-xl hover:bg-white/5 transition-all text-text-muted hover:text-primary disabled:opacity-50"
          title="Atualizar Dados"
        >
          <RefreshCwIcon :class="{'animate-spin': isLoadingData}" class="w-5 h-5" />
        </button>

        <button 
          @click="generateWeeklyReport" 
          :disabled="isGeneratingReport"
          class="flex items-center gap-2 bg-[#4CC23A] hover:bg-[#3A9E2C] text-white px-5 py-2.5 rounded-xl font-bold transition-all shadow-lg hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50"
        >
          <FileTextIcon v-if="!isGeneratingReport" class="w-4 h-4" />
          <RefreshCwIcon v-else class="w-4 h-4 animate-spin" />
          <span>Gerar Relatório</span>
        </button>

        <button 
          @click="openSocialModal"
          class="flex items-center gap-2 bg-gradient-to-r from-[#f09433] via-[#e6683c] to-[#bc1888] hover:brightness-110 text-white px-5 py-2.5 rounded-xl font-bold transition-all shadow-lg hover:scale-[1.02] active:scale-[0.98]"
        >
          <InstagramIcon class="w-4 h-4" />
          <span>Relatório Instagram</span>
        </button>
      </div>
    </div>

    <!-- Header Público -->
    <div v-else class="flex items-center justify-between bg-surface/40 backdrop-blur-md p-6 rounded-2xl border border-white/5 mb-4 shadow-lg">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-glow overflow-hidden">
          <img src="/image.png" alt="FAPA" class="w-full h-full object-contain" />
        </div>
        <div>
          <h1 class="text-2xl font-heading font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">Acessoria Fapa</h1>
          <p class="text-xs text-primary font-medium tracking-widest uppercase">Relatório de Performance</p>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <div class="text-right hidden sm:block mr-4">
          <h2 class="text-xl font-semibold text-white">{{ clientName }}</h2>
          <p class="text-sm text-text-muted">Métricas dos últimos {{ filterDays }} dias</p>
        </div>
        
        <button 
          @click="generateWeeklyReport" 
          :disabled="isGeneratingReport"
          class="flex items-center gap-2 bg-[#4CC23A] hover:bg-[#3A9E2C] text-white px-4 py-2 rounded-xl font-bold transition-all shadow-lg text-sm disabled:opacity-50"
        >
          <FileTextIcon v-if="!isGeneratingReport" class="w-4 h-4" />
          <RefreshCwIcon v-else class="w-4 h-4 animate-spin" />
          <span>Site</span>
        </button>

        <button 
          @click="openSocialModal"
          class="flex items-center gap-2 bg-gradient-to-r from-[#f09433] via-[#e6683c] to-[#bc1888] hover:brightness-110 text-white px-4 py-2 rounded-xl font-bold transition-all shadow-lg text-sm"
        >
          <InstagramIcon class="w-4 h-4" />
          <span>Instagram</span>
        </button>
      </div>
    </div>

    <!-- Filtros Ativos (Chips) -->
    <div v-if="filterDevice !== 'all' || filterAudience !== 'all' || filterSource !== 'all'" class="flex items-center gap-3 -mt-2">
      <span class="text-sm text-text-muted font-medium">Filtros aplicados:</span>
      
      <!-- Device Chip -->
      <div v-if="filterDevice !== 'all'" class="flex items-center gap-2 bg-primary/20 text-primary border border-primary/30 px-3 py-1 rounded-full text-sm font-medium">
        <span>{{ filterDevice === 'mobile' ? 'Mobile (Celular)' : 'Desktop' }}</span>
        <button @click="clearFilter('device')" class="hover:text-white transition-colors">
          <XIcon class="w-3.5 h-3.5" />
        </button>
      </div>

      <!-- Audience Chip -->
      <div v-if="filterAudience !== 'all'" class="flex items-center gap-2 bg-primary/20 text-primary border border-primary/30 px-3 py-1 rounded-full text-sm font-medium">
        <span>{{ filterAudience === 'new' ? 'Novos Visitantes' : 'Retornantes' }}</span>
        <button @click="clearFilter('audience')" class="hover:text-white transition-colors">
          <XIcon class="w-3.5 h-3.5" />
        </button>
      </div>
      
      <!-- Source Chip -->
      <div v-if="filterSource !== 'all'" class="flex items-center gap-2 bg-primary/20 text-primary border border-primary/30 px-3 py-1 rounded-full text-sm font-medium">
        <span>Origem: {{ filterSource }}</span>
        <button @click="clearFilter('source')" class="hover:text-white transition-colors">
          <XIcon class="w-3.5 h-3.5" />
        </button>
      </div>
      
      <button @click="clearFilter('all')" class="text-xs text-text-muted hover:text-white transition-colors underline decoration-white/20 underline-offset-4 ml-2">
        Limpar filtros
      </button>
    </div>

    <!-- Main Grid Layout -->
    <div class="grid grid-cols-12 gap-6">
      
      <!-- Coluna Esquerda: KPIs (Span 4) -->
      <div class="col-span-12 lg:col-span-4 flex flex-col gap-6">
        <!-- KPI 1 -->
        <div class="bg-surface/40 backdrop-blur-xl border border-white/5 p-6 rounded-2xl relative overflow-hidden group shadow-lg flex-1 flex flex-col justify-center">
          <div class="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full blur-3xl -mr-10 -mt-10 group-hover:bg-primary/10 transition-colors"></div>
          <div class="flex justify-between items-start mb-2">
            <p class="text-sm text-text-muted font-bold uppercase tracking-wider">Visualizações de Página</p>
          </div>
          <div class="flex items-end justify-between">
            <h3 class="text-5xl font-heading font-bold text-white tracking-tight">{{ formatNumber(metrics.pageViews) }}</h3>
            <div class="text-right">
              <span class="text-lg font-bold" :class="metrics.growth > 0 ? 'text-primary' : 'text-red-500'">{{ metrics.growth > 0 ? '+' : '' }}{{ metrics.growth }}%</span>
              <p class="text-xs text-text-muted mt-1">vs período anterior</p>
            </div>
          </div>
        </div>

        <!-- KPI 2 -->
        <div class="bg-surface/40 backdrop-blur-xl border border-white/5 p-6 rounded-2xl relative overflow-hidden group shadow-lg flex-1 flex flex-col justify-center">
          <div class="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full blur-3xl -mr-10 -mt-10 group-hover:bg-primary/10 transition-colors"></div>
          <div class="flex justify-between items-start mb-2">
            <p class="text-sm text-text-muted font-bold uppercase tracking-wider">Online Agora</p>
          </div>
          <div class="flex items-end justify-between">
            <h3 class="text-5xl font-heading font-bold text-white tracking-tight">{{ formatNumber(metrics.realtimeActiveUsers || 0) }}</h3>
            <div class="text-right">
              <span v-if="hasRealData" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-green-500/10 text-green-400 text-[10px] font-bold uppercase tracking-wider mb-2 border border-green-500/20">
                <div class="w-1 h-1 bg-green-500 rounded-full animate-pulse"></div>
                Live GA4
              </span>
              <div class="mt-1">
                <p class="text-[10px] text-text-muted uppercase font-bold tracking-widest">Total no Período</p>
                <p class="text-lg font-bold text-white">{{ formatNumber(metrics.activeUsers) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Right: Gráfico de Linha (Span 8) -->
      <div class="col-span-12 lg:col-span-8 bg-surface/40 backdrop-blur-xl border border-white/5 p-6 rounded-2xl shadow-lg relative">
        <h3 class="text-sm font-bold text-text-muted uppercase tracking-wider mb-6">Evolução de Acessos</h3>
        <div class="h-[240px]">
          <Line v-if="renderChart" :data="lineData" :options="lineOptions" />
        </div>
      </div>

      <!-- Bottom Left: Gráfico de Barras -->
      <div class="col-span-12 lg:col-span-4 bg-surface/40 backdrop-blur-xl border border-white/5 p-6 rounded-2xl shadow-lg">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-sm font-bold text-text-muted uppercase tracking-wider">Acessos por Dispositivo</h3>
          <SmartphoneIcon class="w-4 h-4 text-primary" />
        </div>
        <div class="h-[200px]">
          <Bar v-if="renderChart" :data="barDataLeft" :options="barOptionsLeft" />
        </div>
      </div>

      <!-- Bottom Middle: Novos vs Retornantes (Donut) -->
      <div class="col-span-12 lg:col-span-3 bg-surface/40 backdrop-blur-xl border border-white/5 p-6 rounded-2xl shadow-lg relative overflow-hidden flex flex-col">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-sm font-bold text-text-muted uppercase tracking-wider">Público</h3>
          <UsersIcon class="w-4 h-4 text-primary" />
        </div>
        <div class="flex-1 flex items-center justify-center relative">
            <div class="h-[180px] w-full">
              <Doughnut v-if="renderChart" :data="donutData" :options="donutOptions" />
            </div>
            <!-- Texto central ocultado pois a legenda e o grafico mais grosso substituem -->
        </div>
      </div>

      <!-- Bottom Right: Gráfico de Barras Longo -->
      <div class="col-span-12 lg:col-span-5 bg-surface/40 backdrop-blur-xl border border-white/5 p-6 rounded-2xl shadow-lg">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-sm font-bold text-text-muted uppercase tracking-wider">Acessos por Origem</h3>
          <GlobeIcon class="w-4 h-4 text-primary" />
        </div>
        <div class="h-[200px]">
          <Bar v-if="renderChart" :data="barDataRight" :options="barOptionsRight" />
        </div>
      </div>

      <!-- Row 3 Left: Insight IA -->
      <div class="col-span-12 lg:col-span-5 bg-gradient-to-br from-surface/60 to-surface/40 backdrop-blur-xl border border-primary/20 p-6 rounded-2xl shadow-lg relative overflow-hidden group">
        <div class="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-3xl -mr-10 -mt-10"></div>
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-sm font-bold text-primary uppercase tracking-wider flex items-center gap-2">
            <SparklesIcon class="w-4 h-4" /> Análise IA
          </h3>
          <span v-if="isLoadingInsight" class="flex items-center space-x-2 text-xs text-primary/70">
            <div class="w-2 h-2 bg-primary rounded-full animate-ping"></div>
            <span>Analisando...</span>
          </span>
        </div>
        <p class="text-sm text-gray-300 leading-relaxed min-h-[60px]" :class="{'opacity-50': isLoadingInsight}">
          {{ aiInsight }}
        </p>
        <div class="mt-6 flex justify-between items-end">
          <div>
            <p class="text-xs text-text-muted uppercase tracking-wider mb-1">Duração Média</p>
            <h4 class="text-3xl font-heading font-bold text-white">{{ metrics.avgDuration }}</h4>
          </div>
          <div>
            <p class="text-xs text-text-muted uppercase tracking-wider mb-1 text-right">Rejeição</p>
            <h4 class="text-3xl font-heading font-bold text-white">{{ metrics.bounceRate }}</h4>
          </div>
        </div>
      </div>

      <!-- Row 3 Right: Páginas Mais Acessadas -->
      <div class="col-span-12 lg:col-span-7 bg-surface/40 backdrop-blur-xl border border-white/5 p-6 rounded-2xl shadow-lg">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-sm font-bold text-text-muted uppercase tracking-wider">Páginas Mais Acessadas</h3>
          <FileTextIcon class="w-4 h-4 text-primary" />
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-text-muted text-xs uppercase tracking-wider border-b border-white/5">
                <th class="pb-3 font-medium">Caminho da Página</th>
                <th class="pb-3 font-medium text-right">Visualizações</th>
                <th class="pb-3 font-medium text-right">% do Total</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr v-for="(page, index) in topPages" :key="index" class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="py-3 text-white truncate max-w-[200px]" :title="page.path">{{ page.path }}</td>
                <td class="py-3 text-right text-primary font-bold">{{ formatNumber(page.views) }}</td>
                <td class="py-3 text-right text-text-muted">
                  <div class="flex items-center justify-end space-x-2">
                    <span>{{ page.percent }}%</span>
                    <div class="w-16 h-1.5 bg-white/10 rounded-full overflow-hidden">
                      <div class="h-full bg-primary rounded-full" :style="`width: ${page.percent}%`"></div>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Row 4 Left: Cidades -->
      <div class="col-span-12 lg:col-span-4 bg-surface/40 backdrop-blur-xl border border-white/5 p-6 rounded-2xl shadow-lg flex flex-col">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-sm font-bold text-text-muted uppercase tracking-wider">Ativos por Cidade</h3>
          <MapPinIcon class="w-4 h-4 text-primary" />
        </div>
        
        <div class="overflow-y-auto flex-1 pr-2" style="scrollbar-width: thin; scrollbar-color: #333 transparent;">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-text-muted text-xs uppercase tracking-wider border-b border-white/5">
                <th class="pb-3 font-medium">Cidade</th>
                <th class="pb-3 font-medium text-right">Usuários</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr v-for="(item, index) in topCities" :key="index" class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="py-3 text-white truncate max-w-[120px]" :title="item.city">{{ item.city }}</td>
                <td class="py-3 text-right text-primary font-bold">{{ formatNumber(item.users) }}</td>
              </tr>
              <tr v-if="topCities.length === 0">
                <td colspan="2" class="py-8 text-center text-text-muted text-sm">Sem dados disponíveis</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Row 4 Right: Chat Interativo com IA -->
      <div class="col-span-12 lg:col-span-8 bg-surface/40 backdrop-blur-xl border border-white/5 rounded-2xl shadow-lg overflow-hidden flex flex-col max-h-[500px]">
        <!-- Header do Chat -->
        <div class="flex items-center justify-between p-5 border-b border-white/5">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gradient-to-tr from-primary to-secondary rounded-lg flex items-center justify-center">
              <MessageCircleIcon class="w-4 h-4 text-white" />
            </div>
            <div>
              <h3 class="text-sm font-bold text-white uppercase tracking-wider">Pergunte aos Dados</h3>
              <p class="text-xs text-text-muted">Tire dúvidas sobre o desempenho do site com a IA</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span class="text-xs text-green-500/80 font-medium">Online</span>
          </div>
        </div>

        <!-- Mensagens -->
        <div ref="chatContainer" class="p-5 space-y-4 max-h-[320px] overflow-y-auto scroll-smooth" style="scrollbar-width: thin; scrollbar-color: #333 transparent;">
          <!-- Mensagem de boas-vindas -->
          <div class="flex items-start gap-3">
            <div class="w-7 h-7 bg-primary/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
              <SparklesIcon class="w-3.5 h-3.5 text-primary" />
            </div>
            <div class="bg-white/5 border border-white/5 rounded-2xl rounded-tl-sm px-4 py-3 max-w-[80%]">
              <p class="text-sm text-gray-300 leading-relaxed">Olá! 👋 Sou a assistente de analytics da <span class="text-primary font-semibold">Assessoria Fapa</span>. Pode me perguntar qualquer coisa sobre os dados do site, como por exemplo: "Por que o tráfego caiu essa semana?" ou "Qual a minha melhor origem de acessos?"</p>
            </div>
          </div>

          <!-- Mensagens do histórico -->
          <template v-for="(msg, index) in chatMessages" :key="index">
            <!-- Mensagem do Usuário -->
            <div v-if="msg.role === 'user'" class="flex items-start gap-3 justify-end">
              <div class="bg-primary/20 border border-primary/20 rounded-2xl rounded-tr-sm px-4 py-3 max-w-[80%]">
                <p class="text-sm text-white leading-relaxed">{{ msg.content }}</p>
              </div>
              <div class="w-7 h-7 bg-white/10 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                <UserIcon class="w-3.5 h-3.5 text-white" />
              </div>
            </div>

            <div v-else class="flex items-start gap-3">
              <div class="w-7 h-7 bg-primary/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                <SparklesIcon class="w-3.5 h-3.5 text-primary" />
              </div>
              <div class="bg-white/5 border border-white/5 rounded-2xl rounded-tl-sm px-4 py-3 max-w-[80%] prose-custom">
                <div class="text-sm text-gray-300 leading-relaxed markdown-content" v-html="renderMarkdown(msg.content)"></div>
              </div>
            </div>
          </template>

          <!-- Indicador de carregamento -->
          <div v-if="isChatLoading" class="flex items-start gap-3">
            <div class="w-7 h-7 bg-primary/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
              <SparklesIcon class="w-3.5 h-3.5 text-primary" />
            </div>
            <div class="bg-white/5 border border-white/5 rounded-2xl rounded-tl-sm px-4 py-3">
              <div class="flex items-center gap-1.5">
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0ms;"></div>
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 150ms;"></div>
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 300ms;"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input do Chat -->
        <div class="p-4 border-t border-white/5">
          <form @submit.prevent="sendChatMessage" class="flex items-center gap-3">
            <input 
              v-model="chatInput" 
              type="text" 
              placeholder="Faça uma pergunta sobre os dados..." 
              class="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder-text-muted outline-none focus:border-primary/50 transition-colors"
              :disabled="isChatLoading"
            />
            <button 
              type="submit" 
              :disabled="isChatLoading || !chatInput.trim()" 
              class="bg-primary hover:bg-primary/80 disabled:bg-white/10 disabled:text-text-muted text-white px-5 py-3 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center gap-2"
            >
              <SendIcon class="w-4 h-4" />
              Enviar
            </button>
          </form>
        </div>
      </div>

    </div>
    

  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, nextTick } from 'vue'
import { marked } from 'marked'
import { useRoute } from 'vue-router'
import { useLeadStore } from '../stores/leads'
import { 
  Smartphone as SmartphoneIcon,
  Globe as GlobeIcon,
  Sparkles as SparklesIcon,
  Users as UsersIcon,
  FileText as FileTextIcon,
  X as XIcon,
  MessageCircle as MessageCircleIcon,
  Send as SendIcon,
  User as UserIcon,
  RefreshCw as RefreshCwIcon,
  Instagram as InstagramIcon,
  MapPin as MapPinIcon
} from 'lucide-vue-next'
import WeeklyReportModal from './WeeklyReportModal.vue'
import SocialMediaInputModal from './SocialMediaInputModal.vue'
import SocialMediaPreviewModal from './SocialMediaPreviewModal.vue'

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line, Bar, Doughnut } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const route = useRoute()
const leadsStore = useLeadStore()

const isPublic = computed(() => route.meta.public === true)
const leadId = Number(route.params.id)

const clientName = computed(() => {
  const lead = leadsStore.leads.find((l: any) => l.id === leadId)
  return lead ? (lead.nome_empresa || lead.nome_cliente) : 'Acessando Relatório...'
})

// Filtros
const filterDays = ref('30')
const filterDevice = ref('all')
const filterAudience = ref('all')
const filterSource = ref('all')
const renderChart = ref(true)

// Métricas Dinâmicas (Mocks que mudam com filtros)
const metrics = ref({
  pageViews: 0,
  activeUsers: 0,
  realtimeActiveUsers: 0,
  growth: 0,
  growthUsers: 0,
  newUsersPercent: 0,
  avgDuration: '0m 0s',
  bounceRate: '0%'
})

const topPages = ref<{path: string, views: number, percent: number}[]>([])
const topCities = ref<{city: string, users: number}[]>([])

const aiInsight = ref('A Inteligência Artificial está analisando as métricas...')
const isLoadingInsight = ref(false)
const isLoadingData = ref(false)
const hasRealData = ref(false)

// Chat Interativo
const chatInput = ref('')
const chatMessages = ref<{role: string, content: string}[]>([])
const isChatLoading = ref(false)
const chatContainer = ref<HTMLElement | null>(null)

// Report State
const showReportModal = ref(false)
const isGeneratingReport = ref(false)
const reportData = ref(null)

// Social Media Report State
const showSocialInputModal = ref(false)
const showSocialPreviewModal = ref(false)
const isGeneratingSocialReport = ref(false)
const socialReportHtml = ref('')

const openSocialModal = () => {
  console.log('Abrindo modal de Social Media...')
  showSocialInputModal.value = true
}

const generateSocialReport = async (rawMetrics: string) => {
  isGeneratingSocialReport.value = true
  try {
    const response = await fetch('/api/analytics/social_media_report/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ metrics: rawMetrics })
    })
    
    if (!response.ok) throw new Error('Falha ao gerar relatório')
    
    const data = await response.json()
    socialReportHtml.value = data.html
    showSocialInputModal.value = false
    showSocialPreviewModal.value = true
  } catch (error) {
    console.error('Erro ao gerar relatório social:', error)
    alert('Erro ao processar as métricas com a IA.')
  } finally {
    isGeneratingSocialReport.value = false
  }
}

const generateWeeklyReport = async () => {
  if (isGeneratingReport.value) return
  isGeneratingReport.value = true
  
  try {
    const response = await fetch(`/api/leads/${leadId}/weekly_report/`)
    if (!response.ok) throw new Error('Falha ao gerar relatório')
    
    const data = await response.json()
    reportData.value = data
    showReportModal.value = true
  } catch (error) {
    console.error('Erro ao gerar relatório:', error)
    alert('Erro ao gerar relatório estratégico. Verifique a conexão com o servidor.')
  } finally {
    isGeneratingReport.value = false
  }
}

const scrollChatToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const renderMarkdown = (text: string) => {
  return marked.parse(text)
}

const sendChatMessage = async () => {
  const question = chatInput.value.trim()
  if (!question || isChatLoading.value) return

  // Adicionar mensagem do usuário
  chatMessages.value.push({ role: 'user', content: question })
  chatInput.value = ''
  isChatLoading.value = true
  scrollChatToBottom()

  try {
    const dashboardData = {
      pageViews: metrics.value.pageViews,
      activeUsers: metrics.value.activeUsers,
      bounceRate: metrics.value.bounceRate,
      avgDuration: metrics.value.avgDuration,
      growth: metrics.value.growth,
      newUsersPercent: metrics.value.newUsersPercent,
      days: filterDays.value,
      device: filterDevice.value,
      source: filterSource.value,
      topPages: topPages.value.map(p => `${p.path} (${p.views} views)`).join(', '),
      topCities: topCities.value.map(c => `${c.city} (${c.users} users)`).join(', ')
    }

    const response = await fetch(`/api/leads/${leadId}/analytics_chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, dashboard_data: dashboardData })
    })
    const data = await response.json()
    chatMessages.value.push({ role: 'ai', content: data.answer })
  } catch (error) {
    chatMessages.value.push({ role: 'ai', content: 'Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente.' })
  } finally {
    isChatLoading.value = false
    scrollChatToBottom()
  }
}

const clearFilter = (type: string) => {
  if (type === 'device') filterDevice.value = 'all'
  else if (type === 'audience') filterAudience.value = 'all'
  else if (type === 'source') filterSource.value = 'all'
  else if (type === 'all') {
    filterDevice.value = 'all'
    filterAudience.value = 'all'
    filterSource.value = 'all'
  }
  applyFilters()
}

const formatNumber = (num: number) => {
  return new Intl.NumberFormat('pt-BR').format(num)
}

const fetchAIInsight = async () => {
  isLoadingInsight.value = true
  try {
    const params = new URLSearchParams({
      days: filterDays.value,
      device: filterDevice.value,
      audience: filterAudience.value,
      source: filterSource.value
    })
    
    // Atualizar dados no backend na requisição
    const response = await fetch(`/api/leads/${leadId}/analytics_insight/?${params}`)
    const data = await response.json()
    if (data.insight) {
      aiInsight.value = data.insight
    }
  } catch (error) {
    console.error('Erro ao buscar IA Insight', error)
    aiInsight.value = "Aguardando dados do Google Analytics. Como a etiqueta foi configurada recentemente, as métricas podem levar até 48 horas para aparecer."
  } finally {
    isLoadingInsight.value = false
  }
}

// Aplicação dos Filtros (Simulação reativa no frontend)
const applyFilters = async () => {
  renderChart.value = false
  
  if (hasRealData.value || leadsStore.leads.find((l: any) => l.id === leadId)?.ga4_property_id) {
    await fetchRealData()
  } else {
    // Se não houver Property ID, resetamos as métricas para zero em vez de mostrar mocks
    metrics.value = {
      pageViews: 0,
      activeUsers: 0,
      realtimeActiveUsers: 0,
      growth: 0,
      growthUsers: 0,
      newUsersPercent: 0,
      avgDuration: '0m 0s',
      bounceRate: '0%'
    }
    topPages.value = []
    topCities.value = []
    lineData.value.datasets[0].data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hasRealData.value = false
  }

  // Feedback visual de seleção no Device
  if (filterDevice.value === 'mobile') {
    barDataLeft.value.datasets[0].backgroundColor = [primaryColor, '#222', '#222']
  } else if (filterDevice.value === 'desktop') {
    barDataLeft.value.datasets[0].backgroundColor = ['#222', primaryColor, '#222']
  }

  await nextTick()
  renderChart.value = true
  fetchAIInsight()
}

const fetchRealData = async () => {
  isLoadingData.value = true
  try {
    const response = await fetch(`/api/leads/${leadId}/analytics_report/?days=${filterDays.value}`)
    if (!response.ok) throw new Error('Falha ao buscar dados reais')
    
    const data = await response.json()
    metrics.value = data.metrics
    topPages.value = data.top_pages
    topCities.value = data.top_cities || []
    
    // Atualizar Gráficos
    lineData.value.labels = data.charts.line.labels
    lineData.value.datasets[0].data = data.charts.line.data
    
    barDataLeft.value.datasets[0].data = data.charts.devices.data
    donutData.value.datasets[0].data = data.charts.audience.data
    
    // Atualizar fontes (labels e data)
    barDataRight.value.labels = data.charts.sources.labels
    barDataRight.value.datasets[0].data = data.charts.sources.data
    
    hasRealData.value = true
  } catch (error) {
    console.error('Erro no GA4:', error)
    hasRealData.value = false
  } finally {
    isLoadingData.value = false
  }
}

let refreshInterval: any = null

onMounted(async () => {
  console.log('Dashboard montado para Lead ID:', leadId)
  if (leadsStore.leads.length === 0) {
    console.log('Buscando leads no store...')
    await leadsStore.fetchLeads()
  }
  
  // Consolidar a lógica chamando applyFilters que já trata renderização e busca
  await applyFilters()

  // Configurar auto-refresh a cada 5 minutos (300.000 ms)
  refreshInterval = setInterval(() => {
    console.log('🔄 Executando atualização automática de dados...')
    applyFilters()
  }, 300000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})

// --- CHART.JS CONFIGS ---
ChartJS.defaults.color = '#666666'
ChartJS.defaults.font.family = "'Inter', sans-serif"

const primaryColor = '#ff751f'

// Linha
const lineData = ref({
  labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex'],
  datasets: [
    {
      label: 'Acessos',
      borderColor: primaryColor,
      borderWidth: 3,
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      tension: 0.4,
      pointBackgroundColor: '#000000',
      pointBorderColor: '#ffb380',
      pointBorderWidth: 3,
      pointRadius: 5,
      pointHoverRadius: 8,
      fill: false
    }
  ]
})

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { backgroundColor: '#111111', titleColor: '#ffffff', bodyColor: primaryColor, borderColor: '#333333', borderWidth: 1, padding: 12, displayColors: false } },
  scales: {
    y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.03)', drawBorder: false }, ticks: { font: { size: 11 }, maxTicksLimit: 5 }, border: { display: false } },
    x: { grid: { display: false }, ticks: { font: { size: 11 } }, border: { display: false } }
  }
}

// Barras Esquerda (Devices)
const barDataLeft = ref({
  labels: ['Mobile', 'Desktop', 'Tablet'],
  datasets: [
    {
      data: [0, 0, 0],
      backgroundColor: primaryColor as string | string[],
      borderRadius: 4,
      barThickness: 16
    }
  ]
})

const barOptionsLeft = {
  responsive: true,
  maintainAspectRatio: false,
  onClick: (_event: any, elements: any, chart: any) => {
    if (elements.length > 0) {
      const index = elements[0].index
      const label = chart.data.labels[index] // 'Mobile', 'Desktop', 'Tablet'
      
      if (label === 'Mobile') filterDevice.value = 'mobile'
      else if (label === 'Desktop') filterDevice.value = 'desktop'
      else filterDevice.value = 'all'
    } else {
      // Se clicar no fundo, reseta o filtro
      filterDevice.value = 'all'
    }
    applyFilters()
  },
  onHover: (event: any, chartElement: any) => {
    event.native.target.style.cursor = chartElement[0] ? 'pointer' : 'default'
  },
  plugins: { legend: { display: false }, tooltip: { backgroundColor: '#111111', titleColor: '#ffffff', bodyColor: '#ffffff', borderColor: '#333333', borderWidth: 1, padding: 12, displayColors: false } },
  scales: {
    y: { display: false, beginAtZero: true, grid: { display: false } },
    x: { grid: { display: false }, ticks: { font: { size: 10 }, color: '#888888' }, border: { display: false } }
  }
}

const barOptionsRight = {
  responsive: true,
  maintainAspectRatio: false,
  onClick: (_event: any, elements: any, chart: any) => {
    if (elements.length > 0) {
      const index = elements[0].index
      const label = chart.data.labels[index] // Origem clicada
      filterSource.value = label
    } else {
      filterSource.value = 'all'
    }
    applyFilters()
  },
  onHover: (event: any, chartElement: any) => {
    event.native.target.style.cursor = chartElement[0] ? 'pointer' : 'default'
  },
  plugins: { legend: { display: false }, tooltip: { backgroundColor: '#111111', titleColor: '#ffffff', bodyColor: '#ffffff', borderColor: '#333333', borderWidth: 1, padding: 12, displayColors: false } },
  scales: {
    y: { display: false, beginAtZero: true, grid: { display: false } },
    x: { grid: { display: false }, ticks: { font: { size: 10 }, color: '#888888' }, border: { display: false } }
  }
}

// Donut (Novos vs Retornantes)
const donutData = ref({
  labels: ['Novos', 'Retornantes'],
  datasets: [{
    data: [0, 0],
    backgroundColor: [primaryColor, '#111111'],
    hoverBackgroundColor: ['#ff8c42', '#222222'],
    borderColor: '#333333',
    borderWidth: 2,
    cutout: '50%' // Mais grosso como na referência
  }]
})

const donutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  onClick: (_event: any, elements: any, chart: any) => {
    if (elements.length > 0) {
      const index = elements[0].index
      const label = chart.data.labels[index] // 'Novos', 'Retornantes'
      
      if (label === 'Novos') filterAudience.value = 'new'
      else if (label === 'Retornantes') filterAudience.value = 'returning'
      else filterAudience.value = 'all'
    } else {
      filterAudience.value = 'all'
    }
    applyFilters()
  },
  onHover: (event: any, chartElement: any) => {
    event.native.target.style.cursor = chartElement[0] ? 'pointer' : 'default'
  },
  plugins: {
    legend: { 
      display: true, 
      position: 'right' as const,
      labels: {
        color: '#aaaaaa',
        usePointStyle: true,
        padding: 20,
        font: { size: 12 }
      }
    },
    tooltip: { backgroundColor: '#111111', titleColor: '#ffffff', bodyColor: '#ffffff', borderColor: '#333333', borderWidth: 1, padding: 12 }
  }
}

// Barras Direita (Fontes)
const barDataRight = ref({
  labels: ['Orgânico', 'Direto', 'Social', 'Ads', 'Referência'],
  datasets: [
    {
      data: [0, 0, 0, 0, 0],
      backgroundColor: (context: any) => {
        const chart = context.chart;
        const {ctx, chartArea} = chart;
        
        // Feedback Visual
        if (context.dataIndex !== undefined) {
           const label = context.chart.data.labels[context.dataIndex]
           if (filterSource.value !== 'all' && label !== filterSource.value) return '#222222'
        }

        if (!chartArea) return primaryColor;
        const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
        gradient.addColorStop(0, '#333333');
        gradient.addColorStop(1, primaryColor);
        return gradient;
      },
      borderRadius: 4,
      barThickness: 16
    }
  ]
})
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Markdown Styles */
.markdown-content :deep(p) {
  margin-bottom: 1rem;
}

.markdown-content :deep(p:last-child) {
  margin-bottom: 0;
}

.markdown-content :deep(strong) {
  color: #ffffff;
  font-weight: 700;
}

.markdown-content :deep(ul), .markdown-content :deep(ol) {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.markdown-content :deep(li) {
  margin-bottom: 0.5rem;
  list-style-type: disc;
}

.markdown-content :deep(h1), .markdown-content :deep(h2), .markdown-content :deep(h3) {
  color: #ffffff;
  font-weight: 700;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.markdown-content :deep(h1) { font-size: 1.25rem; }
.markdown-content :deep(h2) { font-size: 1.1rem; }
.markdown-content :deep(h3) { font-size: 1rem; }

.markdown-content :deep(code) {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-family: monospace;
  font-size: 0.85rem;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid var(--color-primary);
  padding-left: 1rem;
  margin: 1rem 0;
  background: rgba(255, 117, 31, 0.05);
  border-radius: 0 0.5rem 0.5rem 0;
  padding: 0.75rem 1rem;
}
</style>
