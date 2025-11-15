import os
import sqlite3
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            r'C:\Projetos\Lubrimax\Site_Consulta\logs\database_update.log',
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

def criar_tabela_vendas():
    """Cria a tabela de vendas se não existir"""
    conn = sqlite3.connect(r'C:\Projetos\Lubrimax\Site_Consulta\data\db.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_emissao TEXT,
            numero_nf TEXT,
            cliente TEXT,
            placa TEXT,
            produto TEXT,
            quantidade REAL,
            valor_unitario REAL,
            valor_total REAL,
            empresa TEXT,
            data_atualizacao TEXT
        )
    ''')
    
    # Criar índice na coluna placa para buscas mais rápidas
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_placa ON vendas(placa)
    ''')
    
    conn.commit()
    conn.close()
    logging.info("[OK] Tabela vendas criada/verificada com sucesso")

def limpar_tabela_vendas():
    """Limpa todos os dados da tabela vendas"""
    conn = sqlite3.connect(r'C:\Projetos\Lubrimax\Site_Consulta\data\db.sqlite')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vendas')
    conn.commit()
    conn.close()
    logging.info("[OK] Tabela vendas limpa")

def processar_excel():
    """Processa o arquivo Excel e retorna um DataFrame limpo"""
    caminho_excel = r'C:\Projetos\Lubrimax\Vendas_Lubrimax.xlsx'
    
    if not os.path.exists(caminho_excel):
        logging.error(f"[ERRO] Arquivo não encontrado: {caminho_excel}")
        return None
    
    try:
        df = pd.read_excel(caminho_excel, engine='openpyxl')
        logging.info(f"[OK] Excel carregado com {len(df)} registros")
        logging.info(f"Colunas encontradas: {df.columns.tolist()}")
        
        # Normalizar nomes das colunas (remover espaços extras, converter para minúsculas)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Adicionar data de atualização
        df['data_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Remover registros sem placa
        df_limpo = df[df['placa'].notna() & (df['placa'] != '')]
        logging.info(f"[OK] Após limpeza: {len(df_limpo)} registros com placa válida")
        
        return df_limpo
    
    except Exception as e:
        logging.error(f"[ERRO] Erro ao processar Excel: {e}")
        return None

def atualizar_database(df):
    """Atualiza o banco de dados com os dados do DataFrame"""
    if df is None or len(df) == 0:
        logging.warning("[AVISO] Nenhum dado para inserir")
        return False
    
    try:
        conn = sqlite3.connect(r'C:\Projetos\Lubrimax\Site_Consulta\data\db.sqlite')
        
        # Mapear colunas do DataFrame para a tabela
        # Ajuste os nomes das colunas conforme necessário baseado no Excel real
        colunas_mapeamento = {
            'data_emissao': 'data_emissao',
            'numero_nf': 'numero_nf',
            'nf': 'numero_nf',  # caso seja apenas "NF"
            'cliente': 'cliente',
            'placa': 'placa',
            'produto': 'produto',
            'quantidade': 'quantidade',
            'qtd': 'quantidade',
            'valor_unitario': 'valor_unitario',
            'vlr_unitario': 'valor_unitario',
            'valor_total': 'valor_total',
            'vlr_total': 'valor_total',
            'empresa': 'empresa',
            'data_atualizacao': 'data_atualizacao'
        }
        
        # Renomear colunas do DataFrame se necessário
        for col_origem, col_destino in colunas_mapeamento.items():
            if col_origem in df.columns and col_origem != col_destino:
                df = df.rename(columns={col_origem: col_destino})
        
        # Selecionar apenas as colunas que existem tanto no DataFrame quanto na tabela
        colunas_tabela = ['data_emissao', 'numero_nf', 'cliente', 'placa', 'produto', 
                         'quantidade', 'valor_unitario', 'valor_total', 'empresa', 'data_atualizacao']
        
        colunas_disponiveis = [col for col in colunas_tabela if col in df.columns]
        df_inserir = df[colunas_disponiveis]
        
        # Inserir dados
        df_inserir.to_sql('vendas', conn, if_exists='append', index=False)
        
        conn.commit()
        conn.close()
        
        logging.info(f"[OK] {len(df_inserir)} registros inseridos no banco de dados")
        return True
    
    except Exception as e:
        logging.error(f"[ERRO] Erro ao atualizar banco de dados: {e}")
        return False

def verificar_dados():
    """Verifica quantos registros existem no banco"""
    conn = sqlite3.connect(r'C:\Projetos\Lubrimax\Site_Consulta\data\db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM vendas')
    total = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(DISTINCT placa) FROM vendas WHERE placa IS NOT NULL')
    total_placas = cursor.fetchone()[0]
    conn.close()
    
    logging.info(f"[INFO] Total de registros: {total}")
    logging.info(f"[INFO] Total de placas únicas: {total_placas}")
    return total, total_placas

def main():
    """Função principal"""
    logging.info("=" * 50)
    logging.info("🔄 Iniciando atualização do banco de dados")
    logging.info("=" * 50)
    
    # Passo 1: Criar tabela se não existir
    criar_tabela_vendas()
    
    # Passo 2: Limpar dados antigos
    limpar_tabela_vendas()
    
    # Passo 3: Processar Excel
    df = processar_excel()
    
    if df is None:
        logging.error("❌ Falha ao processar Excel")
        return False
    
    # Passo 4: Atualizar banco de dados
    sucesso = atualizar_database(df)
    
    if sucesso:
        # Passo 5: Verificar dados inseridos
        verificar_dados()
        logging.info("✅ Atualização do banco de dados concluída com sucesso!")
        return True
    else:
        logging.error("❌ Falha na atualização do banco de dados")
        return False

if __name__ == "__main__":
    main()
