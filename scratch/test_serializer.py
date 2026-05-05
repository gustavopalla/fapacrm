import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.models import Lead, Project
from crm.serializers import LeadSerializer

try:
    # Criar um lead sem projeto
    lead = Lead.objects.create(
        nome_cliente="Teste Serializer",
        nome_empresa="Teste Serializer",
    )
    
    serializer = LeadSerializer(lead)
    print("Serializado com sucesso:")
    print(serializer.data)
    
except Exception as e:
    print(f"Erro ao serializar: {e}")
    import traceback
    traceback.print_exc()
