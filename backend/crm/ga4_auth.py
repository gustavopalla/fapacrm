"""
Módulo de Autenticação OAuth 2.0 para Google Analytics 4.

Suporta dois modos:
- LOCAL: Usa arquivos (client_secret_*.json + token.json) com fluxo via navegador
- VERCEL: Usa variáveis de ambiente (GA4_REFRESH_TOKEN, GA4_CLIENT_ID, GA4_CLIENT_SECRET)
"""
import os
import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Escopos necessários — apenas leitura de dados do Analytics
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

# Detectar ambiente
IS_VERCEL = bool(os.environ.get('VERCEL'))

# Caminhos dos arquivos de credenciais (modo local)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # MyCRM/
TOKEN_PATH = Path('/tmp/token.json') if IS_VERCEL else BASE_DIR / 'token.json'


def _find_client_secret():
    """Encontra o arquivo client_secret na raiz do projeto."""
    for f in BASE_DIR.iterdir():
        if f.name.startswith('client_secret') and f.name.endswith('.json'):
            return str(f)
    return None


def _get_credentials_from_env():
    """
    Constrói credenciais a partir de variáveis de ambiente (para Vercel).
    Usa o refresh_token para obter um access_token novo automaticamente.
    """
    refresh_token = os.environ.get('GA4_REFRESH_TOKEN')
    client_id = os.environ.get('GA4_CLIENT_ID')
    client_secret = os.environ.get('GA4_CLIENT_SECRET')

    if not all([refresh_token, client_id, client_secret]):
        print("❌ Variáveis de ambiente GA4 não configuradas!")
        print("   Necessário: GA4_REFRESH_TOKEN, GA4_CLIENT_ID, GA4_CLIENT_SECRET")
        return None

    try:
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )

        # Forçar refresh para obter access_token válido
        print("🔄 [Vercel] Obtendo access token via refresh_token...")
        creds.refresh(Request())
        print(f"✅ [Vercel] Token obtido! Expira em: {creds.expiry}")
        return creds

    except Exception as e:
        import traceback
        print(f"❌ [Vercel] Erro ao obter token: {e}")
        print(f"   Detalhes: {traceback.format_exc()}")
        return None


def get_credentials():
    """
    Obtém credenciais OAuth 2.0 válidas.
    
    - Na Vercel: usa variáveis de ambiente
    - Localmente: usa arquivos token.json / client_secret_*.json
    """
    # === MODO VERCEL: variáveis de ambiente ===
    if IS_VERCEL:
        return _get_credentials_from_env()

    # === MODO LOCAL: arquivos ===
    creds = None

    # 1. Tentar carregar token salvo
    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        except Exception as e:
            print(f"⚠️ Erro ao carregar token.json: {e}")
            creds = None

    # 2. Se tem credenciais mas expiraram, renovar
    if creds and creds.expired and creds.refresh_token:
        try:
            print("🔄 Renovando token de acesso...")
            print(f"   Token expirou em: {creds.expiry}")
            creds.refresh(Request())
            _save_token(creds)
            print("✅ Token renovado com sucesso!")
            print(f"   Novo vencimento: {creds.expiry}")
        except Exception as e:
            import traceback
            print(f"❌ Erro ao renovar token: {e}")
            print(f"   Detalhes: {traceback.format_exc()}")
            print("   🗑️  Deletando token inválido para forçar re-autenticação...")
            if TOKEN_PATH.exists():
                TOKEN_PATH.unlink()
            creds = None

    # 3. Se não tem credenciais válidas, iniciar fluxo OAuth completo
    if not creds or not creds.valid:
        from google_auth_oauthlib.flow import InstalledAppFlow
        
        client_secret_path = _find_client_secret()
        if not client_secret_path:
            print("❌ Arquivo client_secret_*.json não encontrado na raiz do projeto!")
            return None

        print("🌐 Abrindo navegador para autorização Google...")
        print("   (Faça login com impalla404@gmail.com)")
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_path,
                SCOPES
            )
            creds = flow.run_local_server(
                port=0,
                prompt='consent',
                access_type='offline',
                success_message="Sucesso! Autenticação GA4 concluída. Você já pode fechar esta aba."
            )
            _save_token(creds)
            print("✅ Login realizado com sucesso! Token salvo.")
        except Exception as e:
            print(f"❌ Erro durante autenticação OAuth: {e}")
            return None

    return creds


def _save_token(creds):
    """Salva as credenciais no token.json para reutilizar."""
    with open(TOKEN_PATH, 'w') as token_file:
        token_file.write(creds.to_json())


def is_authenticated():
    """Verifica se já existe um token válido ou se as env vars estão configuradas."""
    # Na Vercel, verificar se as variáveis de ambiente existem
    if IS_VERCEL:
        return all([
            os.environ.get('GA4_REFRESH_TOKEN'),
            os.environ.get('GA4_CLIENT_ID'),
            os.environ.get('GA4_CLIENT_SECRET')
        ])
    
    # Localmente, verificar o token.json
    if not TOKEN_PATH.exists():
        return False
    try:
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        return creds.valid or (creds.expired and creds.refresh_token is not None)
    except Exception:
        return False


def revoke_token():
    """Remove o token salvo (logout)."""
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
        return True
    return False
