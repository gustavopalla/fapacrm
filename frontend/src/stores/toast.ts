import { defineStore } from 'pinia'
import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'info'

export const useToastStore = defineStore('toast', () => {
  const show = ref(false)
  const message = ref('')
  const type = ref<ToastType>('success')

  const notify = (msg: string, t: ToastType = 'success') => {
    message.value = msg
    type.value = t
    show.value = true
    
    setTimeout(() => {
      show.value = false
    }, 4000)
  }

  return { show, message, type, notify }
})
