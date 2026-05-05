#!/bin/bash

echo "🚀 Iniciando o MyCRM..."

# Função para limpar processos ao fechar
cleanup() {
    echo ""
    echo "🛑 Parando servidores..."
    kill $(jobs -p)
    exit
}
˜
trap cleanup SIGINT SIGTERM

# Verifica e configura o ambiente virtual no Backend
echo "📦 Configurando Backend..."
cd backend

if [ ! -d "venv_mac" ]; then
    echo "Creating macOS virtual environment..."
    python3 -m venv venv_mac
    source venv_mac/bin/activate
    pip install --upgrade pip
    pip install django djangorestframework django-cors-headers psycopg2-binary
else
    source venv_mac/bin/activate
fi

# Aplica migrações caso o banco de dados precise de ajustes
echo "🔄 Aplicando migrações de banco de dados..."
python manage.py migrate

# Inicia o Backend em segundo plano
python manage.py runserver &
BACKEND_PID=$!

cd ..

# Inicia o Frontend
echo "🎨 Iniciando Frontend..."
cd frontend
# Garante que as dependências do frontend estão instaladas
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências do frontend..."
    npm install
fi
npm run dev &
FRONTEND_PID=$!

cd ..

# Aguarda o carregamento
echo "⏳ Aguardando servidores (5s)..."
sleep 5

# Abre o navegador no FRONTEND
echo "🌐 Abrindo o CRM no navegador..."
open http://localhost:5173

echo "✅ O sistema está rodando!"
echo "👉 Acesse: http://localhost:5173"
echo "⚠️  Nota: O erro 404 em 'http://localhost:8000/' é normal, a API fica em /api/"
echo "Pressione Ctrl+C para encerrar."

# Mantém o script rodando para segurar os processos
wait
