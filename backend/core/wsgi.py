import os
import sys
from pathlib import Path

# 1. Identifica o caminho absoluto da pasta 'backend'
# Path(__file__) é backend/core/wsgi.py
# .parent é backend/core/
# .parent.parent é backend/
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent

# 2. Adiciona ao sys.path de forma prioritária (posição 0)
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# 3. Configura o módulo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 4. Inicializa o WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# 5. Roda as migrações (agora que o sys.path e o Django estão prontos)
if os.environ.get('VERCEL'):
    from django.core.management import call_command
    try:
        print(">>> Rodando migrações no startup...")
        call_command('migrate', '--noinput')
        print(">>> Migrações concluídas!")
    except Exception as e:
        print(f">>> Erro nas migrações: {e}")

app = application
