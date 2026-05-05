@echo off
title Iniciar MyCRM
echo 🚀 Iniciando o MyCRM...

:: Inicia o Backend minimizado
echo 📦 Iniciando Backend...
start /min "CRM Backend" cmd /c "cd backend && .\venv\Scripts\python.exe manage.py runserver"

:: Inicia o Frontend minimizado
echo 🎨 Iniciando Frontend...
start /min "CRM Frontend" cmd /c "cd frontend && npm run dev"

:: Aguarda o carregamento (5 segundos)
echo ⏳ Aguardando servidores...
timeout /t 5 /nobreak > nul

:: Abre o navegador
echo 🌐 Abrindo no navegador...
start http://localhost:5173

echo ✅ Tudo pronto!
exit
