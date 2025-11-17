#!/usr/bin/env python3
"""
Script para processar relatório Lubrimax e extrair placa + KM da observação
"""

import pandas as pd
import sqlite3
import re
from pathlib import Path
from datetime import datetime

# Configurações
PROJECT_DIR = Path(__file__).parent
DB_PATH = PROJECT_DIR / "data" / "db.sqlite"
RELATORIO_PATH = PROJECT_DIR / "Vendas_Lubrimax.xlsx"
LOG_FILE = PROJECT_DIR / "logs" / "processar_relatorio.log"

def log(message):
    """Log messages"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    
    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

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

def processar_relatorio():
    """Processa o relatório Excel e atualiza o banco"""
    
    try:
        log("=" * 60)
        log("🔄 Iniciando processamento do relatório Lubrimax")
        log("=" * 60)
        
        # 1. Verificar arquivo
        if not RELATORIO_PATH.exists():
            log(f"❌ Erro: Arquivo não encontrado em {RELATORIO_PATH}")
            return False
        
        log(f"✅ Arquivo encontrado: {RELATORIO_PATH}")
        
        # 2. Ler Excel
        log("📖 Lendo arquivo Excel...")
        df = pd.read_excel(RELATORIO_PATH)
        log(f"✅ {len(df)} linhas lidas")
        
        # 3. Mapear colunas
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
        
        # 4. Processar observação para extrair placa e KM
        log("🔍 Extraindo placa e KM da observação...")
        
        df[['placa_extraida', 'km']] = df['observacao'].apply(
            lambda x: pd.Series(extrair_placa_km(x))
        )
        
        # Usar placa extraída ou identificação como fallback
        df['placa'] = df['placa_extraida'].fillna(df['identificacao'])
        
        # Limpar placa (remover espaços, hífens, etc)
        df['placa'] = df['placa'].apply(
            lambda x: re.sub(r'[^A-Z0-9]', '', str(x).upper()) if pd.notna(x) else None
        )
        
        # 5. Converter data
        try:
            df['data_emissao'] = pd.to_datetime(df['data_emissao'], format='%d/%m/%Y')
            df['data_emissao'] = df['data_emissao'].dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            log("⚠️ Erro ao converter datas, mantendo formato original")
        
        # 6. Converter valores
        try:
            # Tratar valores com vírgula
            if df['total_venda'].dtype == 'object':
                df['total_venda'] = df['total_venda'].str.replace('.', '', regex=False)
                df['total_venda'] = df['total_venda'].str.replace(',', '.', regex=False)
            df['total_venda'] = pd.to_numeric(df['total_venda'], errors='coerce')
        except:
            log("⚠️ Erro ao converter valores")
        
        # 7. Remover linhas vazias
        df = df.dropna(subset=['placa'], how='all')
        df = df[df['placa'].notna()]
        
        log(f"✅ {len(df)} registros válidos após limpeza")
        
        # Estatísticas
        registros_com_km = df['km'].notna().sum()
        log(f"📊 Registros com KM: {registros_com_km}/{len(df)}")
        
        # 8. Conectar ao banco
        log("🗄️ Conectando ao banco de dados...")
        DB_PATH.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 9. Recriar tabela com nova coluna KM
        log("🗑️ Recriando tabela...")
        cursor.execute("DROP TABLE IF EXISTS vendas")
        
        cursor.execute("""
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
        """)
        
        cursor.execute("CREATE INDEX idx_placa ON vendas(placa)")
        log("✅ Tabela criada com campo KM")
        
        # 10. Inserir dados
        log("💾 Inserindo dados no banco...")
        
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
                    row['data_emissao'],
                    row['numero_nf'],
                    row['serie'],
                    row['nome_cliente'],
                    row['total_venda'],
                    row['nome_vendedor'],
                    row['identificacao'],
                    row['placa'],
                    row['km'],
                    row['status']
                ))
                registros_inseridos += 1
            except Exception as e:
                log(f"⚠️ Erro ao inserir registro: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        log("=" * 60)
        log(f"✅ Processamento concluído!")
        log(f"📊 Total de registros: {registros_inseridos}")
        log(f"📊 Registros com KM: {registros_com_km}")
        log("=" * 60)
        
        return True
        
    except Exception as e:
        log(f"❌ Erro crítico: {e}")
        import traceback
        log(traceback.format_exc())
        return False

if __name__ == "__main__":
    import sys
    sucesso = processar_relatorio()
    sys.exit(0 if sucesso else 1)
