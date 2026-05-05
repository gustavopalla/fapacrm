#!/bin/bash
# Vercel build script - roda as migrações do Django automaticamente

echo ">>> Instalando dependências do backend..."
pip install -r backend/requirements.txt

echo ">>> Coletando arquivos estáticos..."
cd backend
python manage.py collectstatic --noinput

echo ">>> Rodando migrações do banco de dados..."
python manage.py migrate --noinput

echo ">>> Build do backend concluído!"
