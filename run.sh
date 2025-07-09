#!/bin/bash

echo "Iniciando Aplicativo de Preenchimento de Formulários..."
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python3 não encontrado. Por favor, instale Python 3.11 ou superior."
    exit 1
fi

# Verificar se tkinter está disponível
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERRO: tkinter não encontrado."
    echo "No Ubuntu/Debian, instale com: sudo apt-get install python3-tk"
    echo "No CentOS/RHEL, instale com: sudo yum install tkinter"
    echo "No macOS, tkinter já vem com Python."
    exit 1
fi

# Verificar se as dependências estão instaladas
echo "Verificando dependências..."
python3 -c "import selenium, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERRO: Falha ao instalar dependências."
        exit 1
    fi
fi

# Tornar ChromeDriver executável
chmod +x chromedriver

# Executar o aplicativo
echo "Iniciando aplicativo..."
python3 app_gui.py

