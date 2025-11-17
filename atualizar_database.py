import os
import sqlite3
import pandas as pd
import logging
import re
from datetime import datetime

# Configuração de logging
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

def extrair_placa_km(observacao):
    """
    Extrai placa e KM do campo observação
    
    Formatos aceitos para KM:
    - "KM 123456"
    - "KM: 220.878" (com pontos)
    - "KM  265184" (com espaços extras)
    - "KM  1207403" (milhões)
    - "KM: 220,878" (com vírgulas)
    
    Formatos aceitos para placa:
    - "PLACA: ABC1234" ou "PLACA ABC1234"
    - "PLACAS: ABC1234" (plural)
    - "ABC1234" (só a placa)
    - "VW ABC1234" (com modelo)
    - "DUCATO ABC1234"
    
    Returns:
        tuple: (placa, km) onde km pode ser None
    """
    if pd.isna(observacao):
        return None, None
    
    observacao = str(observacao).strip().upper()
    
    # Extrair KM se existir - aceita pontos, vírgulas e espaços como separadores
    km = None
    # Busca padrão: KM seguido de números com possíveis separadores
    km_match = re.search(r'KM\s*[:=]?\s*([\d.,\s]+)', observacao, re.IGNORECASE)
    if km_match:
        km_str = km_match.group(1)
        # Remover pontos, vírgulas e espaços (separadores de milhares)
        km_clean = re.sub(r'[.,\s]', '', km_str)
        # Pegar apenas os dígitos
        km_digits = re.search(r'(\d+)', km_clean)
        if km_digits:
            km = km_digits.group(1)
    
    # Extrair placa
    placa = None
    
    # Padrão 1: "PLACA:" ou "PLACAS:" seguido da placa
    placa_match = re.search(r'PLACAS?\s*[:=]?\s*([A-Z]{3}[0-9][A-Z0-9][0-9]{2})', observacao)
    if placa_match:
        placa = placa_match.group(1)
        return placa, km
    
    # Padrão 2: Buscar qualquer placa no formato brasileiro (antigo ou Mercosul)
    # Ignorar se for parte de KM ou número
    placa_match = re.search(r'\b([A-Z]{3}[0-9][A-Z0-9][0-9]{2})\b', observacao)
    if placa_match:
        placa = placa_match.group(1)
        return placa, km
    
    # Padrão 3: Buscar placa com hífen ou espaço (ex: ABC-1234 ou ABC 1234)
    placa_match = re.search(r'([A-Z]{3}[-\s]?[0-9][A-Z0-9][0-9]{2})', observacao)
    if placa_match:
        placa = placa_match.group(1).replace('-', '').replace(' ', '')
        return placa, km
    
    return None, km

def criar_tabela_vendas():
    """Cria a tabela de vendas com estrutura atualizada"""
    conn = sqlite3.connect(r'C:\Projetos\Lubrimax\Site_Consulta\data\db.sqlite')
    cursor = conn.cursor()
    
    # Apagar tabela antiga se existir
    cursor.execute('DROP TABLE IF EXISTS vendas')
    
    # Criar tabela nova com todos os campos
    cursor.execute('''
        CREATE TABLE vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_emissao TEXT,
            numero_nf INTEGER,
            serie TEXT,
            nome_cliente TEXT,
            total_venda REAL,
            nome_vendedor TEXT,
            identificacao TEXT,
            placa TEXT,
            km TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Criar índice na coluna placa para buscas mais rápidas
    cursor.execute('CREATE INDEX idx_placa ON vendas(placa)')
    
    conn.commit()
    conn.close()
    logging.info("[OK] Tabela vendas criada com sucesso (com campo KM)")

def processar_excel():
    """Processa o arquivo Excel e retorna um DataFrame limpo com placa e KM extraídos"""
    caminho_excel = r'C:\Projetos\Lubrimax\Vendas_Lubrimax.xlsx'
    
    if not os.path.exists(caminho_excel):
        logging.error(f"[ERRO] Arquivo não encontrado: {caminho_excel}")
        return None
    
    try:
        # Ler Excel
        df = pd.read_excel(caminho_excel, engine='openpyxl')
        logging.info(f"[OK] Excel carregado com {len(df)} registros")
        logging.info(f"Colunas encontradas: {df.columns.tolist()}")
        
        # Mapear colunas do Excel para estrutura do banco
        df = df.rename(columns={
            'EMISSÃO': 'data_emissao',
            'SÉRIE': 'serie',
            'NUMERO VENDA': 'numero_nf',
            'CLIENTE': 'nome_cliente',
            'TOTAL VENDA': 'total_venda',
            'VENDEDOR': 'nome_vendedor',
            'IDENTIFICAÇÃO': 'identificacao',
            'STATUS': 'status',
            'OBSERVAÇÃO': 'observacao'
        })
        
        # Extrair placa e KM da observação
        logging.info("[INFO] Extraindo placa e KM do campo OBSERVAÇÃO...")
        
        df[['placa_extraida', 'km']] = df['observacao'].apply(
            lambda x: pd.Series(extrair_placa_km(x))
        )
        
        # Usar placa extraída ou identificação como fallback
        df['placa'] = df['placa_extraida'].fillna(df['identificacao'])
        
        # Limpar placa (remover espaços, hífens, etc)
        df['placa'] = df['placa'].apply(
            lambda x: re.sub(r'[^A-Z0-9]', '', str(x).upper()) if pd.notna(x) else None
        )
        
        # Converter data
        try:
            df['data_emissao'] = pd.to_datetime(df['data_emissao'], format='%d/%m/%Y')
            df['data_emissao'] = df['data_emissao'].dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            logging.warning("[AVISO] Erro ao converter datas, mantendo formato original")
        
        # Converter valores (tratar vírgula como decimal)
        try:
            if df['total_venda'].dtype == 'object':
                df['total_venda'] = df['total_venda'].str.replace('.', '', regex=False)
                df['total_venda'] = df['total_venda'].str.replace(',', '.', regex=False)
            df['total_venda'] = pd.to_numeric(df['total_venda'], errors='coerce')
        except:
            logging.warning("[AVISO] Erro ao converter valores")
        
        # Remover linhas sem placa
        df_limpo = df[df['placa'].notna()]
        logging.info(f"[OK] Após limpeza: {len(df_limpo)} registros com placa válida")
        
        # Estatísticas
        registros_com_km = df_limpo['km'].notna().sum()
        logging.info(f"[INFO] Registros com KM: {registros_com_km}/{len(df_limpo)}")
        
        return df_limpo
    
    except Exception as e:
        logging.error(f"[ERRO] Erro ao processar Excel: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return None

def atualizar_database(df):
    """Atualiza o banco de dados com os dados do DataFrame"""
    if df is None or len(df) == 0:
        logging.warning("[AVISO] Nenhum dado para inserir")
        return False
    
    try:
        conn = sqlite3.connect(r'C:\Projetos\Lubrimax\Site_Consulta\data\db.sqlite')
        cursor = conn.cursor()
        
        # Selecionar colunas para inserção
        colunas_inserir = [
            'data_emissao', 'numero_nf', 'serie', 'nome_cliente',
            'total_venda', 'nome_vendedor', 'identificacao',
            'placa', 'km', 'status'
        ]
        
        # Inserir dados
        registros_inseridos = 0
        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO vendas (
                        data_emissao, numero_nf, serie, nome_cliente,
                        total_venda, nome_vendedor, identificacao,
                        placa, km, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row.get('data_emissao'),
                    row.get('numero_nf'),
                    row.get('serie'),
                    row.get('nome_cliente'),
                    row.get('total_venda'),
                    row.get('nome_vendedor'),
                    row.get('identificacao'),
                    row.get('placa'),
                    row.get('km'),
                    row.get('status')
                ))
                registros_inseridos += 1
            except Exception as e:
                logging.warning(f"[AVISO] Erro ao inserir registro: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        logging.info(f"[OK] {registros_inseridos} registros inseridos no banco de dados")
        return True
    
    except Exception as e:
        logging.error(f"[ERRO] Erro ao atualizar banco de dados: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return False

def verificar_dados():
    """Verifica quantos registros existem no banco"""
    conn = sqlite3.connect(r'C:\Projetos\Lubrimax\Site_Consulta\data\db.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM vendas')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT placa) FROM vendas WHERE placa IS NOT NULL')
    total_placas = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM vendas WHERE km IS NOT NULL AND km != ""')
    total_com_km = cursor.fetchone()[0]
    
    conn.close()
    
    logging.info(f"[INFO] Total de registros: {total}")
    logging.info(f"[INFO] Total de placas únicas: {total_placas}")
    logging.info(f"[INFO] Registros com KM: {total_com_km}")
    
    return total, total_placas, total_com_km

def fazer_backup():
    """Faz backup do banco de dados antes de atualizar"""
    try:
        origem = r'C:\Projetos\Lubrimax\Site_Consulta\data\db.sqlite'
        destino = r'C:\Projetos\Lubrimax\Site_Consulta\data\backups'
        
        # Criar pasta de backups se não existir
        os.makedirs(destino, exist_ok=True)
        
        if os.path.exists(origem):
            import shutil
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(destino, f'db_backup_{timestamp}.sqlite')
            shutil.copy2(origem, backup_file)
            logging.info(f"[OK] Backup criado: {backup_file}")
            
            # Manter apenas últimos 7 backups
            backups = sorted([f for f in os.listdir(destino) if f.startswith('db_backup_')])
            if len(backups) > 7:
                for old_backup in backups[:-7]:
                    os.remove(os.path.join(destino, old_backup))
                    logging.info(f"[INFO] Backup antigo removido: {old_backup}")
        
        return True
    except Exception as e:
        logging.warning(f"[AVISO] Erro ao fazer backup: {e}")
        return False

def main():
    """Função principal"""
    logging.info("=" * 60)
    logging.info("🔄 Iniciando atualização do banco de dados Lubrimax")
    logging.info("=" * 60)
    
    # Passo 1: Fazer backup
    fazer_backup()
    
    # Passo 2: Criar/recriar tabela
    criar_tabela_vendas()
    
    # Passo 3: Processar Excel
    df = processar_excel()
    
    if df is None:
        logging.error("❌ Falha ao processar Excel")
        return False
    
    # Passo 4: Atualizar banco de dados
    sucesso = atualizar_database(df)
    
    if sucesso:
        # Passo 5: Verificar dados inseridos
        total, placas, com_km = verificar_dados()
        
        logging.info("=" * 60)
        logging.info("✅ Atualização do banco de dados concluída com sucesso!")
        logging.info(f"📊 Resumo:")
        logging.info(f"   • Total de registros: {total}")
        logging.info(f"   • Placas únicas: {placas}")
        logging.info(f"   • Registros com KM: {com_km}")
        logging.info("=" * 60)
        
        return True
    else:
        logging.error("=" * 60)
        logging.error("❌ Falha na atualização do banco de dados")
        logging.error("=" * 60)
        return False

if __name__ == "__main__":
    try:
        sucesso = main()
        if not sucesso:
            input("\nPressione ENTER para sair...")
    except Exception as e:
        logging.error(f"[ERRO CRÍTICO] {e}")
        import traceback
        logging.error(traceback.format_exc())
        input("\nPressione ENTER para sair...")
