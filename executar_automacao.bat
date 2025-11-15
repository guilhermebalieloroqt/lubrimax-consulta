@echo off
REM ================================================
REM Automacao Lubrimax - Execucao diaria as 5h da manha
REM Este arquivo deve ser configurado no Agendador de Tarefas do Windows
REM ================================================

echo.
echo ================================================
echo       AUTOMACAO LUBRIMAX - INICIANDO
echo ================================================
echo Data/Hora: %date% %time%
echo.

REM Mudar para o diretorio do script
cd /d "%~dp0"
if %errorlevel% neq 0 (
    echo ERRO: Falha ao mudar para diretorio do script
    exit /b 1
)

echo Diretorio de trabalho: %CD%
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado no PATH!
    echo Verifique a instalacao do Python
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Verificar se o script existe
if not exist "automacao_completa.py" (
    echo ERRO: Script automacao_completa.py nao encontrado!
    exit /b 1
)

echo [OK] Script encontrado
echo.

REM Executar automacao
echo Executando automacao...
echo.
python automacao_completa.py

REM Capturar resultado
set RESULTADO=%errorlevel%

echo.
if %RESULTADO% equ 0 (
    echo ================================================
    echo   AUTOMACAO CONCLUIDA COM SUCESSO ^_^
    echo ================================================
    echo.
    echo Os dados foram atualizados no GitHub!
    echo Streamlit Cloud ira atualizar automaticamente.
) else (
    echo ================================================
    echo     ERRO NA EXECUCAO DA AUTOMACAO ^!
    echo ================================================
    echo.
    echo Codigo de erro: %RESULTADO%
    echo Verifique o log em: logs\automacao_completa.log
)
echo.

REM Se executado manualmente, manter janela aberta
if /I "%1" NEQ "agendado" (
    echo Pressione qualquer tecla para fechar...
    pause >nul
)

exit /b %RESULTADO%
