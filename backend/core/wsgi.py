import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Inicializa o Django
# No Vercel, as migrações devem rodar no build_vercel.sh, não aqui.
application = get_wsgi_application()
app = application
