import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = '/api/leads/'

export interface Lead {
  id: number
  nome_cliente: string
  nome_empresa: string
  telefone: string
  status: string
  nicho: string
  valor_estimado: number
  ultima_interacao: string
  proximo_contato: string | null
  notas: string
  motivo_espera: string
  tem_site: boolean
  nota_performance: number | null
  tem_pixel: boolean
  nota_google_meu_negocio: number | null
  project?: {
    valor_recorrente: number
    go_live: boolean
  }
  ga4_property_id?: string | null
}

export const useLeadStore = defineStore('leads', {
  state: () => ({
    leads: [] as Lead[],
    loading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchLeads() {
      this.loading = true
      try {
        const response = await axios.get(API_URL)
        this.leads = response.data
      } catch (err: any) {
        this.error = 'Erro ao carregar leads'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async updateLead(leadId: number, leadData: Partial<Lead>) {
      try {
        const response = await axios.patch(`${API_URL}${leadId}/`, leadData)
        const index = this.leads.findIndex(l => l.id === leadId)
        if (index !== -1) {
          this.leads[index] = { ...this.leads[index], ...response.data }
        }
        return response.data
      } catch (err) {
        console.error('Erro ao atualizar lead:', err)
        throw err
      }
    },
    async updateLeadStatus(leadId: number, newStatus: string) {
      return this.updateLead(leadId, { status: newStatus })
    },
    async deleteLead(leadId: number) {
      try {
        await axios.delete(`${API_URL}${leadId}/`)
        this.leads = this.leads.filter(l => l.id !== leadId)
      } catch (err) {
        console.error('Erro ao deletar lead:', err)
        throw err
      }
    },
    async createLead(leadData: Partial<Lead>) {
      try {
        const response = await axios.post(API_URL, leadData)
        this.leads.unshift(response.data)
        return response.data
      } catch (err) {
        console.error('Erro ao criar lead:', err)
        throw err
      }
    }
  }
})
