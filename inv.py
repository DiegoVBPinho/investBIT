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

# Total de compras
total_gasto_bolso = df[df["Tipo"] == "Compra"]["Valor (R$)"].sum()

# Lucro realizado
lucro_realizado = df[df["Tipo"] == "Venda"]["Valor (R$)"].sum() - total_gasto_bolso

# Dinheiro disponível = lucro + entrada ainda não usada
dinheiro_em_caixa = lucro_realizado + entrada_nao_usada

# Calcular o valor de "1 BTC (Estimado)" para cada movimentação
df["1 BTC (Estimado)"] = df["Valor (R$)"] / df["BTC"].replace(0, 1)  # Previne divisão por zero

# Calcular o Lucro Total e Dinheiro em Caixa com base nas movimentações
df["Lucro Total (R$)"] = df.apply(
    lambda row: lucro_realizado if row["Tipo"] == "Venda" else 0, axis=1
)

df["Dinheiro em Caixa (R$)"] = df.apply(
    lambda row: lucro_realizado + entrada_nao_usada if row["Tipo"] == "Aplicação" else dinheiro_em_caixa, axis=1
)

# Streamlit config
st.set_page_config(page_title="Dashboard BTC", layout="wide")
st.title("📊 Dashboard de Investimento em Bitcoin")

# Cabeçalho
col1, col2, col3 = st.columns(3)
col1.metric("Dinheiro Investido", f"R$ {total_gasto_bolso:,.2f}")
col2.metric("Lucro até o momento", f"R$ {lucro_realizado:,.2f}")
col3.metric("Dinheiro em Caixa", f"R$ {dinheiro_em_caixa:,.2f}")

# Tabela de Movimentações
df_tabela = df[["Data", "Tipo", "Valor (R$)", "BTC", "1 BTC (Estimado)", "Lucro Total (R$)", "Dinheiro em Caixa (R$)"]]

# Exibindo a Tabela
st.subheader("📅 Histórico de Movimentações")
st.dataframe(df_tabela, use_container_width=True)

# Gráfico do valor pago por BTC ao longo do tempo
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Data"], y=df["Valor (R$)"], mode="lines+markers", name="Valor Pago por BTC", line=dict(color="blue")))
fig.update_layout(title="Valor Pago por BTC ao Longo do Tempo", xaxis_title="Data", yaxis_title="Valor (R$)", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Rodapé
st.caption("Desenvolvido para Diego Victor - Última atualização em 11/05/2025")
