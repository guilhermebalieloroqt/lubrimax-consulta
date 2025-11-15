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
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            r'C:\Projetos\Lubrimax\Site_Consulta\logs\automacao_completa.log',
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

def executar_comando(comando, descricao):
    """Executa um comando e retorna True se bem sucedido"""
    try:
        logging.info(f"Executando: {descricao}")
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd=r'C:\Projetos\Lubrimax')
        
        if resultado.returncode == 0:
            logging.info(f"✅ {descricao} - Sucesso")
            if resultado.stdout:
                logging.info(f"Output: {resultado.stdout}")
            return True
        else:
            logging.error(f"❌ {descricao} - Falhou")
            if resultado.stderr:
                logging.error(f"Erro: {resultado.stderr}")
            return False
    except Exception as e:
        logging.error(f"❌ Erro ao executar {descricao}: {e}")
        return False

def main():
    """Função principal da automação"""
    inicio = datetime.now()
    logging.info("=" * 70)
    logging.info(f"🤖 AUTOMAÇÃO COMPLETA INICIADA - {inicio.strftime('%d/%m/%Y %H:%M:%S')}")
    logging.info("=" * 70)
    
    # Etapa 1: Download dos relatórios
    logging.info("\n📥 ETAPA 1/4: Download dos relatórios")
    sucesso_download = executar_comando(
        "python Site_Consulta\\download_relatorio.py",
        "Download e processamento dos relatórios"
    )
    
    if not sucesso_download:
        logging.error("❌ Falha no download. Abortando automação.")
        return False
    
    # Etapa 2: Verificar se o arquivo do banco existe
    logging.info("\n🔍 ETAPA 2/4: Verificando banco de dados")
    db_path = r'C:\Projetos\Lubrimax\Site_Consulta\data\db.sqlite'
    if os.path.exists(db_path):
        tamanho = os.path.getsize(db_path)
        logging.info(f"✅ Banco de dados encontrado ({tamanho} bytes)")
    else:
        logging.warning("⚠️ Banco de dados não encontrado (será criado)")
    
    # Etapa 3: Git add, commit e push
    logging.info("\n📤 ETAPA 3/4: Enviando para GitHub")
    
    # Git add
    executar_comando(
        "git add Site_Consulta/data/db.sqlite",
        "Git add - banco de dados"
    )
    
    executar_comando(
        "git add Vendas_Lubrimax.xlsx",
        "Git add - arquivo Excel"
    )
    
    # Git commit
    data_commit = datetime.now().strftime('%d/%m/%Y %H:%M')
    sucesso_commit = executar_comando(
        f'git commit -m "Atualização automática dos dados - {data_commit}"',
        "Git commit"
    )
    
    if sucesso_commit:
        # Git push
        sucesso_push = executar_comando(
            "git push origin main",
            "Git push para GitHub"
        )
        
        if sucesso_push:
            logging.info("✅ Dados enviados para GitHub com sucesso!")
        else:
            # Tentar com master caso main não funcione
            logging.info("Tentando push com branch master...")
            sucesso_push = executar_comando(
                "git push origin master",
                "Git push para GitHub (master)"
            )
    else:
        logging.warning("⚠️ Nenhuma mudança para commit ou erro no commit")
    
    # Etapa 4: Resumo final
    logging.info("\n📊 ETAPA 4/4: Resumo da execução")
    fim = datetime.now()
    duracao = (fim - inicio).total_seconds()
    
    logging.info("=" * 70)
    logging.info(f"⏱️  Tempo total de execução: {duracao:.2f} segundos")
    logging.info(f"🏁 Automação finalizada em: {fim.strftime('%d/%m/%Y %H:%M:%S')}")
    logging.info("=" * 70)
    logging.info("\n🌐 Próximos passos automáticos:")
    logging.info("   1. GitHub recebe os dados")
    logging.info("   2. Streamlit Cloud detecta mudança")
    logging.info("   3. Streamlit Cloud faz redeploy automático")
    logging.info("   4. Site WordPress mostra dados atualizados")
    logging.info("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("\n⚠️ Automação interrompida pelo usuário")
    except Exception as e:
        logging.error(f"\n❌ Erro crítico na automação: {e}")
