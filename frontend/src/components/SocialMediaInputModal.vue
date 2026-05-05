<template>
  <div v-if="show" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
    <!-- Overlay -->
    <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="!isLoading && $emit('close')"></div>
    
    <!-- Modal Content -->
    <div class="relative bg-surface w-full max-w-lg rounded-3xl shadow-2xl border border-white/10 overflow-hidden flex flex-col animate-in">
      
      <!-- Header with Instagram Gradient Theme -->
      <div class="p-6 border-b border-white/5 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-r from-[#f09433] via-[#e6683c] to-[#bc1888] opacity-20"></div>
        <div class="relative flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center bg-gradient-to-tr from-[#f09433] via-[#e6683c] to-[#bc1888] text-white">
              <InstagramIcon class="w-5 h-5" />
            </div>
            <div>
              <h3 class="text-xl font-bold text-white">Relatório IA</h3>
              <p class="text-sm text-text-muted">Redes Sociais / Instagram</p>
            </div>
          </div>
          <button @click="!isLoading && $emit('close')" class="p-2 hover:bg-white/5 rounded-xl transition-colors">
            <XIcon class="w-5 h-5 text-text-muted hover:text-white" />
          </button>
        </div>
      </div>

      <!-- Body -->
      <div class="p-6 space-y-4">
        <div>
          <label class="block text-sm font-bold text-text-muted mb-2 uppercase tracking-wider">Métricas Brutas</label>
          <textarea 
            v-model="metrics" 
            class="w-full h-48 bg-black/20 border border-white/10 rounded-xl p-4 text-white placeholder:text-white/20 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 resize-none font-mono text-sm"
            placeholder="Cole aqui as métricas copiadas do Instagram Insights...&#10;&#10;Exemplo:&#10;Contas alcançadas: 15.340 (+12%)&#10;Contas com engajamento: 1.200&#10;Visitas ao perfil: 450&#10;Novos seguidores: +120"
            :disabled="isLoading"
          ></textarea>
        </div>
      </div>

      <!-- Footer -->
      <div class="p-6 border-t border-white/5 bg-black/20 flex justify-end gap-3">
        <button 
          @click="$emit('close')" 
          :disabled="isLoading"
          class="px-5 py-2.5 rounded-xl font-bold text-text-muted hover:text-white hover:bg-white/5 transition-colors"
        >
          Cancelar
        </button>
        <button 
          @click="generate" 
          :disabled="isLoading || !metrics.trim()"
          class="flex items-center gap-2 px-6 py-2.5 rounded-xl font-bold text-white transition-all shadow-lg hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:hover:scale-100 relative overflow-hidden group"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-[#f09433] via-[#e6683c] to-[#bc1888] group-hover:brightness-110 transition-all"></div>
          <div class="relative flex items-center gap-2">
            <SparklesIcon v-if="!isLoading" class="w-4 h-4" />
            <Loader2Icon v-else class="w-4 h-4 animate-spin" />
            <span>{{ isLoading ? 'Analisando...' : 'Gerar Relatório ✨' }}</span>
          </div>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Instagram as InstagramIcon, X as XIcon, Sparkles as SparklesIcon, Loader2 as Loader2Icon } from 'lucide-vue-next'

const props = defineProps<{
  show: boolean
  isLoading: boolean
}>()

const emit = defineEmits(['close', 'generate'])

const metrics = ref('')

const generate = () => {
  if (!metrics.value.trim()) return
  emit('generate', metrics.value)
}
</script>

<style scoped>
.animate-in {
  animation: animate-in 0.2s ease-out;
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
