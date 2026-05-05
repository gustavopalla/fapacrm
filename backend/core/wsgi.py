import os
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Inicializa o Django antes de qualquer outra coisa
application = get_wsgi_application()

# Roda migrações apenas se estiver na Vercel
if os.environ.get('VERCEL') or os.environ.get('POSTGRES_URL'):
    try:
        print(">>> Rodando migrações na Vercel...")
        call_command('migrate', '--noinput')
        print(">>> Migrações concluídas!")
    except Exception as e:
        print(f">>> Erro nas migrações: {e}")
        import traceback
        traceback.print_exc()

app = application
