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

# Calculando os valores de "1 BTC (Estimado)" e "Lucro Total"
df["1 BTC (Estimado)"] = df["Valor (R$)"] / df["BTC"].replace(0, 1)  # Previne divisão por zero
df["Lucro Total (R$)"] = df.apply(lambda row: row["Valor (R$)"] - df[df["Tipo"] == "Compra"]["Valor (R$)"].sum() if row["Tipo"] == "Venda" else 0, axis=1)
df["Dinheiro em Caixa (R$)"] = df["Lucro Total (R$)"].cumsum()

# Adicionando valores de "Lucro Total" e "Dinheiro em Caixa" para cada linha
df["Lucro Total (R$)"] = df["Lucro Total (R$)"].fillna(0).cumsum()
df["Dinheiro em Caixa (R$)"] = df["Lucro Total (R$)"] + entrada_nao_usada

# Streamlit config
st.set_page_config(page_title="Dashboard BTC", layout="wide")
st.title("📊 Dashboard de Investimento em Bitcoin")

# Cabeçalho
col1, col2, col3 = st.columns(3)
col1.metric("Dinheiro Investido", f"R$ {df['Valor (R$)'].sum():,.2f}")
col2.metric("Lucro até o momento", f"R$ {df['Lucro Total (R$)'].iloc[-1]:,.2f}")
col3.metric("Dinheiro em Caixa", f"R$ {df['Dinheiro em Caixa (R$)'].iloc[-1]:,.2f}")

# Exibindo a Tabela
df_tabela = df[["Data", "Tipo", "Valor (R$)", "BTC", "1 BTC (Estimado)", "Lucro Total (R$)", "Dinheiro em Caixa (R$)"]]
st.subheader("📅 Histórico de Movimentações")
st.dataframe(df_tabela, use_container_width=True)

# Gráfico do valor pago por BTC ao longo do tempo
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Data"], y=df["Valor (R$)"], mode="lines+markers", name="Valor Pago por BTC", line=dict(color="blue")))
fig.update_layout(title="Valor Pago por BTC ao Longo do Tempo", xaxis_title="Data", yaxis_title="Valor (R$)", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Rodapé
st.caption("Desenvolvido para Diego Victor - Última atualização em 11/05/2025")
