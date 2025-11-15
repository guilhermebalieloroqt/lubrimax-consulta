import sqlite3

def buscar_por_placa(placa_exata):
    """
    Busca vendas por placa no banco de dados
    
    Args:
        placa_exata: Placa do veículo (formato ABC1234 ou ABC1D23)
        
    Returns:
        Lista de dicionários com os dados das vendas
    """
    conn = sqlite3.connect("data/db.sqlite")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            id,
            data_emissao,
            numero_nf,
            serie,
            nome_cliente,
            total_venda,
            nome_vendedor,
            identificacao,
            placa,
            km,
            status
        FROM vendas
        WHERE UPPER(placa) = ?
        ORDER BY data_emissao DESC
    """, (placa_exata.upper(),))
    
    resultados = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in resultados]
