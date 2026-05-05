<template>
  <div class="max-w-5xl mx-auto space-y-8 lg:space-y-12 pb-24 lg:pb-20">
    <!-- Hero Section -->
    <section class="text-center py-8 lg:py-12 relative overflow-hidden rounded-2xl lg:rounded-3xl bg-surface/30 border border-white/5">
      <div class="absolute inset-0 bg-gradient-to-tr from-primary/10 to-secondary/5 pointer-events-none"></div>
      <div class="relative z-10 px-4 lg:px-6">
        <span class="inline-block px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold tracking-widest uppercase mb-6">
          Guia do Vendedor de Sites
        </span>
        <h1 class="text-3xl lg:text-5xl font-bold mb-4 lg:mb-6 tracking-tight">
          Do zero ao seu <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">primeiro cliente</span>
        </h1>
        <p class="text-text-muted text-base lg:text-lg max-w-2xl mx-auto mb-6 lg:mb-10 leading-relaxed">
          Tudo que você precisa para vender sites para pequenos negócios locais — sem mimimi, sem teoria, só o que funciona.
        </p>
        
        <div class="flex flex-wrap justify-center gap-3">
          <div v-for="pill in heroPills" :key="pill" class="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-sm text-text-muted hover:border-primary/30 transition-colors">
            {{ pill }}
          </div>
        </div>
      </div>
    </section>

    <!-- Navigation Tabs -->
    <div class="sticky top-16 lg:top-24 z-30 bg-background/80 backdrop-blur-md border-b border-white/5 mb-6 lg:mb-8 -mx-4 px-4 lg:mx-0 lg:px-0">
      <nav class="flex overflow-x-auto no-scrollbar py-2 gap-2">
        <button 
          v-for="section in sections" 
          :key="section.id"
          @click="activeSection = section.id"
          class="flex-shrink-0 px-6 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 border"
          :class="activeSection === section.id 
            ? 'bg-primary/10 border-primary/30 text-primary' 
            : 'border-transparent text-text-muted hover:text-white hover:bg-white/5'"
        >
          {{ section.label }}
        </button>
      </nav>
    </div>

    <!-- Section Content -->
    <div class="space-y-8">
      <!-- Módulo 01: Clientes -->
      <div v-if="activeSection === 'clientes'" class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div class="space-y-4">
          <h2 class="text-3xl font-bold">Onde estão seus clientes</h2>
          <p class="text-text-muted leading-relaxed">
            O erro mais comum de quem está começando é tentar vender para qualquer um. Pequenos negócios locais são o filão perfeito: eles precisam de presença online, não têm grana para agências grandes, e estão ao seu redor.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 lg:gap-6">
          <div v-for="nicho in nichos" :key="nicho.title" class="glass-card p-8 group">
            <div class="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-3xl mb-6 group-hover:scale-110 transition-transform">
              {{ nicho.icon }}
            </div>
            <h3 class="text-xl font-bold mb-3">{{ nicho.title }}</h3>
            <p class="text-sm text-primary font-medium mb-4 uppercase tracking-wider">{{ nicho.sub }}</p>
            <p class="text-text-muted text-sm leading-relaxed">{{ nicho.description }}</p>
          </div>
        </div>

        <div class="space-y-6 bg-surface/50 p-4 lg:p-8 rounded-2xl lg:rounded-3xl border border-white/5">
          <h3 class="text-2xl font-bold">3 métodos que funcionam de verdade</h3>
          <div class="space-y-8">
            <div v-for="(method, index) in findMethods" :key="method.title" class="flex gap-6">
              <div class="flex-shrink-0 w-12 h-12 rounded-full border border-primary/30 flex items-center justify-center text-primary font-bold text-xl">
                {{ index + 1 }}
              </div>
              <div class="space-y-2">
                <h4 class="text-lg font-bold">{{ method.title }}</h4>
                <p class="text-text-muted text-sm leading-relaxed">{{ method.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Módulo 02: Precificação -->
      <div v-if="activeSection === 'preco'" class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div class="space-y-4">
          <h2 class="text-3xl font-bold text-center">Como precificar sem se desvalorizar</h2>
          <p class="text-text-muted text-center max-w-2xl mx-auto leading-relaxed">
            A dúvida clássica: "quanto cobro?" O erro é cobrar pelo seu tempo. Você deve cobrar pelo valor gerado para o cliente.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6 max-w-4xl mx-auto items-stretch">
          <div v-for="plan in pricingPlans" :key="plan.name" 
            class="glass-card p-8 flex flex-col relative overflow-hidden"
            :class="plan.highlight ? 'border-primary/50 bg-primary/5 ring-1 ring-primary/20' : ''">
            <div v-if="plan.highlight" class="absolute top-4 right-4 px-3 py-1 bg-primary text-white text-[10px] font-bold rounded-full tracking-widest uppercase">
              RECOMENDADO
            </div>
            <h3 class="text-sm font-bold text-text-muted uppercase tracking-widest mb-4">{{ plan.name }}</h3>
            <div class="mb-6">
              <span class="text-4xl font-bold text-white">{{ plan.price }}</span>
              <p class="text-text-muted text-sm mt-1">{{ plan.range }}</p>
            </div>
            <ul class="space-y-4 flex-1 mb-8">
              <li v-for="feature in plan.features" :key="feature" class="flex items-start gap-3 text-sm text-text-muted">
                <CheckCircleIcon class="w-5 h-5 text-primary flex-shrink-0" />
                {{ feature }}
              </li>
            </ul>
          </div>
        </div>

        <div class="bg-primary/10 border border-primary/20 rounded-2xl lg:rounded-3xl p-4 lg:p-8 flex flex-col sm:flex-row gap-4 lg:gap-6 items-start sm:items-center">
          <div class="w-16 h-16 rounded-2xl bg-primary/20 flex items-center justify-center text-3xl">🔄</div>
          <div>
            <h3 class="text-xl font-bold mb-2">Estratégia de recorrência</h3>
            <p class="text-text-muted text-sm leading-relaxed">
              Ofereça sempre um plano mensal após a entrega: hospedagem, atualizações de conteúdo, relatório de visitas e suporte. 
              <strong>R$150 a R$350/mês por cliente.</strong>
            </p>
          </div>
        </div>
      </div>

      <!-- Módulo 03: Abordagem -->
      <div v-if="activeSection === 'abordagem'" class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div class="space-y-4">
          <h2 class="text-3xl font-bold">Como abordar sem parecer vendedor</h2>
          <p class="text-text-muted leading-relaxed">
            Medo de vender vem de uma confusão: você acha que vai incomodar. Mas se o negócio deles não tem site e você tem a solução, você está fazendo um favor. Mude esse frame primeiro.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-bold flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center text-primary text-sm">P</div>
            Abordagem Presencial
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 lg:gap-6">
            <div v-for="(step, idx) in approachSteps" :key="idx" class="glass-card p-6 space-y-3">
              <div class="text-primary font-bold text-2xl opacity-50">{{ idx + 1 }}</div>
              <h4 class="font-bold">{{ step.title }}</h4>
              <p class="text-text-muted text-sm leading-relaxed">{{ step.description }}</p>
            </div>
          </div>
          
          <div class="relative group">
            <div class="absolute -top-3 left-6 px-3 py-1 bg-primary text-white text-[10px] font-bold rounded-full tracking-widest uppercase z-10">
              SCRIPT PRESENCIAL
            </div>
            <div class="bg-surface border-l-4 border-primary p-4 lg:p-8 rounded-r-2xl italic text-base lg:text-lg leading-relaxed text-text-muted group-hover:text-white transition-colors">
              "Oi, tudo bem! Eu vim aqui [tomar um café / me informar sobre] e aproveitei para perguntar — vocês têm algum site ou página onde as pessoas podem ver o cardápio e o horário de funcionamento? Porque fiz uma pesquisa rápida no Google aqui e não apareceu nada, o que é uma pena porque o lugar é ótimo."
            </div>
            <button @click="copyText('Oi, tudo bem! Eu vim aqui [tomar um café / me informar sobre] e aproveitei para perguntar — vocês têm algum site ou página onde as pessoas podem ver o cardápio e o horário de funcionamento? Porque fiz uma pesquisa rápida no Google aqui e não apareceu nada, o que é uma pena porque o lugar é ótimo.')" 
              class="absolute bottom-4 right-4 p-2 rounded-lg bg-white/5 hover:bg-white/10 text-text-muted hover:text-white transition-colors">
              <CopyIcon class="w-4 h-4" />
            </button>
          </div>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-bold flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-secondary/20 flex items-center justify-center text-secondary text-sm">W</div>
            WhatsApp / DM
          </h3>
          <div class="relative group">
            <div class="absolute -top-3 left-6 px-3 py-1 bg-secondary text-white text-[10px] font-bold rounded-full tracking-widest uppercase z-10">
              SCRIPT DIGITAL
            </div>
            <div class="bg-surface border-l-4 border-secondary p-4 lg:p-8 rounded-r-2xl italic text-base lg:text-lg leading-relaxed text-text-muted group-hover:text-white transition-colors">
              "Oi [Nome]! Vi o perfil de vocês aqui no Instagram e achei muito bacana o trabalho que fazem. Fiz uma pesquisa no Google por [tipo do negócio] aqui em [cidade] e percebi que vocês não aparecem — o que significa que muita gente que está procurando o serviço de vocês não está achando.<br><br>
              Sou especialista em criar sites para negócios locais aqui na região. Seria interessante pra você ter mais visibilidade no Google? Posso mostrar exatamente como funcionaria, sem compromisso."
            </div>
            <button @click="copyText('Oi [Nome]! Vi o perfil de vocês aqui no Instagram e achei muito bacana o trabalho que fazem. Fiz uma pesquisa no Google por [tipo do negócio] aqui em [cidade] e percebi que vocês não aparecem — o que significa que muita gente que está procurando o serviço de vocês não está achando.\n\nSou especialista em criar sites para negócios locais aqui na região. Seria interessante pra você ter mais visibilidade no Google? Posso mostrar exatamente como funcionaria, sem compromisso.')" 
              class="absolute bottom-4 right-4 p-2 rounded-lg bg-white/5 hover:bg-white/10 text-text-muted hover:text-white transition-colors">
              <CopyIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Módulo 04: Objeções -->
      <div v-if="activeSection === 'objecoes'" class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div class="space-y-4">
          <h2 class="text-3xl font-bold">Rebatendo objeções com confiança</h2>
          <p class="text-text-muted leading-relaxed">
            Objeção não é rejeição — é pedido de mais informação. Quando o cliente diz "tá caro" ele está dizendo "ainda não entendi o valor". Sua missão é ajudar ele a entender.
          </p>
        </div>

        <div class="grid gap-4">
          <div v-for="obj in objections" :key="obj.q" class="glass-card overflow-hidden">
            <div class="bg-red-500/10 p-5 border-b border-red-500/10 text-red-200 font-bold flex items-center gap-3">
              <MessageSquareXIcon class="w-5 h-5" />
              {{ obj.q }}
            </div>
            <div class="p-6 text-text-muted leading-relaxed">
              <div v-html="obj.a"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Módulo 07: Rotina -->
      <div v-if="activeSection === 'rotina'" class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div class="space-y-4">
          <h2 class="text-3xl font-bold text-center">Sua rotina de vendas semanal</h2>
          <p class="text-text-muted text-center max-w-2xl mx-auto leading-relaxed">
            Consistência bate talento toda vez. Aqui está o modelo mínimo viável para você começar.
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
          <div v-for="day in routine" :key="day.label" class="glass-card p-6 space-y-4">
            <div class="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-2xl">{{ day.icon }}</div>
            <h4 class="font-bold">{{ day.label }}</h4>
            <p class="text-primary text-[10px] font-bold uppercase tracking-widest">{{ day.sub }}</p>
            <p class="text-text-muted text-sm leading-relaxed">{{ day.description }}</p>
          </div>
        </div>

        <div class="glass-card p-10 bg-gradient-to-br from-primary/10 to-transparent text-center">
          <h3 class="text-3xl font-bold mb-4 text-white">Agora é só executar. 🔥</h3>
          <p class="text-text-muted mb-8 max-w-xl mx-auto">
            Você já tem o mapa. A única diferença entre quem vende e quem não vende é quem vai até o final da planilha de leads. Uma abordagem por dia muda sua vida em 30 dias.
          </p>
          <button @click="activeSection = 'clientes'" class="bg-primary hover:bg-primary/90 text-white px-8 py-3 rounded-2xl font-bold transition-all shadow-glow">
            Começar Garimpo
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { 
  CheckCircle as CheckCircleIcon,
  Copy as CopyIcon,
  MessageSquareX as MessageSquareXIcon
} from 'lucide-vue-next'
import { useToastStore } from '../stores/toast'

const toast = useToastStore()
const activeSection = ref('clientes')

const heroPills = [
  '🎯 Onde encontrar clientes',
  '💰 Como precificar',
  '🗣️ Scripts de abordagem',
  '🛡️ Rebater objeções'
]

const sections = [
  { id: 'clientes', label: '01 · Clientes' },
  { id: 'preco', label: '02 · Precificação' },
  { id: 'abordagem', label: '03 · Abordagem' },
  { id: 'objecoes', label: '04 · Objeções' },
  { id: 'rotina', label: '07 · Rotina' }
]

const nichos = [
  {
    icon: '🍕',
    title: 'Restaurantes',
    sub: 'Alto volume, dor clara',
    description: 'A maioria só tem perfil no Instagram mal feito. Precisam de cardápio online ou uma página que apareça no Google.'
  },
  {
    icon: '💆',
    title: 'Salões & Estética',
    sub: 'Agendamento online',
    description: 'O maior problema é o agendamento por WhatsApp que vira caos. Um site simples com botão de agendamento resolve.'
  },
  {
    icon: '🔧',
    title: 'Serviços Locais',
    sub: 'Visibilidade no Google',
    description: 'Encanadores, eletricistas, etc. Eles vivem de indicação, mas um site os faz aparecer quando alguém pesquisa "perto de mim".'
  }
]

const findMethods = [
  {
    title: 'Google Maps Hunting',
    description: 'Pesquise no Google Maps por negócios locais. Filtre por negócios sem site (aparecem sem link azul no perfil). Esses são seus leads quentes.'
  },
  {
    title: 'Mapeamento de rua',
    description: 'Ande pelos comércios da sua região. Pegue cartões de visita. Se não tiver site no cartão, é um lead quente para abordagem presencial.'
  },
  {
    title: 'Instagram sem link na bio',
    description: 'Procure perfis com muitos posts mas sem link de site na bio. Mande DM direta oferecendo visibilidade real.'
  }
]

const pricingPlans = [
  {
    name: 'Tráfego Orgânico',
    price: 'R$ 3.350',
    range: '',
    features: [
      'Landing page única (R$ 500)',
      'Suporte ao site e relatório de performance semanal (R$ 150/mês)',
      'SEO local (Google)',
      'Gestão do perfil Google Meu Negócio (R$ 200/mês)',
      'Pacote Social Media (R$ 2.500/mês)',
      '↳ Captação de vídeo / 30 reels por mês',
      '↳ Edição de vídeo',
      '↳ Social Media e Relatório do Instagram semanal'
    ]
  },
  {
    name: 'Tráfego Pago',
    price: 'A definir',
    range: '',
    highlight: true,
    features: [
      'Landing page única (R$ 500)',
      'Suporte ao site e relatório de performance semanal (R$ 150/mês)',
      'SEO local (Google)',
      'Gestão do perfil Google Meu Negócio (R$ 200/mês)',
      'Pacote Social Media (R$ 2.500/mês)',
      '↳ Captação de vídeo / 30 reels por mês',
      '↳ Edição de vídeo',
      '↳ Social Media e Relatório do Instagram semanal',
      '↳ Bônus Extra: Foto e Design',
      'Tráfego pago Meta Ads'
    ]
  }
]

const approachSteps = [
  {
    title: 'Entre como cliente',
    description: 'Vá ao estabelecimento normalmente. Consuma algo e observe os pontos que você poderia resolver.'
  },
  {
    title: 'Abra com observação',
    description: 'Não chegue falando "faço sites". Comente algo positivo sobre o negócio para quebrar a resistência.'
  },
  {
    title: 'Pergunta-gatilho',
    description: 'Faça a pergunta certa que deixa o cliente falar sobre a dor de não ser encontrado.'
  }
]

const objections = [
  {
    q: '💬 "Tá caro, não tenho orçamento agora."',
    a: '<strong>"Entendo. Se um novo cliente entrar por semana por causa do site, quanto isso representa em faturamento? O site se paga em poucas semanas. É investimento, não custo."</strong>'
  },
  {
    q: '💬 "Já tenho o Instagram, não preciso de site."',
    a: '<strong>"O Instagram é ótimo para quem já te segue. Mas quem pesquisa no Google não te acha por lá. Além disso, o site é seu, o Instagram pode te banir."</strong>'
  },
  {
    q: '💬 "Preciso pensar, vou ver com meu sócio."',
    a: '<strong>"Claro! Posso mandar um resumo por escrito do que discutimos para você mostrar para ele? Facilita a decisão."</strong>'
  }
]

const routine = [
  { icon: '📅', label: 'Segunda', sub: 'Prospecção', description: 'Pesquise 10 novos negócios locais sem site. Monte sua planilha.' },
  { icon: '📲', label: 'Terça e Quarta', sub: 'Abordagem', description: 'Envie mensagem ou ligue para 5 leads por dia. Siga o script.' },
  { icon: '🤝', label: 'Quinta', sub: 'Reunião', description: 'Faça diagnósticos e envie propostas para quem respondeu.' },
  { icon: '📊', label: 'Sexta', sub: 'Revisão', description: 'Conte seus números e ajuste sua meta para a próxima semana.' }
]

const copyText = (text: string) => {
  navigator.clipboard.writeText(text)
  toast.notify('Script copiado com sucesso!')
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
