import streamlit as st

# Configuração visual do Jarvis
st.set_page_config(page_title="Jarvis - Calculadora de Margem", page_icon="📈", layout="centered")

st.title("📈 Jarvis: Calculadora de Lotes (Forex & Metais)")
st.markdown("---")

# 1. Definição dos Ativos e Contract Sizes
# Forex Padrão: 100.000 | Ouro: 100 | Prata: 5.000
ativos = {
    "EURUSD": 100000, "GBPUSD": 100000, "USDJPY": 100000, 
    "AUDUSD": 100000, "USDCAD": 100000, "USDCHF": 100000, 
    "NZDUSD": 100000, "EURGBP": 100000, "EURJPY": 100000,
    "GBPCHF": 100000, "XAUUSD (Ouro)": 100, "XAGUSD (Prata)": 5000
}

# 2. Interface Lateral (Sidebar) ou Central
col1, col2 = st.columns(2)

with col1:
    selecao_ativo = st.selectbox("Selecione o Ativo", list(ativos.keys()))
    margem_livre = st.number_input("Margem Livre ($)", min_value=0.0, value=1000.0, step=100.0)
    
with col2:
    alavancagem = st.number_input("Alavancagem (ex: 500 para 1:500)", min_value=1, value=500)
    preco_atual = st.number_input("Preço Atual", min_value=0.0001, value=1.0850 if "USD" in selecao_ativo else 2000.0, format="%.5f")

# 3. Lógica de Cálculo
contract_size = ativos[selecao_ativo]

# Fórmula: Lote = (Margem * Alavancagem) / (Preço * ContractSize)
if preco_atual > 0:
    lote_maximo = (margem_livre * alavancagem) / (preco_atual * contract_size)
else:
    lote_maximo = 0

# 4. Exibição de Resultados
st.markdown("---")
st.subheader("Cálculo de Capacidade")

# Estilização de métricas
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric(label="Lote Máximo Permitido", value=f"{lote_maximo:.2f}")
    st.caption("Uso de 100% da margem disponível.")

with res_col2:
    # Recomendação Jarvis (Segurança de 20% de Margem Livre)
    lote_recomendado = lote_maximo * 0.8
    st.metric(label="Lote Recomendado (80% Cap.)", value=f"{lote_recomendado:.2f}", delta_color="normal")
    st.caption("Margem de segurança para oscilação.")

# Informações Adicionais
with st.expander("Ver detalhes técnicos do ativo"):
    st.write(f"**Ativo:** {selecao_ativo}")
    st.write(f"**Tamanho do Contrato:** {contract_size:,}")
    st.write(f"**Poder de Compra Total:** ${(margem_livre * alavancagem):,.2f}")

st.info("Configurado para MetaTrader 5 (Padrão de Mercado).")
