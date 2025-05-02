import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conectar ao banco de dados
engine = create_engine('sqlite:///database/empresa.db')
df = pd.read_sql("SELECT * FROM empresas", con=engine)

# Título
st.title("📦 Dashboard de Agenciamento de Cargas - Empresas")

# KPIs principais
st.subheader("🔢 Indicadores Gerais")
col1, col2, col3 = st.columns(3)

col1.metric("Total de Cargas", len(df))
col2.metric("Valor Médio do Frete (R$)", f"{df['valor_frete'].mean():.2f}")
col3.metric("Estados Atendidos", df['estado_destino'].nunique())

# Gráfico - Cargas por Estado de Destino
st.subheader("📍 Distribuição de Cargas por Estado de Destino")
cargas_por_estado = df['estado_destino'].value_counts().reset_index()
cargas_por_estado.columns = ['Estado', 'Quantidade']
fig = px.bar(cargas_por_estado, x='Estado', y='Quantidade', color='Estado', title="Cargas por Estado")
st.plotly_chart(fig, use_container_width=True)

# Gráfico - Tipo de Carga mais comum
st.subheader("📦 Tipos de Carga mais Comuns")
tipos = df['tipo_carga'].value_counts().head(10).reset_index()
tipos.columns = ['Tipo de Carga', 'Total']
fig2 = px.pie(tipos, names='Tipo de Carga', values='Total', title='Top 10 Tipos de Carga')
st.plotly_chart(fig2, use_container_width=True)
