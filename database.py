import sqlite3

def buscar_por_placa(placa_exata):
    conn = sqlite3.connect("data/db.sqlite")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM vendas
        WHERE UPPER(placa) = ?
        ORDER BY data_emissao DESC
    """, (placa_exata.upper(),))
    
    resultados = cursor.fetchall()
    conn.close()
    return [dict(row) for row in resultados]
