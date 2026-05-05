import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Adiciona o diretório 'backend' ao sys.path para que o Django encontre o módulo 'core'
# Isso resolve o erro 'ModuleNotFoundError: No module named core' na Vercel
sys.path.append(str(Path(__file__).resolve().parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Inicializa o Django
application = get_wsgi_application()
app = application
