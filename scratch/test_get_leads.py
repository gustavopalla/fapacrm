import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.models import Lead

try:
    leads = Lead.objects.all()
    print(f"Total de leads: {leads.count()}")
    for lead in leads[:5]:
        print(f"Lead: {lead.nome_cliente}")
except Exception as e:
    print(f"Erro ao buscar leads: {e}")
    import traceback
    traceback.print_exc()
