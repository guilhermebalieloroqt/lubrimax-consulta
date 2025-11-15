@echo off
REM Automação Lubrimax - Execução diária às 5h da manhã
REM Este arquivo deve ser configurado no Agendador de Tarefas do Windows

echo ========================================
echo Iniciando Automacao Lubrimax
echo ========================================

cd /d C:\Projetos\Lubrimax

REM Executar o script Python
python Site_Consulta\automacao_completa.py

REM Verificar resultado
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Automacao concluida com SUCESSO!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ERRO na execucao da automacao
    echo ========================================
)

REM Manter janela aberta por 10 segundos para visualizar resultado
timeout /t 10

exit
