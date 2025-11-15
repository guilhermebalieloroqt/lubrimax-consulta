import streamlit as st
from database import buscar_por_placa
from PIL import Image
import re

# Configurações iniciais
st.set_page_config(page_title="Lubrimax - Consulta por Placa", layout="centered")

# Carregar logo
logo = Image.open("data/LOGO_png-removebg-preview.png")
st.image(logo, width=250)

st.title("🔎 Consulta de Vendas por Placa")

def validar_placa(placa):
    placa = placa.upper()
    return bool(re.match(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$', placa))

placa = st.text_input("Digite a placa do veículo (ex: ABC1234 ou ABC1C23):").strip().upper()

if st.button("Consultar"):
    if validar_placa(placa):
        resultado = buscar_por_placa(placa)
        if resultado:
            st.success("✅ Registro encontrado!")
            for venda in resultado:
                with st.container():
                    col1, col2 = st.columns(2)
                    col1.markdown("**Cliente:** " + venda['nome_cliente'])
                    col2.markdown("**Data da Venda:** " + venda['data_emissao'])
                    
                    col1.markdown("**Placa/Modelo:** " + venda['identificacao'])
                    col2.markdown("**Valor:** R$ {:.2f}".format(venda['total_venda']))
                    
                    col1.markdown("**Vendedor:** " + venda['nome_vendedor'])
                    col2.markdown("**Status:** " + venda['status'])
                    
                    st.markdown("---")
        else:
            st.warning("Nenhum registro encontrado para essa placa.")
    else:
        st.error("Placa inválida. Use o formato ABC1234 ou ABC1C23.")
