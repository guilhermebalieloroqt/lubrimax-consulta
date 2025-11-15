"""
Script de teste para verificar se o Git Push está funcionando
Execute este script antes de agendar a automação
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Cores para terminal Windows
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.ENDC}")

def executar_comando(cmd):
    """Executa comando e retorna output"""
    try:
        resultado = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        return resultado.returncode == 0, resultado.stdout.strip(), resultado.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def main():
    print(f"\n{Colors.BOLD}{'='*70}")
    print("🔧 TESTE DE CONFIGURAÇÃO GIT - LUBRIMAX")
    print(f"{'='*70}{Colors.ENDC}\n")
    
    erros = []
    avisos = []
    
    # 1. Verificar se é repositório Git
    print_info("Verificando repositório Git...")
    if (Path(__file__).parent / '.git').exists():
        print_success("Repositório Git detectado")
    else:
        print_error("NÃO é um repositório Git!")
        erros.append("Não é um repositório Git")
    
    # 2. Verificar configuração Git
    print_info("Verificando configuração do usuário Git...")
    sucesso, user, erro = executar_comando("git config user.name")
    if sucesso and user:
        print_success(f"Nome: {user}")
    else:
        print_error("Nome de usuário não configurado")
        erros.append("Configurar: git config --global user.name \"Seu Nome\"")
    
    sucesso, email, erro = executar_comando("git config user.email")
    if sucesso and email:
        print_success(f"Email: {email}")
    else:
        print_error("Email não configurado")
        erros.append("Configurar: git config --global user.email \"seu@email.com\"")
    
    # 3. Verificar remote
    print_info("Verificando remote GitHub...")
    sucesso, remote, erro = executar_comando("git remote -v")
    if sucesso and remote:
        print_success("Remote configurado:")
        for linha in remote.split('\n'):
            if linha.strip():
                print(f"   {linha}")
    else:
        print_error("Remote não configurado")
        erros.append("Remote não configurado")
    
    # 4. Verificar branch
    print_info("Verificando branch atual...")
    sucesso, branch, erro = executar_comando("git branch --show-current")
    if sucesso and branch:
        print_success(f"Branch: {branch}")
    else:
        print_error("Não foi possível detectar branch")
        erros.append("Branch não detectada")
    
    # 5. Verificar status
    print_info("Verificando status do repositório...")
    sucesso, status, erro = executar_comando("git status --porcelain")
    if sucesso:
        if status:
            print_warning(f"{len(status.split(chr(10)))} arquivo(s) modificado(s)")
            print("   Arquivos:")
            for linha in status.split('\n')[:5]:  # Mostrar apenas 5 primeiros
                print(f"   {linha}")
        else:
            print_success("Repositório limpo (sem modificações)")
    
    # 6. Verificar conectividade com GitHub
    print_info("Testando conectividade com GitHub...")
    sucesso, output, erro = executar_comando("git ls-remote origin")
    if sucesso:
        print_success("Conexão com GitHub OK")
    else:
        print_error("Falha ao conectar com GitHub")
        print_warning("Possíveis causas:")
        print("   - Sem conexão com internet")
        print("   - Credenciais não configuradas")
        print("   - Token/senha incorretos")
        erros.append("Falha de conexão com GitHub")
    
    # 7. Testar criação de arquivo temporário
    print_info("Testando git add...")
    test_file = Path(__file__).parent / "logs" / ".test_git"
    try:
        test_file.parent.mkdir(exist_ok=True)
        test_file.write_text(f"Teste: {datetime.now()}")
        
        sucesso, output, erro = executar_comando(f'git add "{test_file.relative_to(Path(__file__).parent)}"')
        if sucesso:
            print_success("Git add funcionando")
            # Limpar
            executar_comando("git reset HEAD")
            test_file.unlink()
        else:
            print_error("Git add falhou")
            erros.append("Git add falhou")
    except Exception as e:
        print_error(f"Erro ao testar git add: {e}")
        erros.append(str(e))
    
    # 8. Verificar credenciais (credential helper)
    print_info("Verificando armazenamento de credenciais...")
    sucesso, helper, erro = executar_comando("git config credential.helper")
    if helper:
        print_success(f"Credential helper: {helper}")
    else:
        print_warning("Nenhum credential helper configurado")
        print("   Você precisará digitar senha/token a cada push")
        avisos.append("Configure credential helper para evitar digitar senha sempre")
    
    # Resumo
    print(f"\n{Colors.BOLD}{'='*70}")
    print("📊 RESUMO DO TESTE")
    print(f"{'='*70}{Colors.ENDC}\n")
    
    if not erros and not avisos:
        print_success("TUDO OK! Git está configurado corretamente.")
        print_success("Você pode agendar a automação com segurança.")
        return 0
    
    if avisos:
        print(f"\n{Colors.YELLOW}⚠️  AVISOS ({len(avisos)}):{Colors.ENDC}")
        for aviso in avisos:
            print(f"   • {aviso}")
    
    if erros:
        print(f"\n{Colors.RED}❌ ERROS ENCONTRADOS ({len(erros)}):{Colors.ENDC}")
        for erro in erros:
            print(f"   • {erro}")
        print(f"\n{Colors.RED}Corrija os erros antes de agendar a automação!{Colors.ENDC}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⚠️  Teste interrompido")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
