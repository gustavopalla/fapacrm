
import os
import django
import sys
sys.path.append('/Users/gustavopallaagostinho/Downloads/MyCRM/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.ga4_service import _create_client
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from crm.models import Lead

def test_raw_devices():
    lead = Lead.objects.filter(ga4_property_id='534448251').first()
    client = _create_client()
    property_name = f"properties/{lead.ga4_property_id}"
    
    response = client.run_report(RunReportRequest(
        property=property_name,
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        dimensions=[Dimension(name="deviceCategory")],
        metrics=[Metric(name="sessions")],
    ))
    
    print("RAW DEVICE DATA:")
    for row in response.rows:
        device = row.dimension_values[0].value
        count = row.metric_values[0].value
        print(f"Device: {device}, Sessions: {count}")

if __name__ == "__main__":
    test_raw_devices()
