"""
Serviço de consulta à Google Analytics 4 Data API.

Realiza queries reais na API do GA4 usando as credenciais OAuth
e retorna dados formatados prontos para o frontend consumir.
"""
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    RunRealtimeReportRequest,
    DateRange,
    Dimension,
    Metric,
    FilterExpression,
    Filter,
)

from .ga4_auth import get_credentials


def _create_client():
    """Cria o cliente da API do GA4 com as credenciais OAuth."""
    creds = get_credentials()
    if not creds:
        return None
    return BetaAnalyticsDataClient(credentials=creds)


def _format_duration(seconds):
    """Formata segundos em 'Xm Ys'."""
    if seconds is None or seconds == 0:
        return "0m 0s"
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}m {secs:02d}s"


def _format_bounce_rate(rate):
    """Formata bounce rate como porcentagem."""
    if rate is None:
        return "0%"
    return f"{rate:.1f}%".replace('.', ',')


def get_realtime_active_users(property_id):
    """
    Busca o número de usuários ativos nos últimos 30 minutos (Realtime).
    """
    client = _create_client()
    if not client:
        return 0
    
    try:
        response = client.run_realtime_report(RunRealtimeReportRequest(
            property=f"properties/{property_id}",
            metrics=[Metric(name="activeUsers")],
        ))
        
        if response.rows:
            return int(response.rows[0].metric_values[0].value or 0)
    except Exception as e:
        print(f"⚠️ Erro ao buscar realtime (Property: {property_id}): {e}")
    
    return 0


def get_full_report(property_id, days=30):
    """
    Busca o relatório completo de analytics para um Property ID.
    
    Retorna todos os dados necessários para a dashboard:
    - Métricas principais (pageViews, activeUsers, etc.)
    - Dados para gráfico de linha (evolução diária)
    - Breakdown por dispositivo
    - Breakdown por origem de tráfego
    - Páginas mais acessadas
    - Split novos vs retornantes
    
    Args:
        property_id: ID da propriedade GA4 (string de números)
        days: Número de dias para o período (7, 30, 365)
    
    Returns:
        dict com todos os dados formatados, ou None se falhar
    """
    client = _create_client()
    if not client:
        return None

    property_name = f"properties/{property_id}"
    start_date = f"{days}daysAgo"
    
    try:
        result = {}
        
        # ===== 1. MÉTRICAS PRINCIPAIS (COM COMPARAÇÃO) =====
        try:
            # Período Atual
            metrics_response = client.run_report(RunReportRequest(
                property=property_name,
                date_ranges=[DateRange(start_date=start_date, end_date="today")],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="activeUsers"),
                    Metric(name="bounceRate"),
                    Metric(name="userEngagementDuration"),
                    Metric(name="sessions"),
                    Metric(name="newUsers"),
                ],
            ))
            
            # Período Anterior (para cálculo de growth)
            prev_start = f"{days * 2}daysAgo"
            prev_end = f"{days}daysAgo"
            prev_response = client.run_report(RunReportRequest(
                property=property_name,
                date_ranges=[DateRange(start_date=prev_start, end_date=prev_end)],
                metrics=[Metric(name="screenPageViews")],
            ))

            current = {'pageViews': 0, 'activeUsers': 0, 'bounceRate': 0, 'duration': 0, 'sessions': 1, 'newUsers': 0}
            if metrics_response.rows:
                row = metrics_response.rows[0]
                current['pageViews'] = int(row.metric_values[0].value or 0)
                current['activeUsers'] = int(row.metric_values[1].value or 0)
                # GA4 bounceRate can be 0-1 or 0-100 depending on the property. We'll handle it.
                br_val = float(row.metric_values[2].value or 0)
                current['bounceRate'] = br_val if br_val > 1 else br_val * 100
                current['duration'] = float(row.metric_values[3].value or 0)
                current['sessions'] = int(row.metric_values[4].value or 1) or 1
                current['newUsers'] = int(row.metric_values[5].value or 0)

            prev_page_views = 0
            if prev_response.rows:
                prev_page_views = int(prev_response.rows[0].metric_values[0].value or 0)
            
            growth = 0
            if prev_page_views > 0:
                growth = round(((current['pageViews'] - prev_page_views) / prev_page_views) * 100, 1)

            result['metrics'] = {
                'pageViews': current['pageViews'],
                'activeUsers': current['activeUsers'],
                'growth': growth,
                'growthUsers': 0, # Reservado para usuários se necessário
                'newUsersPercent': round((current['newUsers'] / current['activeUsers']) * 100) if current['activeUsers'] > 0 else 0,
                'avgDuration': _format_duration(current['duration'] / current['activeUsers']) if current['activeUsers'] > 0 else "0m 0s",
                'bounceRate': f"{current['bounceRate']:.1f}%".replace('.', ','),
            }
        except Exception as e:
            print(f"⚠️ Erro no Bloco 1 (Métricas): {e}")
            result['metrics'] = {'pageViews': 0, 'activeUsers': 0, 'growth': 0, 'growthUsers': 0, 'newUsersPercent': 0, 'avgDuration': "0m 0s", 'bounceRate': "0%"}
        
        # ===== 2. GRÁFICO DE LINHA (Evolução diária) =====
        try:
            line_response = client.run_report(RunReportRequest(
                property=property_name,
                date_ranges=[DateRange(start_date=start_date, end_date="today")],
                dimensions=[Dimension(name="date")],
                metrics=[Metric(name="screenPageViews")],
                order_bys=[{
                    "dimension": {"dimension_name": "date", "order_type": "ALPHANUMERIC"},
                }],
            ))
            
            line_labels = []
            line_data = []
            if line_response.rows:
                for row in sorted(line_response.rows, key=lambda r: r.dimension_values[0].value):
                    date_str = row.dimension_values[0].value  # YYYYMMDD
                    try:
                        dt = datetime.strptime(date_str, "%Y%m%d")
                        if days <= 7:
                            day_names = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
                            line_labels.append(day_names[dt.weekday()])
                        else:
                            line_labels.append(dt.strftime("%d/%m"))
                    except ValueError:
                        line_labels.append(date_str)
                    line_data.append(int(row.metric_values[0].value or 0))
            
            result['lineChart'] = {
                'labels': line_labels,
                'data': line_data,
            }
        except Exception as e:
            print(f"⚠️ Erro no Bloco 2 (Linha): {e}")
            result['lineChart'] = {'labels': [], 'data': []}
        
        # ===== 3. BREAKDOWN POR DISPOSITIVO =====
        try:
            device_response = client.run_report(RunReportRequest(
                property=property_name,
                date_ranges=[DateRange(start_date=start_date, end_date="today")],
                dimensions=[Dimension(name="deviceCategory")],
                metrics=[Metric(name="sessions")],
            ))
            
            device_data = {'mobile': 0, 'desktop': 0, 'tablet': 0}
            device_total = 0
            if device_response.rows:
                for row in device_response.rows:
                    category = row.dimension_values[0].value.lower()
                    count = int(row.metric_values[0].value or 0)
                    device_total += count
                    if category in device_data:
                        device_data[category] = count
            
            if device_total > 0:
                device_data = {k: round((v / device_total) * 100) for k, v in device_data.items()}
            
            result['deviceBreakdown'] = device_data
        except Exception as e:
            print(f"⚠️ Erro no Bloco 3 (Dispositivos): {e}")
            result['deviceBreakdown'] = {'mobile': 0, 'desktop': 0, 'tablet': 0}
        
        # ===== 4. BREAKDOWN POR ORIGEM DE TRÁFEGO =====
        try:
            source_response = client.run_report(RunReportRequest(
                property=property_name,
                date_ranges=[DateRange(start_date=start_date, end_date="today")],
                dimensions=[Dimension(name="sessionDefaultChannelGroup")],
                metrics=[Metric(name="sessions")],
            ))
            
            source_map = {}
            source_translations = {
                'Organic Search': 'Orgânico',
                'Direct': 'Direto',
                'Organic Social': 'Social',
                'Paid Search': 'Ads',
                'Referral': 'Referência',
                'Email': 'Email',
                'Paid Social': 'Social Pago',
                'Display': 'Display',
                'Unassigned': 'Outros',
            }
            
            if source_response.rows:
                for row in source_response.rows:
                    source_name = row.dimension_values[0].value
                    translated = source_translations.get(source_name, source_name)
                    count = int(row.metric_values[0].value or 0)
                    source_map[translated] = source_map.get(translated, 0) + count
            
            result['sourceBreakdown'] = dict(sorted(source_map.items(), key=lambda x: x[1], reverse=True))
        except Exception as e:
            print(f"⚠️ Erro no Bloco 4 (Fontes): {e}")
            result['sourceBreakdown'] = {}
        
        # ===== 5. PÁGINAS MAIS ACESSADAS =====
        try:
            pages_response = client.run_report(RunReportRequest(
                property=property_name,
                date_ranges=[DateRange(start_date=start_date, end_date="today")],
                dimensions=[Dimension(name="pagePath")],
                metrics=[Metric(name="screenPageViews")],
                limit=10,
                order_bys=[{
                    "metric": {"metric_name": "screenPageViews"},
                    "desc": True,
                }],
            ))
            
            top_pages = []
            total_page_views = result.get('metrics', {}).get('pageViews', 1) or 1
            if pages_response.rows:
                for row in pages_response.rows[:5]:  # Top 5
                    views = int(row.metric_values[0].value or 0)
                    top_pages.append({
                        'path': row.dimension_values[0].value,
                        'views': views,
                        'percent': round((views / total_page_views) * 100) if total_page_views > 0 else 0,
                    })
            
            result['topPages'] = top_pages
        except Exception as e:
            print(f"⚠️ Erro no Bloco 5 (Páginas): {e}")
            result['topPages'] = []
        
        # ===== 6. NOVOS VS RETORNANTES =====
        try:
            audience_response = client.run_report(RunReportRequest(
                property=property_name,
                date_ranges=[DateRange(start_date=start_date, end_date="today")],
                dimensions=[Dimension(name="newVsReturning")],
                metrics=[Metric(name="activeUsers")],
            ))
            
            audience_data = {'new': 0, 'returning': 0}
            if audience_response.rows:
                for row in audience_response.rows:
                    audience_type = row.dimension_values[0].value.lower()
                    count = int(row.metric_values[0].value or 0)
                    if audience_type in audience_data:
                        audience_data[audience_type] = count
            
            result['audienceSplit'] = audience_data
        except Exception as e:
            print(f"⚠️ Erro no Bloco 6 (Audiência): {e}")
            result['audienceSplit'] = {'new': 0, 'returning': 0}

        # ===== 8. CIDADES =====
        try:
            city_response = client.run_report(RunReportRequest(
                property=property_name,
                date_ranges=[DateRange(start_date=start_date, end_date="today")],
                dimensions=[Dimension(name="city")],
                metrics=[Metric(name="activeUsers")],
                limit=10,
                order_bys=[{
                    "metric": {"metric_name": "activeUsers"},
                    "desc": True,
                }],
            ))
            
            top_cities = []
            if city_response.rows:
                for row in city_response.rows[:5]:  # Top 5
                    city = row.dimension_values[0].value
                    users = int(row.metric_values[0].value or 0)
                    # GA4 sometimes returns '(not set)' for unknown cities
                    if city != '(not set)':
                        top_cities.append({
                            'city': city,
                            'users': users
                        })
            
            result['topCities'] = top_cities
        except Exception as e:
            print(f"⚠️ Erro no Bloco 8 (Cidades): {e}")
            result['topCities'] = []
        
        # ===== 7. REALTIME (EXTRA) =====
        result['realtimeActiveUsers'] = get_realtime_active_users(property_id)
        
        return result
        
    except Exception as e:
        print(f"❌ Erro ao buscar dados do GA4 (Property: {property_id}): {e}")
        import traceback
        traceback.print_exc()
        return None
