import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.models import Lead

def seed():
    leads = [
        {
            "nome_cliente": "João Silva",
            "nome_empresa": "Padaria do João",
            "status": "PROSPECCAO",
            "valor_estimado": 2500.00,
            "tem_site": False
        },
        {
            "nome_cliente": "Maria Oliveira",
            "nome_empresa": "Tech Solutions",
            "status": "CONTATO",
            "valor_estimado": 8000.00,
            "tem_site": True
        },
        {
            "nome_cliente": "Carlos Souza",
            "nome_empresa": "Oficina do Carlos",
            "status": "BRIEFING",
            "valor_estimado": 4500.00,
            "tem_site": False
        },
        {
            "nome_cliente": "Ana Costa",
            "nome_empresa": "Escola de Dança Ana",
            "status": "PROPOSTA",
            "valor_estimado": 12000.00,
            "tem_site": False
        }
    ]

    for data in leads:
        Lead.objects.get_or_create(**data)
    
    print("Banco de dados populado com sucesso!")

if __name__ == "__main__":
    seed()
