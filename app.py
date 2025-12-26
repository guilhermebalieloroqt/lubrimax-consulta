import streamlit as st
from database import buscar_por_placa
from PIL import Image
import re

# Configurações iniciais
st.set_page_config(
    page_title="Lubrimax - Consulta por Placa",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado com as cores da Lubrimax
st.markdown("""
    <style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Tema principal */
    :root {
        --lubrimax-yellow: #FFD700;
        --lubrimax-dark: #1a1a1a;
        --lubrimax-gray: #2d2d2d;
        --text-primary: #ffffff;
        --text-secondary: #cccccc;
    }
    
    /* Background geral */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Estilo do header */
    .header-container {
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-bottom: 2rem;
    }
    
    .main-title {
        color: var(--lubrimax-yellow);
        font-size: 2.5rem;
        font-weight: 700;
        margin: 1rem 0 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Estilo dos inputs */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 215, 0, 0.3);
        border-radius: 10px;
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--lubrimax-yellow);
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2);
        background-color: rgba(255, 255, 255, 0.15);
    }
    
    /* Botão customizado */
    .stButton > button {
        background: linear-gradient(135deg, var(--lubrimax-yellow) 0%, #FFA500 100%);
        color: var(--lubrimax-dark);
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 3rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
    }
    
    /* Cards de resultado */
    .result-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%);
        border-radius: 15px;
        border-left: 5px solid var(--lubrimax-yellow);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(255, 215, 0, 0.2);
    }
    
    /* Títulos e labels */
    .info-label {
        color: var(--lubrimax-yellow);
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    
    .info-value {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-autorizada {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
        color: #1a1a1a;
    }
    
    /* Alertas customizados */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border-left: 4px solid var(--lubrimax-yellow);
    }
    
    /* Divisores */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--lubrimax-yellow), transparent);
        margin: 2rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: var(--text-secondary);
        padding: 2rem 0 1rem 0;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    /* Ajustes de colunas */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Remover padding extra */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Melhorias de legibilidade */
    p, span, div {
        color: var(--text-primary);
    }
    
    /* Estilo para markdown */
    .stMarkdown {
        color: var(--text-primary);
    }
    </style>
""", unsafe_allow_html=True)

# Header com logo
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    try:
        logo = Image.open("data/LOGO_png-removebg-preview.png")
        st.image(logo, width='stretch')
    except:
        st.warning("Logo não encontrada")

# Título principal
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">🔎 Consulta de Vendas por Placa</h1>
        <p class="subtitle">Sistema de consulta rápida e eficiente</p>
    </div>
""", unsafe_allow_html=True)

def validar_placa(placa):
    """Valida formato de placa brasileira (antigo e Mercosul)"""
    placa = placa.upper()
    return bool(re.match(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$', placa))

def formatar_km(km):
    """Formata KM para exibição"""
    if not km or km == '' or km == 'None':
        return "KM não disponível"
    
    try:
        # Formatar com separador de milhares
        km_int = int(km)
        return f"{km_int:,} km".replace(',', '.')
    except:
        return str(km) + " km"

# Campo de entrada
placa = st.text_input(
    "📋 Digite a placa do veículo",
    placeholder="Ex: ABC1234 ou ABC1D23",
    help="Digite a placa no formato brasileiro (7 caracteres)",
    max_chars=7,
    label_visibility="visible"
).strip().upper()

# Botão de consulta
if st.button("🔍 Consultar Agora", type="primary"):
    if not placa:
        # Mensagem pedindo para digitar a placa
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 165, 0, 0.2) 0%, rgba(255, 165, 0, 0.2) 100%);
                        border-left: 5px solid #FFA500;
                        border-radius: 10px;
                        padding: 1.5rem;
                        margin: 1.5rem 0;
                        text-align: center;'>
                <h3 style='color: #FFA500; margin: 0 0 0.5rem 0;'>⚠️ Digite uma placa!</h3>
                <p style='color: #cccccc; margin: 0;'>Por favor, digite a placa do veículo no campo acima</p>
                <p style='color: var(--lubrimax-yellow); margin: 0.5rem 0 0 0; font-weight: 600;'>Formato: ABC1234 ou ABC1D23</p>
            </div>
        """, unsafe_allow_html=True)
    elif not validar_placa(placa):
        # Mensagem de erro para placa inválida
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(255, 77, 77, 0.2) 100%);
                        border-left: 5px solid #ff6b6b;
                        border-radius: 10px;
                        padding: 1.5rem;
                        margin: 1.5rem 0;
                        text-align: center;'>
                <h3 style='color: #ff6b6b; margin: 0 0 0.5rem 0;'>❌ Placa inválida!</h3>
                <p style='color: #cccccc; margin: 0;'>Use o formato correto:</p>
                <p style='color: var(--lubrimax-yellow); margin: 0.5rem 0 0 0; font-weight: 600;'>ABC1234 (antigo) ou ABC1D23 (Mercosul)</p>
            </div>
        """, unsafe_allow_html=True)
    elif validar_placa(placa):
        with st.spinner("🔄 Buscando informações..."):
            resultado = buscar_por_placa(placa)
        
        if resultado:
            # Mensagem de sucesso estilizada
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(0, 255, 136, 0.2) 0%, rgba(0, 204, 111, 0.2) 100%);
                            border-left: 5px solid #00ff88;
                            border-radius: 10px;
                            padding: 1rem;
                            margin: 1.5rem 0;'>
                    <h3 style='color: #00ff88; margin: 0;'>✅ {len(resultado)} registro(s) encontrado(s)!</h3>
                    <p style='color: #cccccc; margin: 0.5rem 0 0 0;'>Veículo: <strong>{placa}</strong></p>
                </div>
            """, unsafe_allow_html=True)
            
            for idx, venda in enumerate(resultado, 1):
                # Card de resultado com estilo
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                
                with st.container():
                    # Cabeçalho do registro
                    if len(resultado) > 1:
                        st.markdown(f"<h2 style='color: var(--lubrimax-yellow); margin-bottom: 1.5rem;'>📄 Registro #{idx}</h2>", unsafe_allow_html=True)
                    
                    # Criar 3 colunas
                    col1, col2, col3 = st.columns(3)
                    
                    # Coluna 1
                    with col1:
                        st.markdown("<p class='info-label'>👤 Cliente</p>", unsafe_allow_html=True)
                        st.markdown(f"<p class='info-value'>{venda['nome_cliente'] or 'Não informado'}</p>", unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        st.markdown("<p class='info-label'>📅 Data da Venda</p>", unsafe_allow_html=True)
                        # Formatar data
                        data = venda['data_emissao']
                        if data:
                            try:
                                from datetime import datetime
                                dt = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
                                data_formatada = dt.strftime('%d/%m/%Y')
                                st.markdown(f"<p class='info-value'>{data_formatada}</p>", unsafe_allow_html=True)
                            except:
                                st.markdown(f"<p class='info-value'>{data}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown("<p class='info-value' style='color: #888;'>Não informado</p>", unsafe_allow_html=True)
                    
                    # Coluna 2
                    with col2:
                        st.markdown("<p class='info-label'>🚗 Placa</p>", unsafe_allow_html=True)
                        placa_venda = venda['placa'] or "Não informado"
                        st.markdown(f"<p class='info-value'>{placa_venda}</p>", unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        st.markdown("<p class='info-label'>🛣️ Quilometragem</p>", unsafe_allow_html=True)
                        km_formatado = formatar_km(venda.get('km'))
                        color = "#888" if km_formatado == "KM não disponível" else "white"
                        st.markdown(f"<p class='info-value' style='color: {color};'>{km_formatado}</p>", unsafe_allow_html=True)
                    
                    # Coluna 3
                    with col3:
                        st.markdown("<p class='info-label'>💰 Valor Total</p>", unsafe_allow_html=True)
                        valor = venda['total_venda']
                        if valor:
                            valor_formatado = f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                            st.markdown(f"<p class='info-value' style='color: #00ff88; font-weight: 700; font-size: 1.3rem;'>{valor_formatado}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown("<p class='info-value'>R$ 0,00</p>", unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        st.markdown("<p class='info-label'>📋 Status</p>", unsafe_allow_html=True)
                        status = venda['status'] or "Não informado"
                        if status == "AUTORIZADA":
                            st.markdown(f"<span class='status-badge status-autorizada'>{status}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<span class='status-badge' style='background: rgba(100, 149, 237, 0.3); color: #6495ED;'>{status}</span>", unsafe_allow_html=True)
                    
                    # Informações adicionais (linha completa)
                    st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
                    info_col1, info_col2 = st.columns(2)
                    
                    with info_col1:
                        st.markdown("<p class='info-label'>🔧 Identificação</p>", unsafe_allow_html=True)
                        identificacao = venda['identificacao'] or "Não informado"
                        color = "#888" if identificacao == "Não informado" else "white"
                        st.markdown(f"<p class='info-value' style='color: {color};'>{identificacao}</p>", unsafe_allow_html=True)
                    
                    with info_col2:
                        st.markdown("<p class='info-label'>👨‍💼 Vendedor</p>", unsafe_allow_html=True)
                        vendedor = venda['nome_vendedor'] or "Não informado"
                        color = "#888" if vendedor == "Não informado" else "white"
                        st.markdown(f"<p class='info-value' style='color: {color};'>{vendedor}</p>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Espaço entre registros
                if idx < len(resultado):
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            # Mensagem de nenhum resultado encontrado
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(255, 165, 0, 0.2) 0%, rgba(255, 107, 107, 0.2) 100%);
                            border-left: 5px solid #FFA500;
                            border-radius: 10px;
                            padding: 1.5rem;
                            margin: 1.5rem 0;
                            text-align: center;'>
                    <h3 style='color: #FFA500; margin: 0 0 0.5rem 0;'>⚠️ Nenhum registro encontrado</h3>
                    <p style='color: #cccccc; margin: 0;'>Não encontramos vendas para a placa <strong>{placa}</strong></p>
                    <p style='color: #888; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>💡 Verifique se a placa está correta e tente novamente</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
    <div class="footer">
        <p style='font-size: 0.9rem; margin-bottom: 0.5rem;'>
            💡 <strong style='color: var(--lubrimax-yellow);'>Sistema de Consulta Lubrimax</strong>
        </p>
        <p style='font-size: 0.8rem; margin-top: 1rem; color: #666;'>
            📍 Av. Colombo, 6624 - Zona 7, Maringá - PR | 📞 (44) 3029-8020
        </p>
    </div>
""", unsafe_allow_html=True)
