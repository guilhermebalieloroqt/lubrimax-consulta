# Script de Configuração Inicial - Automação Lubrimax
# Execute este script uma vez para configurar todo o ambiente

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  CONFIGURAÇÃO INICIAL - AUTOMAÇÃO LUBRIMAX  " -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está no diretório correto
$currentPath = Get-Location
Write-Host "📂 Diretório atual: $currentPath" -ForegroundColor Yellow

if ($currentPath.Path -notlike "*Lubrimax*") {
    Write-Host "⚠️  ATENÇÃO: Execute este script da pasta C:\Projetos\Lubrimax" -ForegroundColor Red
    Write-Host "   cd C:\Projetos\Lubrimax" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "ETAPA 1: Verificando Python..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python NÃO encontrado!" -ForegroundColor Red
    Write-Host "   Instale Python em: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "ETAPA 2: Instalando dependências Python..." -ForegroundColor Green
Write-Host "   Instalando pacotes do requirements.txt..." -ForegroundColor Yellow
pip install -r Site_Consulta\requirements.txt

Write-Host ""
Write-Host "ETAPA 3: Verificando Git..." -ForegroundColor Green
try {
    $gitVersion = git --version 2>&1
    Write-Host "✅ Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git NÃO encontrado!" -ForegroundColor Red
    Write-Host "   Instale Git em: https://git-scm.com/download/win" -ForegroundColor Yellow
    $skipGit = $true
}

if (-not $skipGit) {
    Write-Host ""
    Write-Host "ETAPA 4: Configurando Git..." -ForegroundColor Green
    
    # Verificar se já é um repositório
    $isRepo = Test-Path ".git"
    
    if (-not $isRepo) {
        Write-Host "   Inicializando repositório Git..." -ForegroundColor Yellow
        git init
        git branch -M main
        Write-Host "✅ Repositório Git inicializado" -ForegroundColor Green
    } else {
        Write-Host "✅ Repositório Git já existe" -ForegroundColor Green
    }
    
    # Configurar credenciais
    Write-Host ""
    Write-Host "   Configurando credential helper..." -ForegroundColor Yellow
    git config --global credential.helper manager-core
    
    Write-Host ""
    Write-Host "📝 Configuração do Remote Git:" -ForegroundColor Cyan
    Write-Host "   Para adicionar seu repositório GitHub, execute:" -ForegroundColor Yellow
    Write-Host "   git remote add origin https://github.com/SEU_USUARIO/lubrimax.git" -ForegroundColor White
}

Write-Host ""
Write-Host "ETAPA 5: Criando estrutura de pastas..." -ForegroundColor Green

$folders = @(
    "Site_Consulta\logs",
    "Site_Consulta\data",
    "Site_Consulta\imagens"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "✅ Criado: $folder" -ForegroundColor Green
    } else {
        Write-Host "✅ Já existe: $folder" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "ETAPA 6: Testando sistema..." -ForegroundColor Green
Write-Host "   Executando teste_sistema.py..." -ForegroundColor Yellow
python Site_Consulta\teste_sistema.py

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  ✅ CONFIGURAÇÃO INICIAL CONCLUÍDA!         " -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 PRÓXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣  Configure o repositório GitHub:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/SEU_USUARIO/lubrimax.git" -ForegroundColor Gray
Write-Host ""
Write-Host "2️⃣  Teste o download dos relatórios:" -ForegroundColor White
Write-Host "   python Site_Consulta\download_relatorio.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3️⃣  Teste a atualização do banco:" -ForegroundColor White
Write-Host "   python Site_Consulta\atualizar_database.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4️⃣  Teste a automação completa:" -ForegroundColor White
Write-Host "   python Site_Consulta\automacao_completa.py" -ForegroundColor Gray
Write-Host ""
Write-Host "5️⃣  Configure o Agendador de Tarefas do Windows:" -ForegroundColor White
Write-Host "   - Abra: taskschd.msc" -ForegroundColor Gray
Write-Host "   - Crie tarefa para executar: Site_Consulta\executar_automacao.bat" -ForegroundColor Gray
Write-Host "   - Horário: 05:00 (diariamente)" -ForegroundColor Gray
Write-Host ""
Write-Host "6️⃣  Configure o Streamlit Cloud:" -ForegroundColor White
Write-Host "   - Acesse: https://share.streamlit.io/" -ForegroundColor Gray
Write-Host "   - Conecte seu repositório GitHub" -ForegroundColor Gray
Write-Host "   - Deploy automático ativado!" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Consulte README_AUTOMACAO.md para instruções detalhadas!" -ForegroundColor Cyan
Write-Host ""
