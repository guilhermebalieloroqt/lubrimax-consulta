"""
Script de teste para validar extração de placa e KM
"""

import re
import pandas as pd

def extrair_placa_km(observacao):
    """
    Extrai placa e KM do campo observação
    """
    if pd.isna(observacao):
        return None, None
    
    observacao = str(observacao).strip().upper()
    
    # Extrair KM se existir - aceita pontos, vírgulas e espaços como separadores
    km = None
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
    placa_match = re.search(r'\b([A-Z]{3}[0-9][A-Z0-9][0-9]{2})\b', observacao)
    if placa_match:
        placa = placa_match.group(1)
        return placa, km
    
    # Padrão 3: Buscar placa com hífen ou espaço
    placa_match = re.search(r'([A-Z]{3}[-\s]?[0-9][A-Z0-9][0-9]{2})', observacao)
    if placa_match:
        placa = placa_match.group(1).replace('-', '').replace(' ', '')
        return placa, km
    
    return None, km

# Casos de teste baseados nos exemplos reais
casos_teste = [
    ("PLACA: BDI4G94", "BDI4G94", None),
    ("PLACA: BBC8906 / KM: 220.878", "BBC8906", "220878"),
    ("PLACA: ATC6530", "ATC6530", None),
    ("DUCATO EBH3J12", "EBH3J12", None),
    ("VW AYZ6J43", "AYZ6J43", None),
    ("PLACA: MMB2545", "MMB2545", None),
    ("WRV BBN9I46", "BBN9I46", None),
    ("PLACA: ETQ8D64", "ETQ8D64", None),
    ("VOYAGE AXO4450", "AXO4450", None),
    ("PLACAS: EAS5445  FXG495", "EAS5445", None),  # Primeira placa quando há múltiplas
    ("KM 265184", None, "265184"),
    ("PLACA AJD3B31  KM  265184", "AJD3B31", "265184"),
    ("PLACA: ESU6B20", "ESU6B20", None),
    ("PLACA: AYM7F18", "AYM7F18", None),
    ("PLACA: BCB4199", "BCB4199", None),
    ("PLACA AXM7F18  KM  1207403", "AXM7F18", "1207403"),
    ("PLACA: BEJ7B20", "BEJ7B20", None),
    ("PLACA: FQX1778", "FQX1778", None),
    ("UNO AVG4G69", "AVG4G69", None),
    ("PLACA: BDJ1G82", "BDJ1G82", None),
    ("PLACA: AXJ2482", "AXJ2482", None),
    ("BCS9B75", "BCS9B75", None),
    ("SCANIA AYT7G74", "AYT7G74", None),
    ("CARGO AWF2A74", "AWF2A74", None),
    ("PLACA: AZR3J78", "AZR3J78", None),
]

print("=" * 80)
print("🧪 TESTE DE EXTRAÇÃO DE PLACA E KM")
print("=" * 80)
print()

sucessos = 0
falhas = 0

for observacao, placa_esperada, km_esperado in casos_teste:
    placa_extraida, km_extraido = extrair_placa_km(observacao)
    
    # Verificar se está correto
    placa_ok = placa_extraida == placa_esperada
    km_ok = km_extraido == km_esperado
    
    if placa_ok and km_ok:
        status = "✅"
        sucessos += 1
    else:
        status = "❌"
        falhas += 1
    
    print(f"{status} Observação: {observacao}")
    print(f"   Esperado: Placa={placa_esperada}, KM={km_esperado}")
    print(f"   Extraído: Placa={placa_extraida}, KM={km_extraido}")
    
    if not placa_ok or not km_ok:
        if not placa_ok:
            print(f"   ⚠️  PLACA INCORRETA!")
        if not km_ok:
            print(f"   ⚠️  KM INCORRETO!")
    
    print()

print("=" * 80)
print(f"📊 RESULTADO: {sucessos}/{len(casos_teste)} testes passaram")
print(f"✅ Sucessos: {sucessos}")
print(f"❌ Falhas: {falhas}")
print("=" * 80)

if falhas == 0:
    print("\n🎉 TODOS OS TESTES PASSARAM! 🎉\n")
else:
    print(f"\n⚠️  {falhas} teste(s) falharam. Verifique os casos acima.\n")
