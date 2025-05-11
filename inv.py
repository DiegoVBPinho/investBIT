import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Dados das movimentações
movimentacoes = [
    {"Data": "2025-03-19", "Tipo": "Compra", "Valor (R$)": 500.00, "BTC": 0.00102448},
    {"Data": "2025-04-07", "Tipo": "Compra", "Valor (R$)": 144.22, "BTC": 0.00030581},
    {"Data": "2025-04-16", "Tipo": "Compra", "Valor (R$)": 156.00, "BTC": 0.00031237},
    {"Data": "2025-05-01", "Tipo": "Venda", "Valor (R$)": 904.91, "BTC": 0.00165440},
    {"Data": "2025-05-07", "Tipo": "Aplicação", "Valor (R$)": 200.00, "BTC": 0}
]

# Entrada disponível não utilizada
entrada_nao_usada = 200.00

# Cálculos principais
df = pd.DataFrame(movimentacoes)
df["Data"] = pd.to_datetime(df["Data"])
df = df.sort_values("Data")

total_gasto_bolso = 1000.22
lucro_realizado = df[df["Tipo"] == "Venda"]["Valor (R$)"].sum()
btc_em_carteira = df[df["Tipo"] == "Compra"]["BTC"].sum() - df[df["Tipo"] == "Venda"]["BTC"].sum()

# Dinheiro disponível = lucro + entrada ainda não usada
dinheiro_em_caixa = lucro_realizado + entrada_nao_usada

# Streamlit config
st.set_page_config(page_title="Dashboard BTC", layout="wide")
st.title("📊 Dashboard de Investimento em Bitcoin")

# Cabeçalho
col1, col2, col3 = st.columns(3)
col1.metric("Dinheiro Investido", f"R$ {total_gasto_bolso:,.2f}")
col2.metric("Lucro até o momento", f"R$ {lucro_realizado:,.2f}")
col3.metric("Dinheiro em Caixa", f"R$ {dinheiro_em_caixa:,.2f}")

# Tabela de Movimentações
df_tabela = df.copy()
df_tabela["1 BTC (Estimado)"] = df_tabela["Valor (R$)"] / df_tabela["BTC"].replace(0, 1)  # Previne divisão por zero
df_tabela["Valor Total em Tempo Real (R$)"] = df_tabela.apply(
    lambda row: row["BTC"] * df_tabela["1 BTC (Estimado)"].iloc[-1] if row["Tipo"] == "Compra" else row["1 BTC (Estimado)"],
    axis=1
)

# Exibindo a Tabela
st.subheader("📅 Histórico de Movimentações")
st.dataframe(df_tabela[["Data", "Tipo", "Valor (R$)", "1 BTC (Estimado)", "BTC", "Valor Total em Tempo Real (R$)"]], use_container_width=True)

# Gráfico do valor pago por BTC ao longo do tempo
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Data"], y=df["Valor (R$)"], mode="lines+markers", name="Valor Pago por BTC", line=dict(color="blue")))
fig.update_layout(title="Valor Pago por BTC ao Longo do Tempo", xaxis_title="Data", yaxis_title="Valor (R$)", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Rodapé
st.caption("Desenvolvido para Diego Victor - Última atualização em 11/05/2025")
