from django.core.cache import cache
import os
import json
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from groq import Groq
from .models import Lead, Interaction, Task, Project
from .serializers import LeadSerializer, InteractionSerializer, TaskSerializer, ProjectSerializer
from . import ga4_auth, ga4_service

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-ultima_interacao')
    serializer_class = LeadSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Erro ao criar lead: {e}")
            print(error_details)
            return Response({
                "error": str(e),
                "details": error_details
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Erro ao listar leads: {e}")
            print(error_details)
            return Response({
                "error": str(e),
                "details": error_details
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def analytics_report(self, request, pk=None):
        lead = self.get_object()
        
        if not lead.ga4_property_id:
            return Response({
                "error": "no_property_id",
                "message": "Configure o GA4 Property ID para este cliente."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if not ga4_auth.is_authenticated():
            return Response({
                "error": "not_authenticated",
                "message": "A integração com o Google Analytics não está autorizada."
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        days = int(request.GET.get('days', '30'))
        
        # Buscar dados REAIS
        raw_data = ga4_service.get_full_report(lead.ga4_property_id, days)
        
        if not raw_data:
            return Response({
                "error": "api_error",
                "message": "Erro ao buscar dados do Google Analytics. Verifique o Property ID e as permissões."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        # Formatar para o que o frontend espera
        formatted_data = {
            "metrics": {
                **raw_data['metrics'],
                "realtimeActiveUsers": raw_data.get('realtimeActiveUsers', 0)
            },
            "top_pages": raw_data['topPages'],
            "top_cities": raw_data.get('topCities', []),
            "charts": {
                "line": {
                    "labels": raw_data['lineChart']['labels'],
                    "data": raw_data['lineChart']['data']
                },
                "devices": {
                    "data": [
                        raw_data['deviceBreakdown'].get('mobile', 0),
                        raw_data['deviceBreakdown'].get('desktop', 0),
                        raw_data['deviceBreakdown'].get('tablet', 0)
                    ]
                },
                "audience": {
                    "data": [
                        raw_data['audienceSplit'].get('new', 0),
                        raw_data['audienceSplit'].get('returning', 0)
                    ]
                },
                "sources": {
                    "labels": list(raw_data['sourceBreakdown'].keys()),
                    "data": list(raw_data['sourceBreakdown'].values())
                }
            }
        }
        return Response(formatted_data)

    @action(detail=True, methods=['get'])
    def analytics_insight(self, request, pk=None):
        lead = self.get_object()
        
        days = request.GET.get('days', '30')
        device = request.GET.get('device', 'all')
        audience = request.GET.get('audience', 'all')
        source = request.GET.get('source', 'all')

        # 1. Tentar buscar do CACHE para economizar tokens
        cache_key = f"ai_insight_{lead.id}_{days}_{device}_{audience}_{source}"
        cached_insight = cache.get(cache_key)
        if cached_insight:
            return Response({"insight": cached_insight, "cached": True})
        
        # 2. Tentar buscar dados REAIS para o prompt
        real_data = None
        if lead.ga4_property_id and ga4_auth.is_authenticated():
            real_data = ga4_service.get_full_report(lead.ga4_property_id, int(days))

        if real_data:
            metrics = real_data['metrics']
            prompt_data = {
                "page_views": metrics['pageViews'],
                "active_users": metrics['activeUsers'],
                "bounce_rate": metrics['bounceRate'],
                "avg_duration": metrics['avgDuration'],
                "new_vs_returning": f"{metrics['newUsersPercent']}% Novos"
            }
        else:
            # Fallback para mocks se não tiver GA4 configurado
            multiplier = 0.25 if days == '7' else (12 if days == '365' else 1)
            device_mod = 0.7 if device == 'mobile' else (0.3 if device == 'desktop' else 1)
            audience_mod = 0.72 if audience == 'new' else (0.28 if audience == 'returning' else 1)
            source_mod = 0.4 if source != 'all' else 1
            
            prompt_data = {
                "page_views": int(14285 * multiplier * device_mod * audience_mod * source_mod),
                "active_users": int(8492 * multiplier * device_mod * audience_mod * source_mod),
                "bounce_rate": "45.8%" if days == '7' else "42.3%",
                "avg_duration": "1m 20s" if days == '7' else "1m 45s",
                "new_vs_returning": "100% Novos" if audience == 'new' else ("100% Retornantes" if audience == 'returning' else ("65% Novos" if days == '7' else "72% Novos"))
            }

        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        def fmt(n):
            return f"{n:,.0f}".replace(",", ".")
        
        prompt = f"""Analise os seguintes dados de desempenho do site nos últimos {days} dias:
        - Visualizações de página: {fmt(prompt_data['page_views'])} visualizações
        - Usuários ativos: {fmt(prompt_data['active_users'])} usuários
        - Taxa de Rejeição: {prompt_data['bounce_rate']}
        - Tempo médio de sessão: {prompt_data['avg_duration']}
        - Retenção: {prompt_data['new_vs_returning']}
        
        Escreva exatamente 2 frases curtas em português analisando o desempenho. Cite os números EXATAMENTE como estão acima. NÃO comece com saudações. Comece direto pela análise.
        """
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            insight = chat_completion.choices[0].message.content
            
            # Salvar no cache por 1 hora (3600 segundos)
            cache.set(cache_key, insight, 3600)
            
            return Response({"insight": insight, "cached": False})
        except Exception:
            fallback = "O tráfego demonstra estabilidade. A retenção está dentro do esperado para o período analisado."
            return Response({"insight": fallback})

    @action(detail=True, methods=['post'])
    def analytics_chat(self, request, pk=None):
        lead = self.get_object()
        user_question = request.data.get('question', '')
        dashboard_data = request.data.get('dashboard_data', {})
        
        if not user_question:
            return Response({"answer": "Por favor, digite uma pergunta."}, status=400)
        
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        system_prompt = f"""Você é a assistente de analytics da Assessoria Fapa. Analisando site de '{lead.nome_empresa or lead.nome_cliente}'.
        REGRAS: 1. Português BR. 2. Direta com números. 3. Máximo 4 frases. 4. Sem markdown."""

        context = f"""DADOS DO DASHBOARD:
        - PageViews: {dashboard_data.get('pageViews')}
        - ActiveUsers: {dashboard_data.get('activeUsers')}
        - BounceRate: {dashboard_data.get('bounceRate')}
        - AvgDuration: {dashboard_data.get('avgDuration')}
        - Growth: {dashboard_data.get('growth')}%
        - NewUsers: {dashboard_data.get('newUsersPercent')}%
        - Top Pages: {dashboard_data.get('topPages', 'Não informado')}
        - Cidades: {dashboard_data.get('topCities', 'Não informado')}"""

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{context}\n\nPergunta: {user_question}"}
                ],
                model="llama-3.1-8b-instant",
            )
            return Response({"answer": chat_completion.choices[0].message.content})
        except Exception:
            return Response({"answer": "Erro ao processar sua pergunta."})

    @action(detail=True, methods=['get'])
    def weekly_report(self, request, pk=None):
        from datetime import datetime, timedelta
        lead = self.get_object()
        days = 7
        
        real_data = None
        if lead.ga4_property_id and ga4_auth.is_authenticated():
            real_data = ga4_service.get_full_report(lead.ga4_property_id, days)

        if not real_data:
            return Response({"error": "No data available"}, status=400)

        metrics = real_data['metrics']
        top_pages = real_data.get('topPages', [])
        devices = real_data.get('deviceBreakdown', {})
        sources = real_data.get('sourceBreakdown', {})
        audience = real_data.get('audienceSplit', {})
        
        # Período formatado
        hoje = datetime.now()
        inicio = hoje - timedelta(days=7)
        periodo_str = f"{inicio.strftime('%d/%m/%Y')} a {hoje.strftime('%d/%m/%Y')}"
        nome_cliente = lead.nome_empresa or lead.nome_cliente

        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        prompt = f"""Você é um analista de métricas sênior da Assessoria Fapa. Gere um relatório semanal para apresentar ao cliente '{nome_cliente}'.

OBJETIVO: Mostrar ao cliente que o site ESTÁ FUNCIONANDO e gerando resultados. O tom deve ser positivo, estratégico e valorizar cada métrica. Mesmo números pequenos devem ser apresentados como progresso real.

PERÍODO: {periodo_str}

DADOS REAIS:
- Visualizações de Página: {metrics['pageViews']}
- Usuários Ativos: {metrics['activeUsers']}
- Taxa de Rejeição: {metrics['bounceRate']}
- Duração Média: {metrics['avgDuration']}
- Crescimento: {metrics['growth']}%
- Novos Usuários: {metrics['newUsersPercent']}%
- Dispositivos: Mobile {devices.get('mobile', 0)}%, Desktop {devices.get('desktop', 0)}%, Tablet {devices.get('tablet', 0)}%
- Origens: {', '.join([f'{k}: {v}' for k, v in sources.items()])}
- Público: {audience.get('new', 0)} novos, {audience.get('returning', 0)} retornantes
- Top Páginas: {', '.join([f"{p['path']} ({p['views']} views)" for p in top_pages[:3]])}

REGRAS DO JSON:
1. TODOS os campos devem ser STRINGS simples (nunca arrays)
2. "conteudo" = parágrafo com 2-3 frases estratégicas mostrando valor ao cliente
3. "visao_analista" = frase ÚNICA e DIFERENTE para cada slide, com insight exclusivo daquele tema
4. "recomendacao" = 1 frase de ação sugerida
5. "destaque_valor" e "destaque_label" = strings curtas
6. Gere EXATAMENTE 4 slides
7. Linguagem profissional e positiva

JSON:
{{
  "capa": {{
    "titulo": "Relatório de Performance Digital",
    "subtitulo": "Análise Estratégica Semanal",
    "periodo": "{periodo_str}",
    "cliente": "{nome_cliente}"
  }},
  "slides": [
    {{
      "titulo": "Tráfego & Alcance",
      "subtitulo": "Volume de acessos no período",
      "destaque_valor": "...",
      "destaque_label": "...",
      "conteudo": "...",
      "visao_analista": "...",
      "recomendacao": "..."
    }},
    {{
      "titulo": "Comportamento do Usuário",
      "subtitulo": "Engajamento e qualidade",
      "destaque_valor": "...",
      "destaque_label": "...",
      "conteudo": "...",
      "visao_analista": "...",
      "recomendacao": "..."
    }},
    {{
      "titulo": "Canais & Dispositivos",
      "subtitulo": "De onde vem seu público",
      "destaque_valor": "...",
      "destaque_label": "...",
      "conteudo": "...",
      "visao_analista": "...",
      "recomendacao": "..."
    }},
    {{
      "titulo": "Próximos Passos",
      "subtitulo": "Estratégia para a próxima semana",
      "destaque_valor": "...",
      "destaque_label": "...",
      "conteudo": "...",
      "visao_analista": "...",
      "recomendacao": "..."
    }}
  ]
}}"""
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                response_format={"type": "json_object"}
            )
            report = json.loads(chat_completion.choices[0].message.content)
            
            # Injetar dados brutos para o frontend usar nos gráficos do PDF
            # Normalizar: se a IA retornou arrays em vez de strings, juntar
            for slide in report.get('slides', []):
                for key in ['conteudo', 'recomendacao', 'visao_analista', 'destaque_valor', 'destaque_label', 'destaque']:
                    if isinstance(slide.get(key), list):
                        slide[key] = ' '.join(str(item) for item in slide[key])
            
            report['raw'] = {
                'metrics': metrics,
                'devices': devices,
                'sources': sources,
                'audience': audience,
                'topPages': top_pages,
            }
            return Response(report)
        except Exception as e:
            print(f"Erro weekly_report Groq: {e}")
            return Response({"error": "AI failure"}, status=500)

class AnalyticsViewSet(viewsets.ViewSet):
    """ViewSet para gerenciar a autenticação global do GA4."""
    
    @action(detail=False, methods=['get'])
    def status(self, request):
        return Response({
            "authenticated": ga4_auth.is_authenticated(),
            "has_client_secret": ga4_auth._find_client_secret() is not None
        })

    @action(detail=False, methods=['get'])
    def authorize(self, request):
        creds = ga4_auth.get_credentials()
        if creds:
            return Response({"status": "success", "message": "Autenticado com sucesso!"})
        return Response({"status": "error", "message": "Falha na autenticação."}, status=400)

    @action(detail=False, methods=['post'])
    def social_media_report(self, request):
        metrics = request.data.get('metrics', '')
        if not metrics:
            return Response({"error": "Nenhuma métrica fornecida"}, status=400)
            
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        prompt = f"""Você é um analista Sênior e Desenvolvedor Front-end. Crie um relatório de Social Media em HTML puro (single-file) altamente denso, analítico e 100% responsivo.
NUNCA use blocos markdown (```html) e NUNCA use asteriscos (**). Retorne APENAS o código HTML.

DADOS REAIS PARA O RELATÓRIO:
{metrics}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. REGRAS DE RESPONSIVIDADE E CSS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Inclua `<meta name="viewport" content="width=device-width, initial-scale=1">` no `<head>`.
- Use CSS Grid para os cards: `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));`.
- Breakpoints:
  @media (max-width: 480px) {{ grid para 1 coluna; padding 16px; tabelas e barras horizontais devem se adaptar para não gerar scroll. }}
  @media (min-width: 481px) {{ padding 24px-40px. }}
- Importe Google Fonts: 'DM Sans' (Títulos) e 'Inter' (Textos).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. PALETA DE CORES E DESIGN OBRIGATÓRIOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Verde Principal: #4CAF50
- Verde Escuro: #2E7D32
- Preto Suave: #1A1A1A
- Fundo: #F9FAFB. Cards: #FFFFFF.
- Vermelho (apenas para quedas): #E53935

ESTILO DOS CARDS DE MÉTRICA:
Fundo branco, sombra sutil (`box-shadow: 0 1px 3px rgba(0,0,0,0.08)`), `border-left: 4px solid #4CAF50`, border-radius 12px.
Regra de Número: NÚMERO COMPLETO → SETA DEPOIS. Exemplo: `<span style="font-size: 48px; font-weight: 900; color: #4CAF50;">45,1% ↑</span>`
Label abaixo: 10px, uppercase, #757575.

PLACEHOLDERS PENDENTES:
Se faltar dados exatos do cliente, envolva em: `<span style="background:#FEF08A; border:1px dashed #EAB308; padding:2px; border-radius:4px;">[dado]</span>`. Nunca use a agência como cliente.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. ESTRUTURA SEMÂNTICA DAS PÁGINAS/SEÇÕES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cada seção deve ser uma `<section>` com `min-height: 100vh; display: flex; flex-direction: column; page-break-after: always; box-sizing: border-box;`.

HEADER FIXO (Em todas as seções exceto capa):
Faixa altura 50px, fundo `#2E7D32`, texto branco, display flex. Esquerda: Logo/Ícone. Centro: Nome da Seção. Direita: Período.

FOOTER FIXO (Em todas as seções):
Texto 10px #757575: "Assessoria Fapa · Dados: Meta Business Suite · Página X de 7".

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. CONTEÚDO OBRIGATÓRIO (ALTA DENSIDADE VISUAL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SEÇÃO 1: CAPA
- Topo: Logo "Assessoria Fapa" + linha verde separadora.
- Centro: Título "RELATÓRIO ESTRATÉGICO", Subtítulo "Performance de Social Media".
- Bloco verde escuro (#2E7D32) com Nome do Cliente (gigante) e Período.
- Fundo da página: Bloco escuro (#1A1A1A) com 4 métricas resumidas.
- Rodapé com nome do analista e data.

SEÇÃO 2: RESUMO EXECUTIVO
- 4 Cards de métricas no topo (CSS Grid).
- Gráfico de barras horizontais em CSS comparando períodos. NUNCA USE TABELAS.
- Interpretação densa (mínimo 4 linhas de análise de negócio).

SEÇÃO 3: ALCANCE E CRESCIMENTO (Ícone 👁️)
- Barras CSS comparativas.
- Análise explicando a queda/aumento baseada na frequência de posts.
- Card isolado mostrando a variação nas Visitas ao Perfil.

SEÇÃO 4: ENGAJAMENTO (Ícone ❤️)
- Elemento visual comparando a Média do Setor (Ex: 4,5%) vs O Cliente (Ex: 5,8%). Badge indicando quanto está acima da média.
- Contextualizar o número de impressões.

SEÇÃO 5: CONVERSÃO (Ícone 🖱️)
- Comparativo visual de cliques no link e visitas.
- Traduzir para o negócio: "X cliques = X potenciais clientes. Intenção de compra real."
- Recomendação de CTA direto.

SEÇÃO 6: PRÓXIMOS PASSOS (Ícone 🎯)
Copie EXATAMENTE estas 3 ações:
1. Publicar 3 reels por semana mostrando bastidores. Por quê: gerou 68% do alcance. Meta: Manter alcance acima de 12.000 em maio.
2. Adicionar CTA claro "Link na bio". Por quê: 272 cliques mostram intenção de compra. Meta: 350+ toques.
3. Criar 2 posts por semana com ofertas. Por quê: conversão 3x maior. Meta: Recuperar visitas para >800.
"""

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
            )
            
            html_content = chat_completion.choices[0].message.content
            # Remove possible markdown blocks
            html_content = html_content.replace('```html', '').replace('```', '').strip()
            
            return Response({"html": html_content})
        except Exception as e:
            print(f"Erro ao gerar relatório de social media: {e}")
            return Response({"error": "Falha na geração com IA"}, status=500)
class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
