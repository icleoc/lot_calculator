import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Calculadora de Lotes Jarvis", page_icon="📊")

st.title("📊 Calculadora de Lotes e Margem")
st.markdown("---")

# 1. Inputs do Usuário
col1, col2 = st.columns(2)

with col1:
    margem_livre = st.number_input("Margem Livre Disponível ($)", min_value=0.0, value=1000.0, step=100.0)
    alavancagem = st.number_input("Alavancagem (ex: 500 para 1:500)", min_value=1, value=500)

with col2:
    # Dicionário de ativos comuns e seus Contract Sizes padrão
    ativos_comuns = {
        "Forex (Pares de Moedas)": 100000,
        "XAUUSD (Ouro)": 100,
        "XAGUSD (Prata)": 5000,
        "Nasdaq / Indices (Varia por corretora)": 100,
        "Bitcoin (BTCUSD)": 1
    }
    
    tipo_ativo = st.selectbox("Selecione o Ativo", list(ativos_comuns.keys()))
    contract_size = ativos_comuns[tipo_ativo]
    
    preco_atual = st.number_input("Preço Atual do Ativo", min_value=0.01, value=2000.0, step=0.1)

# 2. Lógica de Cálculo
# Fórmula: (Margem * Alavancagem) / (Preço * Tamanho do Contrato)
poder_compra = margem_livre * alavancagem
custo_um_lote = preco_atual * contract_size
lote_maximo = poder_compra / custo_um_lote

# 3. Exibição dos Resultados
st.markdown("---")
st.subheader("Resultado do Cálculo")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Lote Máximo (All-in)", f"{lote_maximo:.2f}")

with c2:
    # Sugestão conservadora (usando apenas 10% da margem disponível para margem retida)
    lote_seguro = (margem_livre * 0.1 * alavancagem) / custo_um_lote
    st.metric("Lote Sugerido (10% Margem)", f"{lote_seguro:.2f}")

with c3:
    st.info(f"Tamanho do Contrato: {contract_size}")

# Alerta de Risco
st.warning("**Aviso de Jarvis:** O 'Lote Máximo' não deixa espaço para oscilação de preço (drawdown). Se o preço mover 1 tick contra, a conta entra em Stop Out.")
