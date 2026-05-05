
import os
import django

# Setup Django
import sys
sys.path.append('/Users/gustavopallaagostinho/Downloads/MyCRM/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.ga4_service import _create_client
from google.analytics.data_v1beta.types import RunRealtimeReportRequest, Metric

def test_realtime():
    # Get a lead with a property ID
    from crm.models import Lead
    lead = Lead.objects.filter(ga4_property_id__isnull=False).first()
    if not lead:
        print("No lead with GA4 Property ID found")
        return

    print(f"Testing Realtime for Lead: {lead.nome_cliente} (Property: {lead.ga4_property_id})")
    
    client = _create_client()
    if not client:
        print("Failed to create GA4 client")
        return

    try:
        response = client.run_realtime_report(RunRealtimeReportRequest(
            property=f"properties/{lead.ga4_property_id}",
            metrics=[Metric(name="activeUsers")],
        ))
        
        active_users = 0
        if response.rows:
            active_users = int(response.rows[0].metric_values[0].value or 0)
        
        print(f"Realtime Active Users: {active_users}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_realtime()
