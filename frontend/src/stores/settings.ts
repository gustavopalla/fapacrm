import { defineStore } from 'pinia'

export interface NicheConfig {
  id: string
  label: string
  script: string
}

export interface UserProfile {
  name: string
  role: string
  whatsappLink: string
}

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    profile: {
      name: 'Pedro Machado',
      role: 'Admin',
      whatsappLink: 'https://wa.me/5519974123403'
    } as UserProfile,
    niches: [
      {
        id: 'RESTAURANTE',
        label: 'Restaurantes & Lanchonetes',
        script: 'Oi! Vi o cardápio de vocês no Instagram, mas tive dificuldade de achar no Google. Sabia que muita gente desiste de pedir quando não acha um site oficial com horários?'
      },
      {
        id: 'ESTETICA',
        label: 'Salões & Estética',
        script: 'Olá! O trabalho de vocês é incrível. Notei que o agendamento é só pelo Whats, o que deve dar um trabalhão pra vocês. Um site com agendamento automático ajudaria muito, né?'
      },
      {
        id: 'SERVICOS',
        label: 'Prestadores de Serviço',
        script: 'Oi! Pesquisei por serviços como o seu na região e vocês não apareceram no topo. Um site focado em SEO local traria clientes qualificados todo dia pra vocês.'
      },
      {
        id: 'OUTROS',
        label: 'Outros',
        script: 'Oi! Vi que vocês têm uma presença forte no Instagram, mas ainda não têm um site próprio. Isso ajudaria muito na autoridade e a fechar mais vendas pelo Google.'
      }
    ] as NicheConfig[]
  }),
  actions: {
    loadSettings() {
      const savedProfile = localStorage.getItem('crm_profile')
      const savedNiches = localStorage.getItem('crm_niches')
      
      if (savedProfile) this.profile = JSON.parse(savedProfile)
      if (savedNiches) this.niches = JSON.parse(savedNiches)
    },
    saveProfile(newProfile: UserProfile) {
      this.profile = newProfile
      localStorage.setItem('crm_profile', JSON.stringify(this.profile))
    },
    saveNiches(newNiches: NicheConfig[]) {
      this.niches = newNiches
      localStorage.setItem('crm_niches', JSON.stringify(this.niches))
    },
    addNiche(niche: NicheConfig) {
      this.niches.push(niche)
      this.saveNiches(this.niches)
    },
    removeNiche(id: string) {
      this.niches = this.niches.filter(n => n.id !== id)
      this.saveNiches(this.niches)
    }
  }
})
