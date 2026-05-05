<template>
  <Transition name="toast">
    <div v-if="toast.show" class="fixed bottom-10 right-10 z-[100] flex items-center gap-4 px-6 py-4 rounded-2xl bg-surface/80 backdrop-blur-xl border border-white/10 shadow-2xl shadow-primary/10 min-w-[320px]">
      <!-- Icon based on type -->
      <div class="flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center" :class="typeClasses[toast.type].bg">
        <component :is="typeClasses[toast.type].icon" class="w-5 h-5" :class="typeClasses[toast.type].text" />
      </div>
      
      <div class="flex-1">
        <p class="text-sm font-bold text-white leading-tight">
          {{ toast.message }}
        </p>
      </div>

      <button @click="toast.show = false" class="text-text-dim hover:text-white transition-colors">
        <XIcon class="w-4 h-4" />
      </button>

      <!-- Progress bar timer -->
      <div class="absolute bottom-0 left-0 h-1 bg-primary rounded-full transition-all duration-[4000ms] ease-linear" :style="{ width: toast.show ? '0%' : '100%' }"></div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { 
  CheckCircle as CheckIcon, 
  AlertCircle as ErrorIcon, 
  Info as InfoIcon,
  X as XIcon
} from 'lucide-vue-next'
import { useToastStore } from '../stores/toast'

const toast = useToastStore()

const typeClasses = {
  success: { bg: 'bg-green-500/10', text: 'text-green-400', icon: CheckIcon },
  error: { bg: 'bg-red-500/10', text: 'text-red-400', icon: ErrorIcon },
  info: { bg: 'bg-blue-500/10', text: 'text-blue-400', icon: InfoIcon }
}
</script>

<style scoped>
.toast-enter-active, .toast-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.toast-enter-from {
  transform: translateX(100px) scale(0.9);
  opacity: 0;
}
.toast-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style>
