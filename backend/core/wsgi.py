"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Migrações automáticas no startup para Vercel
try:
    print(">>> Rodando migrações automáticas no startup...")
    call_command('migrate', '--noinput')
    print(">>> Migrações concluídas com sucesso!")
except Exception as e:
    print(f">>> Erro nas migrações de startup: {e}")
    import traceback
    traceback.print_exc()

application = get_wsgi_application()
app = application
