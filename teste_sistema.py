"""
Script de teste para validar a estrutura do Excel e do banco de dados
"""

import os
import sqlite3
import pandas as pd

def teste_excel():
    """Testa se o arquivo Excel existe e mostra sua estrutura"""
    print("\n" + "="*50)
    print("📊 TESTE 1: Arquivo Excel")
    print("="*50)
    
    caminho = r'C:\Projetos\Lubrimax\Vendas_Lubrimax.xlsx'
    
    if not os.path.exists(caminho):
        print("❌ Arquivo Excel NÃO encontrado!")
        print(f"   Esperado em: {caminho}")
        return False
    
    print(f"✅ Arquivo encontrado: {caminho}")
    
    try:
        df = pd.read_excel(caminho, engine='openpyxl')
        print(f"✅ Total de linhas: {len(df)}")
        print(f"✅ Total de colunas: {len(df.columns)}")
        print(f"\n📋 Colunas encontradas:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")
        
        print(f"\n📊 Primeiras 3 linhas:")
        print(df.head(3).to_string())
        
        # Verificar se tem placa
        if 'placa' in df.columns.str.lower() or 'PLACA' in df.columns:
            col_placa = [c for c in df.columns if 'placa' in c.lower()][0]
            placas_validas = df[df[col_placa].notna() & (df[col_placa] != '')]
            print(f"\n✅ Registros com placa: {len(placas_validas)}")
        else:
            print(f"\n⚠️ Coluna 'placa' não encontrada!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler Excel: {e}")
        return False

def teste_banco():
    """Testa o banco de dados"""
    print("\n" + "="*50)
    print("🗄️  TESTE 2: Banco de Dados")
    print("="*50)
    
    caminho = r'C:\Projetos\Lubrimax\Site_Consulta\data\db.sqlite'
    
    if not os.path.exists(caminho):
        print("❌ Banco de dados NÃO encontrado!")
        print(f"   Esperado em: {caminho}")
        return False
    
    print(f"✅ Banco encontrado: {caminho}")
    
    try:
        conn = sqlite3.connect(caminho)
        cursor = conn.cursor()
        
        # Verificar se tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vendas'")
        if cursor.fetchone():
            print("✅ Tabela 'vendas' existe")
            
            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM vendas")
            total = cursor.fetchone()[0]
            print(f"✅ Total de registros: {total}")
            
            # Contar placas únicas
            cursor.execute("SELECT COUNT(DISTINCT placa) FROM vendas WHERE placa IS NOT NULL")
            placas = cursor.fetchone()[0]
            print(f"✅ Placas únicas: {placas}")
            
            # Mostrar estrutura
            cursor.execute("PRAGMA table_info(vendas)")
            colunas = cursor.fetchall()
            print(f"\n📋 Estrutura da tabela:")
            for col in colunas:
                print(f"   - {col[1]} ({col[2]})")
            
            # Mostrar amostra de dados
            if total > 0:
                cursor.execute("SELECT * FROM vendas LIMIT 3")
                colunas_nomes = [desc[0] for desc in cursor.description]
                print(f"\n📊 Amostra de dados:")
                for i, row in enumerate(cursor.fetchall(), 1):
                    print(f"\n   Registro {i}:")
                    for col_nome, valor in zip(colunas_nomes, row):
                        print(f"      {col_nome}: {valor}")
        else:
            print("⚠️ Tabela 'vendas' NÃO existe")
            print("   Execute: python atualizar_database.py")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")
        return False

def teste_app():
    """Testa se o app.py pode ser executado"""
    print("\n" + "="*50)
    print("🌐 TESTE 3: Aplicação Streamlit")
    print("="*50)
    
    caminho = r'C:\Projetos\Lubrimax\Site_Consulta\app.py'
    
    if not os.path.exists(caminho):
        print("❌ app.py NÃO encontrado!")
        return False
    
    print(f"✅ app.py encontrado: {caminho}")
    
    # Verificar imports
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        if 'import streamlit' in conteudo:
            print("✅ Import do Streamlit OK")
        else:
            print("⚠️ Import do Streamlit não encontrado")
            
        if 'database' in conteudo or 'sqlite' in conteudo:
            print("✅ Conexão com banco detectada")
        else:
            print("⚠️ Conexão com banco não detectada")
            
        print(f"\n💡 Para testar o app, execute:")
        print(f"   cd C:\\Projetos\\Lubrimax\\Site_Consulta")
        print(f"   streamlit run app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler app.py: {e}")
        return False

def teste_git():
    """Verifica configuração do Git"""
    print("\n" + "="*50)
    print("🐙 TESTE 4: Configuração Git")
    print("="*50)
    
    try:
        import subprocess
        
        # Verificar se está em um repositório git
        result = subprocess.run(['git', 'status'], capture_output=True, text=True, cwd=r'C:\Projetos\Lubrimax')
        
        if result.returncode == 0:
            print("✅ Repositório Git inicializado")
            
            # Verificar remote
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True, cwd=r'C:\Projetos\Lubrimax')
            if result.stdout:
                print("✅ Remote configurado:")
                print(f"   {result.stdout.strip()}")
            else:
                print("⚠️ Nenhum remote configurado")
                print("   Execute: git remote add origin URL_DO_SEU_REPO")
        else:
            print("⚠️ Não é um repositório Git")
            print("   Execute: git init")
            
        return True
        
    except Exception as e:
        print(f"⚠️ Git não disponível: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("🧪 SUITE DE TESTES - AUTOMAÇÃO LUBRIMAX")
    print("="*70)
    
    resultados = []
    
    resultados.append(("Excel", teste_excel()))
    resultados.append(("Banco", teste_banco()))
    resultados.append(("App", teste_app()))
    resultados.append(("Git", teste_git()))
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)
    
    for nome, sucesso in resultados:
        status = "✅ PASSOU" if sucesso else "❌ FALHOU"
        print(f"{nome:15} {status}")
    
    total = len(resultados)
    passou = sum(1 for _, s in resultados if s)
    
    print("\n" + "="*70)
    print(f"🎯 Total: {passou}/{total} testes passaram")
    print("="*70)
    
    if passou == total:
        print("🎉 Todos os testes passaram! Sistema pronto para uso!")
    else:
        print("⚠️ Alguns testes falharam. Verifique as mensagens acima.")

if __name__ == "__main__":
    main()
