"""
Script automatizado para execução diária às 5h da manhã
Fluxo completo:
1. Baixa relatórios
2. Atualiza banco de dados
3. Faz commit e push para GitHub
4. Streamlit Cloud detecta mudança e atualiza automaticamente
"""

import subprocess
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
import requests
import time

# Garantir que estamos no diretório correto
SCRIPT_DIR = Path(__file__).parent.resolve()
os.chdir(SCRIPT_DIR)

# Criar diretório de logs se não existir
LOGS_DIR = SCRIPT_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            LOGS_DIR / 'automacao_completa.log',
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

def acordar_streamlit(max_tentativas=5, intervalo=60):
    """
    Envia requisições para o app Streamlit para evitar que ele entre em modo de suspensão.
    O Streamlit Cloud pode demorar até 5 minutos para acordar um app em sleep mode.
    
    Args:
        max_tentativas: Número máximo de tentativas
        intervalo: Segundos entre tentativas
    """
    url_app = "https://lubrimax.streamlit.app"
    
    logging.info(f"⏰ Acordando Streamlit App: {url_app}")
    logging.info(f"   (Até {max_tentativas} tentativas com {intervalo}s de intervalo)")
    
    for tentativa in range(1, max_tentativas + 1):
        try:
            logging.info(f"   Tentativa {tentativa}/{max_tentativas}...")
            response = requests.get(url_app, timeout=120)  # Timeout maior para apps dormindo
            
            if response.status_code == 200:
                # Verifica se é a página real ou página de "waking up"
                if "Please wait" in response.text or "waking up" in response.text.lower():
                    logging.info(f"   ⏳ App está acordando... aguardando {intervalo}s")
                    time.sleep(intervalo)
                    continue
                else:
                    logging.info("✅ Streamlit App acordado e respondendo!")
                    return True
            else:
                logging.warning(f"   ⚠️ Status: {response.status_code}")
                
        except requests.exceptions.Timeout:
            logging.info(f"   ⏳ Timeout - app pode estar acordando... aguardando {intervalo}s")
        except Exception as e:
            logging.warning(f"   ⚠️ Erro: {e}")
        
        if tentativa < max_tentativas:
            time.sleep(intervalo)
    
    logging.warning("⚠️ Não foi possível confirmar que o app acordou completamente")
    logging.info("   O app deve acordar automaticamente quando acessado manualmente")
    return False

def executar_comando(comando, descricao, critical=False):
    """
    Executa um comando e retorna True se bem sucedido
    
    Args:
        comando: Comando a ser executado
        descricao: Descrição do comando para log
        critical: Se True, encerra o script em caso de falha
    """
    try:
        logging.info(f"Executando: {descricao}")
        logging.debug(f"Comando: {comando}")
        
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=SCRIPT_DIR,
            timeout=300  # Timeout de 5 minutos
        )
        
        if resultado.returncode == 0:
            logging.info(f"✅ {descricao} - Sucesso")
            if resultado.stdout and resultado.stdout.strip():
                logging.info(f"Output: {resultado.stdout.strip()}")
            return True
        else:
            logging.error(f"❌ {descricao} - Falhou (código: {resultado.returncode})")
            if resultado.stderr and resultado.stderr.strip():
                logging.error(f"Erro: {resultado.stderr.strip()}")
            if resultado.stdout and resultado.stdout.strip():
                logging.error(f"Output: {resultado.stdout.strip()}")
            
            if critical:
                logging.critical(f"Comando crítico falhou. Encerrando automação.")
                sys.exit(1)
            return False
            
    except subprocess.TimeoutExpired:
        logging.error(f"❌ {descricao} - Timeout (>5min)")
        if critical:
            sys.exit(1)
        return False
    except Exception as e:
        logging.error(f"❌ Erro ao executar {descricao}: {e}")
        if critical:
            sys.exit(1)
        return False

def verificar_mudancas_git():
    """Verifica se há mudanças no repositório"""
    try:
        resultado = subprocess.run(
            "git status --porcelain",
            shell=True,
            capture_output=True,
            text=True,
            cwd=SCRIPT_DIR
        )
        return bool(resultado.stdout.strip())
    except Exception as e:
        logging.error(f"Erro ao verificar mudanças Git: {e}")
        return False

def main():
    """Função principal da automação"""
    inicio = datetime.now()
    logging.info("=" * 70)
    logging.info(f"🤖 AUTOMAÇÃO COMPLETA INICIADA - {inicio.strftime('%d/%m/%Y %H:%M:%S')}")
    logging.info(f"📁 Diretório de trabalho: {SCRIPT_DIR}")
    logging.info("=" * 70)
    
    # Verificar se estamos em um repositório Git
    if not (SCRIPT_DIR / '.git').exists():
        logging.critical("❌ Não é um repositório Git! Verifique o diretório.")
        return False
    
    # Etapa 0: Acordar o Streamlit ANTES de tudo (para ganhar tempo)
    logging.info("\n⏰ ETAPA 0/5: Acordando Streamlit App (processo em paralelo)")
    logging.info("   Isso evita que o app fique 'travado' quando você acessar de manhã")
    acordar_streamlit(max_tentativas=3, intervalo=30)  # Primeira tentativa rápida
    
    # Etapa 1: Download dos relatórios
    logging.info("\n📥 ETAPA 1/5: Download dos relatórios")
    python_cmd = sys.executable  # Usa o mesmo Python que está executando o script
    sucesso_download = executar_comando(
        f'"{python_cmd}" download_relatorio.py',
        "Download e processamento dos relatórios",
        critical=True  # Crítico - para tudo se falhar
    )
    
    # Etapa 2: Verificar se o arquivo do banco existe
    logging.info("\n🔍 ETAPA 2/5: Verificando banco de dados")
    db_path = SCRIPT_DIR / 'data' / 'db.sqlite'
    if db_path.exists():
        tamanho = db_path.stat().st_size
        logging.info(f"✅ Banco de dados encontrado ({tamanho:,} bytes)")
        
        # Verificar se tem conteúdo
        if tamanho == 0:
            logging.error("❌ Banco de dados vazio!")
            return False
    else:
        logging.error("❌ Banco de dados não encontrado!")
        return False
    
    # Etapa 3: Verificar mudanças
    logging.info("\n🔎 ETAPA 3/5: Verificando mudanças no repositório")
    if not verificar_mudancas_git():
        logging.info("ℹ️  Nenhuma mudança detectada. Nada para commitar.")
        logging.info("✅ Automação concluída (sem atualizações)")
        return True
    
    # Etapa 4: Git add, commit e push
    logging.info("\n📤 ETAPA 4/5: Enviando para GitHub")
    
    # Git add - adicionar arquivos críticos
    arquivos_git = [
        "data/db.sqlite",
        "Vendas_Lubrimax.xlsx",
        "logs/*.log"
    ]
    
    for arquivo in arquivos_git:
        arquivo_path = SCRIPT_DIR / arquivo.replace('/', '\\')
        if '*' in arquivo or arquivo_path.exists():
            executar_comando(
                f'git add "{arquivo}"',
                f"Git add - {arquivo}"
            )
        else:
            logging.warning(f"⚠️ Arquivo não encontrado: {arquivo}")
    
    # Git commit
    data_commit = datetime.now().strftime('%d/%m/%Y %H:%M')
    sucesso_commit = executar_comando(
        f'git commit -m "🤖 Atualização automática dos dados - {data_commit}"',
        "Git commit"
    )
    
    if not sucesso_commit:
        logging.warning("⚠️ Nenhuma mudança para commit")
        logging.info("✅ Automação concluída (sem mudanças)")
        return True
    
    # Git push com retry
    logging.info("📤 Enviando para GitHub...")
    tentativas_push = 0
    max_tentativas = 3
    sucesso_push = False
    
    while tentativas_push < max_tentativas and not sucesso_push:
        tentativas_push += 1
        logging.info(f"Tentativa {tentativas_push}/{max_tentativas}")
        
        # Tentar pull antes do push (evitar conflitos)
        executar_comando(
            "git pull --rebase origin main",
            "Git pull (rebase)"
        )
        
        # Tentar push
        sucesso_push = executar_comando(
            "git push origin main",
            "Git push para GitHub"
        )
        
        if sucesso_push:
            logging.info("✅ Dados enviados para GitHub com sucesso!")
            break
        elif tentativas_push < max_tentativas:
            logging.warning(f"⚠️ Falha no push. Tentando novamente em 5 segundos...")
            time.sleep(5)
    
    if not sucesso_push:
        logging.error("❌ Falha ao enviar para GitHub após 3 tentativas")
        logging.error("🔧 Ações recomendadas:")
        logging.error("   1. Verifique a conexão com internet")
        logging.error("   2. Verifique as credenciais do Git")
        logging.error("   3. Execute manualmente: git push origin main")
        return False
    
    # Acordar Streamlit após deploy
    if sucesso_push:
        logging.info("\n⏳ Aguardando deploy do Streamlit Cloud...")
        logging.info("   O Streamlit Cloud detecta o push e faz redeploy automático")
        time.sleep(60)  # Aguarda 1 minuto para o deploy iniciar
        
        logging.info("\n🔄 Garantindo que o app está acordado...")
        acordar_streamlit(max_tentativas=5, intervalo=60)  # Tentativas mais persistentes

    # Etapa 5: Resumo final
    logging.info("\n📊 ETAPA 5/5: Resumo da execução")
    fim = datetime.now()
    duracao = (fim - inicio).total_seconds()
    
    logging.info("=" * 70)
    logging.info(f"⏱️  Tempo total de execução: {duracao:.2f} segundos")
    logging.info(f"🏁 Automação finalizada em: {fim.strftime('%d/%m/%Y %H:%M:%S')}")
    logging.info("=" * 70)
    
    if sucesso_push:
        logging.info("\n🌐 Próximos passos automáticos:")
        logging.info("   1. ✅ GitHub recebe os dados")
        logging.info("   2. 🔄 Streamlit Cloud detecta mudança")
        logging.info("   3. 🚀 Streamlit Cloud faz redeploy automático")
        logging.info("   4. 🌍 Site WordPress mostra dados atualizados")
        logging.info("=" * 70)
    
    return sucesso_push

def verificar_credenciais_git():
    """Verifica se as credenciais do Git estão configuradas"""
    try:
        resultado_user = subprocess.run(
            "git config user.name",
            shell=True,
            capture_output=True,
            text=True,
            cwd=SCRIPT_DIR
        )
        
        resultado_email = subprocess.run(
            "git config user.email",
            shell=True,
            capture_output=True,
            text=True,
            cwd=SCRIPT_DIR
        )
        
        if not resultado_user.stdout.strip() or not resultado_email.stdout.strip():
            logging.error("❌ Credenciais do Git não configuradas!")
            logging.error("Execute:")
            logging.error('   git config --global user.name "Seu Nome"')
            logging.error('   git config --global user.email "seu@email.com"')
            return False
        
        logging.info(f"✅ Git configurado: {resultado_user.stdout.strip()} <{resultado_email.stdout.strip()}>")
        return True
        
    except Exception as e:
        logging.error(f"Erro ao verificar credenciais: {e}")
        return False

if __name__ == "__main__":
    try:
        # Verificar credenciais antes de começar
        if not verificar_credenciais_git():
            sys.exit(1)
        
        # Executar automação
        sucesso = main()
        
        # Retornar código apropriado
        sys.exit(0 if sucesso else 1)
        
    except KeyboardInterrupt:
        logging.warning("\n⚠️ Automação interrompida pelo usuário")
        sys.exit(130)
    except Exception as e:
        logging.error(f"\n❌ Erro crítico na automação: {e}")
        logging.exception("Traceback completo:")
        sys.exit(1)
