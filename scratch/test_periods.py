
import os
import django
import sys
sys.path.append('/Users/gustavopallaagostinho/Downloads/MyCRM/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.ga4_service import get_full_report
from crm.models import Lead

def test_periods():
    lead = Lead.objects.filter(ga4_property_id='534448251').first()
    if not lead:
        print("Lead not found")
        return

    print("--- 30 DAYS ---")
    data_30 = get_full_report(lead.ga4_property_id, 30)
    print(f"PageViews: {data_30['metrics']['pageViews']}")
    print(f"Devices: {data_30['deviceBreakdown']}")
    
    print("\n--- 7 DAYS ---")
    data_7 = get_full_report(lead.ga4_property_id, 7)
    print(f"PageViews: {data_7['metrics']['pageViews']}")
    print(f"Devices: {data_7['deviceBreakdown']}")

if __name__ == "__main__":
    test_periods()
