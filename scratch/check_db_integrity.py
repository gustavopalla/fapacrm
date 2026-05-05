import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.models import Lead

leads = Lead.objects.all()
for lead in leads:
    if not lead.nome_cliente or not lead.nome_empresa:
        print(f"Lead ID {lead.id} has missing required fields!")
    if lead.nicho is None:
        print(f"Lead ID {lead.id} has niche=None!")
    if lead.status is None:
        print(f"Lead ID {lead.id} has status=None!")
print("Check complete.")
