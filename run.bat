@echo off
echo Iniciando Aplicativo de Preenchimento de Formularios...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado. Por favor, instale Python 3.11 ou superior.
    pause
    exit /b 1
)

REM Verificar se as dependências estão instaladas
echo Verificando dependencias...
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRO: Falha ao instalar dependencias.
        pause
        exit /b 1
    )
)

REM Executar o aplicativo
echo Iniciando aplicativo...
python app_gui.py

pause

