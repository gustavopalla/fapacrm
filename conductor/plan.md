# Plano de Desenvolvimento do CRM Individual

## Objetivo
Criar um CRM leve, focado na gestão do funil de vendas (Kanban) e na transição direta para a entrega de projetos (sites/high-ticket). O sistema será otimizado para o fluxo de trabalho de um freelancer, com forte integração para automações via webhooks (n8n) e atualizações em tempo real (Supabase).

## Arquitetura Tecnológica
*   **Backend:** Python com Django e Django REST Framework (DRF).
*   **Banco de Dados:** PostgreSQL hospedado no Supabase (preparado para Realtime no futuro).
*   **Frontend:** Vue 3 (Composition API), Vite, Tailwind CSS.
*   **Gerenciamento de Estado (Vue):** Pinia.
*   **Ícones e Drag-and-Drop:** Lucide Vue Next, VueDraggable.
*   **Automações:** n8n (acionado via Webhooks do backend).

## Entidades e Modelos de Dados (Django)
1.  **Lead (Oportunidade)**
    *   Informações Básicas: Nome do Cliente, Nome da Empresa, Status (Coluna do Kanban), Valor Estimado.
    *   Diagnóstico: Tem site?, Nota de Performance (Google), Link Google Maps, Pixel Ativo?
    *   Controle: Última Interação, Próximo Contato.
2.  **Interaction/Note (Histórico)**
    *   Relacionado ao Lead. Armazena notas e log de conversas.
3.  **Task (Lembretes)**
    *   Tarefas de follow-up associadas a um Lead.
4.  **Project (Entrega)**
    *   Criado após o fechamento do Lead.
    *   Checklist de Entrega (Domínio, Setup, Design, Copy, Go-live).
    *   Repositório de Assets (Links Figma, GitHub, Credenciais).

## Componentes do Frontend (Vue 3)
*   `KanbanBoard.vue`: Container principal das colunas.
*   `KanbanColumn.vue`: Filtragem e renderização por status.
*   `LeadCard.vue`: Resumo visual com indicadores (ex: vermelho se estagnado).
*   `LeadDrawer.vue`: Painel lateral deslizante para edição rápida dos detalhes do Lead sem sair do funil.

## Automações e Integrações
*   **Webhooks Django:** Sinais (`post_save`) no Django que detectam mudanças de status (ex: "Proposta Enviada") e disparam dados para o n8n.
*   **n8n Workflow:** Recebe o payload do webhook, gera o contrato/proposta e notifica o usuário via Telegram.

## Roteiro de Desenvolvimento (Sprint Plan)

### Fase 1: O Alicerce (Semana 1)
1.  Inicializar e configurar o projeto backend Django.
2.  Instalar e configurar o Django REST Framework e CORS.
3.  Configurar a conexão com o banco de dados PostgreSQL (Supabase).
4.  Criar os Models (`Lead`, `Interaction`, `Task`, `Project`) e migrar o banco.
5.  Desenvolver os Serializers e as Views/ViewSets da API (GET, POST, PATCH).
6.  Inicializar o projeto frontend Vue 3 com Vite, Tailwind CSS, Pinia e VueRouter.

### Fase 2: O Visual (Semana 2)
1.  Estruturar o layout principal da aplicação (Sidebar, Topbar).
2.  Implementar o consumo da API (Axios/Fetch) para listar Leads.
3.  Desenvolver o componente `KanbanBoard` e implementar o Drag-and-Drop (`vuedraggable`).
4.  Desenvolver o formulário "Quick Add" para criar leads rapidamente.
5.  Criar o `LeadDrawer` para exibir e editar detalhes de um lead específico.

### Fase 3: Inteligência e Automação (Semana 3)
1.  Implementar a lógica de alertas visuais (Card vermelho após X dias sem `ultima_interacao`).
2.  Implementar o `post_save` no Django para disparar webhooks.
3.  Integrar campo "Próximo Passo" nos cards e formulários.
4.  Criar módulo financeiro simplificado (Controle de Parcelas, Calculadora de ROI baseada no valor e horas do projeto).

## Próximos Passos Imediatos (Após Aprovação)
Iniciaremos a **Fase 1** configurando os repositórios base para o Backend (Django) e Frontend (Vue 3).