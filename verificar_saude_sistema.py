"""
Script de Verificação de Saúde do Sistema
Verifica todos os componentes críticos da automação
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import sqlite3

# Cores
class C:
    G = '\033[92m'  # Green
    Y = '\033[93m'  # Yellow
    R = '\033[91m'  # Red
    B = '\033[94m'  # Blue
    E = '\033[0m'   # End
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{C.BOLD}{C.B}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{C.E}\n")

def print_ok(text):
    print(f"{C.G}✅ {text}{C.E}")

def print_warn(text):
    print(f"{C.Y}⚠️  {text}{C.E}")

def print_error(text):
    print(f"{C.R}❌ {text}{C.E}")

def print_info(text):
    print(f"{C.B}ℹ️  {text}{C.E}")

def check_file(filepath, min_size=0):
    """Verifica se arquivo existe e tem tamanho mínimo"""
    path = Path(filepath)
    if not path.exists():
        return False, "Arquivo não encontrado"
    
    size = path.stat().st_size
    if size < min_size:
        return False, f"Arquivo muito pequeno ({size} bytes)"
    
    return True, f"OK ({size:,} bytes)"

def run_command(cmd):
    """Executa comando e retorna sucesso/output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=Path(__file__).parent
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def main():
    script_dir = Path(__file__).parent
    
    print_header("🏥 VERIFICAÇÃO DE SAÚDE DO SISTEMA LUBRIMAX")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Diretório: {script_dir}")
    
    issues = []
    warnings = []
    
    # 1. Verificar Python
    print_header("1️⃣  VERIFICANDO PYTHON")
    success, version, _ = run_command("python --version")
    if success:
        print_ok(f"Python instalado: {version}")
    else:
        print_error("Python não encontrado!")
        issues.append("Python não instalado")
    
    # 2. Verificar dependências
    print_header("2️⃣  VERIFICANDO DEPENDÊNCIAS")
    deps = ['selenium', 'pandas', 'streamlit', 'Pillow', 'pyautogui']
    for dep in deps:
        success, output, _ = run_command(f'python -c "import {dep}; print({dep}.__version__)"')
        if success:
            print_ok(f"{dep}: {output}")
        else:
            print_error(f"{dep}: NÃO INSTALADO")
            issues.append(f"Instalar: pip install {dep}")
    
    # 3. Verificar Git
    print_header("3️⃣  VERIFICANDO GIT")
    success, version, _ = run_command("git --version")
    if success:
        print_ok(f"Git instalado: {version}")
    else:
        print_error("Git não encontrado!")
        issues.append("Git não instalado")
    
    success, user, _ = run_command("git config user.name")
    if success and user:
        print_ok(f"Usuário: {user}")
    else:
        print_error("Usuário Git não configurado")
        issues.append("Configure: git config --global user.name")
    
    success, email, _ = run_command("git config user.email")
    if success and email:
        print_ok(f"Email: {email}")
    else:
        print_error("Email Git não configurado")
        issues.append("Configure: git config --global user.email")
    
    success, remote, _ = run_command("git remote -v")
    if success and remote:
        print_ok("Remote GitHub configurado")
    else:
        print_error("Remote não configurado")
        issues.append("Remote GitHub não configurado")
    
    # 4. Verificar conectividade GitHub
    print_header("4️⃣  TESTANDO GITHUB")
    success, _, _ = run_command("git ls-remote origin")
    if success:
        print_ok("Conexão com GitHub: OK")
    else:
        print_error("Falha ao conectar com GitHub")
        issues.append("Verifique credenciais/internet")
    
    # 5. Verificar arquivos críticos
    print_header("5️⃣  VERIFICANDO ARQUIVOS CRÍTICOS")
    critical_files = {
        'automacao_completa.py': 0,
        'download_relatorio.py': 0,
        'database.py': 0,
        'app.py': 0,
        'executar_automacao.bat': 0,
        'requirements.txt': 0
    }
    
    for filename, min_size in critical_files.items():
        filepath = script_dir / filename
        success, msg = check_file(filepath, min_size)
        if success:
            print_ok(f"{filename}: {msg}")
        else:
            print_error(f"{filename}: {msg}")
            issues.append(f"Arquivo faltando: {filename}")
    
    # 6. Verificar banco de dados
    print_header("6️⃣  VERIFICANDO BANCO DE DADOS")
    db_path = script_dir / 'data' / 'db.sqlite'
    
    if db_path.exists():
        size = db_path.stat().st_size
        print_ok(f"Banco existe: {size:,} bytes")
        
        if size > 0:
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Verificar tabela vendas
                cursor.execute("SELECT COUNT(*) FROM vendas")
                count = cursor.fetchone()[0]
                print_ok(f"Registros no banco: {count:,}")
                
                # Verificar último registro
                cursor.execute("SELECT MAX(data_emissao) FROM vendas")
                ultima_data = cursor.fetchone()[0]
                if ultima_data:
                    print_ok(f"Última atualização: {ultima_data}")
                
                conn.close()
            except Exception as e:
                print_error(f"Erro ao ler banco: {e}")
                issues.append("Banco corrompido ou inválido")
        else:
            print_error("Banco vazio!")
            issues.append("Banco de dados sem dados")
    else:
        print_warn("Banco não existe (será criado na primeira execução)")
        warnings.append("Banco será criado automaticamente")
    
    # 7. Verificar ChromeDriver
    print_header("7️⃣  VERIFICANDO CHROMEDRIVER")
    chromedriver = script_dir / 'chromedriver-win64' / 'chromedriver.exe'
    success, msg = check_file(chromedriver)
    if success:
        print_ok(f"ChromeDriver: {msg}")
    else:
        print_error("ChromeDriver não encontrado!")
        issues.append("Baixe ChromeDriver: https://chromedriver.chromium.org/")
    
    # 8. Verificar logs
    print_header("8️⃣  VERIFICANDO LOGS")
    log_dir = script_dir / 'logs'
    if log_dir.exists():
        print_ok("Diretório de logs existe")
        
        log_file = log_dir / 'automacao_completa.log'
        if log_file.exists():
            size = log_file.stat().st_size
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            print_ok(f"Log existe: {size:,} bytes")
            print_info(f"Última modificação: {mtime.strftime('%d/%m/%Y %H:%M:%S')}")
        else:
            print_warn("Log ainda não criado (normal na primeira vez)")
    else:
        print_warn("Diretório de logs não existe (será criado)")
    
    # 9. Verificar tarefa agendada
    print_header("9️⃣  VERIFICANDO TAREFA AGENDADA")
    success, output, _ = run_command('schtasks /Query /TN "Lubrimax_Atualizacao_Diaria" /FO LIST')
    if success:
        print_ok("Tarefa agendada existe")
        # Extrair informações relevantes
        for line in output.split('\n'):
            if any(key in line for key in ['Status', 'Próxima Execução', 'Última Execução']):
                print_info(f"   {line.strip()}")
    else:
        print_warn("Tarefa agendada NÃO criada")
        warnings.append("Execute: python agendar_automacao.py")
    
    # 10. Testar push (sem fazer push de verdade)
    print_header("🔟 TESTANDO GIT PUSH (dry-run)")
    success, output, error = run_command("git push origin main --dry-run")
    if success or "Everything up-to-date" in output or "up-to-date" in error.lower():
        print_ok("Git push funcionando (sem mudanças ou teste OK)")
    else:
        print_error("Git push falhou!")
        print_error(f"Erro: {error}")
        issues.append("Verifique credenciais Git")
    
    # RESUMO FINAL
    print_header("📊 RESUMO DA VERIFICAÇÃO")
    
    print(f"Total de verificações: {C.BOLD}10{C.E}")
    print(f"Problemas encontrados: {C.BOLD}{len(issues)}{C.E}")
    print(f"Avisos: {C.BOLD}{len(warnings)}{C.E}")
    print()
    
    if warnings:
        print(f"{C.Y}⚠️  AVISOS:{C.E}")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
        print()
    
    if issues:
        print(f"{C.R}❌ PROBLEMAS ENCONTRADOS:{C.E}")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print()
        print(f"{C.R}Corrija os problemas antes de agendar a automação!{C.E}")
        return 1
    
    if not warnings and not issues:
        print(f"{C.G}{'='*70}")
        print(f"🎉 SISTEMA 100% OPERACIONAL!")
        print(f"{'='*70}{C.E}")
        print()
        print(f"{C.G}✅ Tudo está funcionando perfeitamente!")
        print(f"✅ Você pode agendar a automação com segurança!{C.E}")
        print()
        print("Próximos passos:")
        print("   1. Teste manual: .\\executar_automacao.bat")
        print("   2. Agende: python agendar_automacao.py")
        return 0
    
    if warnings and not issues:
        print(f"{C.Y}Sistema funcional, mas há alguns avisos.{C.E}")
        print("Você pode continuar, mas resolva os avisos quando possível.")
        return 0
    
    return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificação interrompida")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
