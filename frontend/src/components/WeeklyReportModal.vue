<template>
  <div v-if="show && data" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
    <!-- Overlay -->
    <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="$emit('close')"></div>
    
    <!-- Modal -->
    <div class="relative bg-[#FAF7F0] w-full max-w-5xl max-h-[90vh] rounded-3xl shadow-2xl overflow-hidden flex flex-col animate-in">
      
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-[#1A1A1A]/10 bg-white shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-[#4CC23A] rounded-xl flex items-center justify-center">
            <FileTextIcon class="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 class="text-xl font-bold text-[#1A1A1A]">Relatório Estratégico</h3>
            <p class="text-sm text-[#1A1A1A]/60">Análise de performance semanal</p>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <button @click="printReport" class="flex items-center gap-2 bg-[#4CC23A] hover:bg-[#3A9E2C] text-white px-5 py-2.5 rounded-xl font-bold transition-all shadow-lg hover:scale-[1.02]">
            <DownloadIcon class="w-4 h-4" />
            Salvar PDF
          </button>
          <button @click="$emit('close')" class="p-2.5 hover:bg-black/5 rounded-xl transition-colors">
            <XIcon class="w-6 h-6 text-[#1A1A1A]" />
          </button>
        </div>
      </div>

      <!-- Slides -->
      <div ref="reportRef" class="flex-1 overflow-y-auto p-8 space-y-12 bg-[#FAF7F0]">
        
        <!-- CAPA -->
        <div class="slide-page bg-white rounded-3xl shadow-xl overflow-hidden flex flex-col min-h-[600px] border border-[#1A1A1A]/5">
          <div style="height:16px;background:#4CC23A;"></div>
          <div class="flex-1 flex flex-col items-center justify-center p-12 text-center">
            <div class="w-24 h-24 bg-white rounded-2xl flex items-center justify-center shadow-lg mb-8">
              <img src="/image.png" alt="FAPA" class="w-16 h-16 object-contain" />
            </div>
            <h1 style="font-size:2.25rem;font-weight:900;color:#1A1A1A;margin-bottom:1rem;text-transform:uppercase;letter-spacing:-0.05em;">{{ data.capa?.titulo || 'Relatório de Performance Digital' }}</h1>
            <div style="width:5rem;height:6px;background:#F5B916;margin-bottom:2rem;border-radius:3px;"></div>
            <p style="font-size:1.5rem;font-weight:700;color:#4CC23A;margin-bottom:0.5rem;">{{ data.capa?.cliente }}</p>
            <p style="font-size:1.125rem;color:#1A1A1A80;font-weight:500;">{{ data.capa?.periodo }}</p>
            
            <!-- KPIs da capa -->
            <div v-if="raw" style="display:flex;gap:1.5rem;margin-top:2.5rem;">
              <div style="text-align:center;padding:0.75rem 1.5rem;background:#FAF7F0;border-radius:0.75rem;border:1px solid #1A1A1A0D;">
                <p style="font-size:1.5rem;font-weight:900;color:#4CC23A;">{{ raw.metrics?.pageViews }}</p>
                <p style="font-size:0.625rem;font-weight:700;color:#1A1A1A66;text-transform:uppercase;letter-spacing:0.1em;">Visualizações</p>
              </div>
              <div style="text-align:center;padding:0.75rem 1.5rem;background:#FAF7F0;border-radius:0.75rem;border:1px solid #1A1A1A0D;">
                <p style="font-size:1.5rem;font-weight:900;color:#4CC23A;">{{ raw.metrics?.activeUsers }}</p>
                <p style="font-size:0.625rem;font-weight:700;color:#1A1A1A66;text-transform:uppercase;letter-spacing:0.1em;">Usuários Ativos</p>
              </div>
              <div style="text-align:center;padding:0.75rem 1.5rem;background:#FAF7F0;border-radius:0.75rem;border:1px solid #1A1A1A0D;">
                <p style="font-size:1.5rem;font-weight:900;" :style="{color: (raw.metrics?.growth || 0) >= 0 ? '#4CC23A' : '#ef4444'}">{{ (raw.metrics?.growth || 0) > 0 ? '+' : '' }}{{ raw.metrics?.growth || 0 }}%</p>
                <p style="font-size:0.625rem;font-weight:700;color:#1A1A1A66;text-transform:uppercase;letter-spacing:0.1em;">Crescimento</p>
              </div>
            </div>
          </div>
          <div style="padding:2rem;background:#FAF7F0;border-top:1px solid #1A1A1A0D;display:flex;justify-content:space-between;align-items:center;">
            <p style="font-size:0.875rem;font-weight:700;color:#1A1A1A66;text-transform:uppercase;letter-spacing:0.15em;">Assessoria Fapa • Inteligência de Dados</p>
            <p style="font-size:0.875rem;font-weight:700;color:#4CC23A;">PROJETADO PARA CRESCER</p>
          </div>
        </div>

        <!-- SLIDES DINÂMICOS -->
        <div v-for="(slide, index) in data.slides" :key="index" 
          class="slide-page bg-white rounded-3xl shadow-xl overflow-hidden flex flex-col min-h-[600px] border border-[#1A1A1A]/5">
          <div style="height:12px;background:#4CC23A;"></div>
          <div style="padding:3rem;flex:1;">
            <!-- Header -->
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.5rem;">
              <div>
                <p style="color:#4CC23A;font-weight:900;text-transform:uppercase;letter-spacing:0.15em;font-size:0.875rem;margin-bottom:0.5rem;">{{ slide.subtitulo }}</p>
                <h2 style="font-size:2.25rem;font-weight:900;color:#1A1A1A;letter-spacing:-0.025em;">{{ slide.titulo }}</h2>
              </div>
              <div style="background:#FAF7F0;padding:1rem 1.5rem;border-radius:1rem;border:1px solid #4CC23A33;">
                <p style="font-size:0.625rem;font-weight:700;color:#1A1A1A66;text-transform:uppercase;margin-bottom:0.25rem;">{{ gc(slide.destaque_label) || 'Indicador Chave' }}</p>
                <p style="font-size:1.5rem;font-weight:900;color:#4CC23A;">{{ gc(slide.destaque_valor) || gc(slide.destaque) }}</p>
              </div>
            </div>

            <!-- Mini KPIs -->
            <div v-if="raw" style="display:flex;gap:0.75rem;margin-bottom:1.5rem;">
              <template v-if="index === 0">
                <div class="mini-kpi"><p class="mini-val">{{ raw.metrics?.pageViews }}</p><p class="mini-lbl">Page Views</p></div>
                <div class="mini-kpi"><p class="mini-val">{{ raw.metrics?.activeUsers }}</p><p class="mini-lbl">Usuários</p></div>
                <div class="mini-kpi"><p class="mini-val">{{ (raw.metrics?.newUsersPercent || 0) }}%</p><p class="mini-lbl">Novos</p></div>
                <div class="mini-kpi"><p class="mini-val" :style="{color: (raw.metrics?.growth||0)>=0?'#4CC23A':'#ef4444'}">{{ (raw.metrics?.growth||0)>0?'+':'' }}{{ raw.metrics?.growth||0 }}%</p><p class="mini-lbl">Crescimento</p></div>
              </template>
              <template v-if="index === 1">
                <div class="mini-kpi"><p class="mini-val">{{ raw.metrics?.avgDuration }}</p><p class="mini-lbl">Duração Média</p></div>
                <div class="mini-kpi"><p class="mini-val">{{ raw.metrics?.bounceRate }}</p><p class="mini-lbl">Rejeição</p></div>
                <div class="mini-kpi"><p class="mini-val">{{ (raw.metrics?.newUsersPercent||0) }}%</p><p class="mini-lbl">Novos Usuários</p></div>
              </template>
              <template v-if="index === 2">
                <div class="mini-kpi"><p class="mini-val">{{ raw.devices?.mobile||0 }}%</p><p class="mini-lbl">Mobile</p></div>
                <div class="mini-kpi"><p class="mini-val">{{ raw.devices?.desktop||0 }}%</p><p class="mini-lbl">Desktop</p></div>
                <div class="mini-kpi"><p class="mini-val">{{ raw.devices?.tablet||0 }}%</p><p class="mini-lbl">Tablet</p></div>
              </template>
              <template v-if="index === 3">
                <div class="mini-kpi"><p class="mini-val">{{ raw.metrics?.pageViews }}</p><p class="mini-lbl">Views</p></div>
                <div class="mini-kpi"><p class="mini-val">{{ raw.metrics?.activeUsers }}</p><p class="mini-lbl">Ativos</p></div>
                <div class="mini-kpi"><p class="mini-val">{{ raw.metrics?.avgDuration }}</p><p class="mini-lbl">Duração</p></div>
                <div class="mini-kpi"><p class="mini-val" :style="{color:(raw.metrics?.growth||0)>=0?'#4CC23A':'#ef4444'}">{{ (raw.metrics?.growth||0)>0?'+':'' }}{{ raw.metrics?.growth||0 }}%</p><p class="mini-lbl">Crescimento</p></div>
              </template>
            </div>
            
            <!-- Conteúdo + Visão -->
            <div style="display:grid;grid-template-columns:7fr 5fr;gap:2rem;align-items:start;">
              <div>
                <div style="font-size:0.9375rem;color:#1A1A1ACC;font-weight:500;line-height:1.7;">
                  {{ gc(slide.conteudo) }}
                </div>
                <div v-if="gc(slide.recomendacao)" style="margin-top:1.5rem;display:flex;align-items:flex-start;gap:0.75rem;background:#F5B91619;border:1px solid #F5B91633;border-radius:0.75rem;padding:1rem 1.25rem;">
                  <span style="font-size:1.25rem;">✨</span>
                  <div>
                    <p style="font-size:0.625rem;font-weight:900;color:#F5B916;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.25rem;">Recomendação</p>
                    <p style="font-size:0.875rem;color:#1A1A1AB3;font-weight:500;">{{ gc(slide.recomendacao) }}</p>
                  </div>
                </div>
              </div>
              <div style="background:#FAF7F0;padding:2rem;border-radius:1.5rem;border:1px solid #1A1A1A0D;position:relative;overflow:hidden;">
                <span style="font-size:2rem;display:block;margin-bottom:1rem;">✨</span>
                <p style="font-size:1.125rem;font-weight:700;color:#1A1A1A;margin-bottom:0.5rem;">Visão do Analista</p>
                <p style="font-size:0.875rem;color:#1A1A1A99;font-style:italic;">"{{ gc(slide.visao_analista) || fallbackInsights[index] }}"</p>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div style="padding:1.5rem 2rem;border-top:1px solid #1A1A1A0D;display:flex;justify-content:space-between;align-items:center;">
            <p style="font-size:0.625rem;font-weight:700;color:#1A1A1A4D;text-transform:uppercase;letter-spacing:0.15em;">{{ data.capa?.cliente }} — Relatório Semanal</p>
            <span style="font-size:0.625rem;font-weight:700;color:#1A1A1A4D;">{{ String(index + 2).padStart(2, '0') }}/{{ String((data.slides?.length || 0) + 1).padStart(2, '0') }}</span>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { FileText as FileTextIcon, X as XIcon, Download as DownloadIcon } from 'lucide-vue-next'

const props = defineProps<{
  show: boolean
  data: any
}>()

const emit = defineEmits(['close'])
const reportRef = ref<HTMLElement | null>(null)
const raw = computed(() => props.data?.raw || null)

// Abre uma NOVA JANELA com o HTML do relatório e imprime a partir dela
const printReport = () => {
  if (!reportRef.value) return
  
  // 1. Pegar o HTML dos slides
  let html = reportRef.value.innerHTML
  
  // 2. Corrigir URLs de imagens (de relativo para absoluto)
  const origin = window.location.origin
  html = html.replace(/src="\/([^"]+)"/g, `src="${origin}/$1"`)
  
  // 3. Copiar TODOS os estilos da página atual (Tailwind, scoped, etc.)
  const allStyles: string[] = []
  document.querySelectorAll('style').forEach(s => {
    allStyles.push(s.innerHTML)
  })
  document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
    allStyles.push(`@import url("${(link as HTMLLinkElement).href}");`)
  })
  
  const win = window.open('', '_blank', 'width=1100,height=800')
  if (!win) { alert('Permita pop-ups para exportar o PDF.'); return }
  
  win.document.write(`<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>${props.data?.capa?.cliente || 'Relatório'} - Relatório Semanal</title>
<style>
  ${allStyles.join('\n')}
</style>
<style>
  * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
  body { margin: 0; padding: 2rem; background: #FAF7F0; font-family: 'Inter', -apple-system, sans-serif; }
  img { max-width: 100%; height: auto; }
  .slide-page { page-break-after: always; page-break-inside: avoid; }
  .slide-page:last-child { page-break-after: auto; }
  @media print {
    body { padding: 0; background: white; }
    .slide-page { border: none !important; box-shadow: none !important; border-radius: 0 !important; min-height: 100vh; margin: 0; }
  }
</style>
</head>
<body>${html}</body>
</html>`)
  win.document.close()
  
  // Esperar estilos e imagens carregarem
  setTimeout(() => {
    win.focus()
    win.print()
  }, 800)
}

const gc = (value: any): string => {
  if (!value) return ''
  if (Array.isArray(value)) return value.join(' ')
  return String(value)
}

const fallbackInsights = [
  'O tráfego demonstra que a presença digital está ativa e alcançando o público-alvo de forma consistente.',
  'O tempo de permanência indica que o conteúdo está capturando a atenção dos visitantes de forma eficiente.',
  'A diversificação de canais é um indicador positivo de alcance orgânico e posicionamento de marca.',
  'A estratégia atual demonstra fundamentos sólidos para escalar os resultados nas próximas semanas.'
]
</script>

<style scoped>
.animate-in {
  animation: animate-in 0.3s ease-out;
}
@keyframes animate-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
.mini-kpi {
  flex: 1;
  text-align: center;
  padding: 0.6rem 0.75rem;
  background: #FAF7F0;
  border-radius: 0.75rem;
  border: 1px solid #1A1A1A0D;
}
.mini-val {
  font-size: 1.125rem;
  font-weight: 900;
  color: #1A1A1A;
}
.mini-lbl {
  font-size: 0.5625rem;
  font-weight: 700;
  color: #1A1A1A59;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 0.125rem;
}
</style>
