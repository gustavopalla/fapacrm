"""
Módulo de Autenticação OAuth 2.0 para Google Analytics 4.

Gerencia o fluxo de login via navegador e o armazenamento/renovação
do token de acesso (Refresh Token) para que o login seja feito
apenas uma vez.s
"""
import os
import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Escopos necessários — apenas leitura de dados do Analytics
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

# Caminhos dos arquivos de credenciais
# BASE_DIR = backend/
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # MyCRM/
TOKEN_PATH = BASE_DIR / 'token.json'

# Buscar o client_secret automaticamente (aceita qualquer nome de arquivo client_secret_*.json)
def _find_client_secret():
    """Encontra o arquivo client_secret na raiz do projeto."""
    for f in BASE_DIR.iterdir():
        if f.name.startswith('client_secret') and f.name.endswith('.json'):
            return str(f)
    return None


def get_credentials():
    """
    Obtém credenciais OAuth 2.0 válidas.
    
    Fluxo:
    1. Se token.json existe e é válido → usa direto
    2. Se token.json existe mas expirou → renova via Refresh Token
    3. Se token.json NÃO existe → abre navegador para login
    
    Returns:
        google.oauth2.credentials.Credentials ou None se falhar
    """
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
            creds.refresh(Request())
            _save_token(creds)
            print("✅ Token renovado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao renovar token: {e}")
            creds = None

    # 3. Se não tem credenciais válidas, iniciar fluxo OAuth completo
    if not creds or not creds.valid:
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
            # Usa port=0 para encontrar uma porta livre automaticamente
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
    """Verifica se já existe um token válido salvo."""
    if not TOKEN_PATH.exists():
        return False
    try:
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        # Se é válido ou tem refresh token (pode renovar)
        return creds.valid or (creds.expired and creds.refresh_token is not None)
    except Exception:
        return False


def revoke_token():
    """Remove o token salvo (logout)."""
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
        return True
    return False
