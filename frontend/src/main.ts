import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'

// Placeholder components for routes
const KanbanBoard = () => import('./components/KanbanBoard.vue')
const SalesGuide = () => import('./components/SalesGuide.vue')
const ProjectsView = () => import('./components/ProjectsView.vue')
const ClientsView = () => import('./components/ClientsView.vue')
const SettingsView = () => import('./components/SettingsView.vue')
const AnalyticsHub = () => import('./components/AnalyticsHub.vue')
const AnalyticsDashboard = () => import('./components/AnalyticsDashboard.vue')

const routes = [
  { path: '/', component: KanbanBoard },
  { path: '/guia', component: SalesGuide },
  { path: '/projetos', component: ProjectsView },
  { path: '/clientes', component: ClientsView },
  { path: '/analytics', component: AnalyticsHub },
  { path: '/analytics/:id', component: AnalyticsDashboard },
  { path: '/public/report/:id', component: AnalyticsDashboard, meta: { public: true } },
  { path: '/configuracoes', component: SettingsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
