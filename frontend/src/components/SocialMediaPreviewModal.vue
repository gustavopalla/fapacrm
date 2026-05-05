<template>
  <div v-if="show" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
    <!-- Overlay -->
    <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="$emit('close')"></div>
    
    <!-- Modal Content -->
    <div class="relative bg-[#FAF7F0] w-full max-w-5xl max-h-[90vh] rounded-3xl shadow-2xl overflow-hidden flex flex-col animate-in">
      
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-[#1A1A1A]/10 bg-white shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center bg-gradient-to-tr from-[#f09433] via-[#e6683c] to-[#bc1888] text-white">
            <InstagramIcon class="w-6 h-6" />
          </div>
          <div>
            <h3 class="text-xl font-bold text-[#1A1A1A]">Relatório IA Social Media</h3>
            <p class="text-sm text-[#1A1A1A]/60">Análise gerada por IA</p>
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

      <!-- Report Content (Preview) -->
      <div ref="reportRef" class="flex-1 overflow-y-auto p-8 bg-[#FAF7F0]" v-html="htmlContent"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Instagram as InstagramIcon, X as XIcon, Download as DownloadIcon } from 'lucide-vue-next'

const props = defineProps<{
  show: boolean
  htmlContent: string
}>()

const emit = defineEmits(['close'])
const reportRef = ref<HTMLElement | null>(null)

// Abre uma NOVA JANELA com o HTML do relatório e imprime
const printReport = () => {
  if (!reportRef.value) return
  
  const html = reportRef.value.innerHTML
  const win = window.open('', '_blank', 'width=1100,height=800')
  if (!win) { alert('Permita pop-ups para exportar o PDF.'); return }
  
  win.document.write(`<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Relatório Social Media</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
  * { 
    margin: 0; padding: 0; box-sizing: border-box; 
    font-family: 'Inter', system-ui, sans-serif !important; 
    -webkit-print-color-adjust: exact !important; 
    print-color-adjust: exact !important; 
  }
  body { background: #FAF7F0; }
  
  .slide {
    margin-bottom: 40px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    border-radius: 10px;
    overflow: hidden;
  }

  /* Garantir que os slides ocupem a página inteira no print */
  @media print {
    body { padding: 0; background: white; }
    .slide {
      page-break-after: always;
      page-break-inside: avoid;
      min-height: 100vh !important;
      border: none !important;
      box-shadow: none !important;
      margin: 0 !important;
      border-radius: 0 !important;
    }
    .slide:last-child { page-break-after: auto; }
  }
</style>
</head>
<body>${html}</body>
</html>`)
  win.document.close()
  
  // Esperar carregar, depois imprimir
  setTimeout(() => {
    win.focus()
    win.print()
  }, 500)
}
</script>

<style scoped>
.animate-in {
  animation: animate-in 0.3s ease-out;
}

@keyframes animate-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
