import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.models import Lead

try:
    lead = Lead.objects.create(
        nome_cliente="Teste Cliente",
        nome_empresa="Teste Empresa",
        telefone="123456789",
        status="PROSPECCAO",
        nicho="OUTROS",
        valor_estimado=100.00,
        ga4_property_id=""
    )
    print(f"Lead criado com sucesso: {lead.id}")
except Exception as e:
    print(f"Erro ao criar lead: {e}")
    import traceback
    traceback.print_exc()
