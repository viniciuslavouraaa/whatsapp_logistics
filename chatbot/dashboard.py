import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from datetime import date
import json
import requests

#  Conexão com o Banco de Dados
engine = create_engine('sqlite:///database/empresa.db')
df = pd.read_sql("SELECT * FROM empresas", con=engine)

#  Barra Lateral (Sidebar)
st.sidebar.title("📋 Filtros de Visualização")

with st.sidebar.expander("🔎 Filtros Personalizados"):
    estados = st.multiselect("Estado de Destino", df['estado_destino'].unique())
    tipos_carga = st.multiselect("Tipo de Carga", df['tipo_carga'].unique())
    valor_min = st.slider("Valor Mínimo do Frete (R$)", float(df['valor_frete'].min()), float(df['valor_frete'].max()), float(df['valor_frete'].min()))

if estados:
    df = df[df['estado_destino'].isin(estados)]
if tipos_carga:
    df = df[df['tipo_carga'].isin(tipos_carga)]
df = df[df['valor_frete'] >= valor_min]

#  Título Principal
st.title("📦 Dashboard de Agenciamento de Cargas - Empresas")

if df.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros aplicados.")
else:
    # Indicadores Gerais (KPIs)
    st.subheader("🔢 Indicadores Gerais")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total de Cargas", len(df))
    col2.metric("Valor Médio do Frete (R$)", f"{df['valor_frete'].mean():.2f}")
    col3.metric("Estados Atendidos", df['estado_destino'].nunique())

    # Gráfico - Cargas por Estado
    st.markdown("---")
    st.subheader("📍 Distribuição de Cargas por Estado de Destino")
    cargas_por_estado = df['estado_destino'].value_counts().reset_index()
    cargas_por_estado.columns = ['Estado', 'Quantidade']
    fig1 = px.bar(cargas_por_estado, x='Estado', y='Quantidade', color='Estado', title="Cargas por Estado")
    st.plotly_chart(fig1, use_container_width=True)

    #  Mapa - Cargas por Estado (Choropleth)
    st.subheader("🗺️ Mapa de Cargas por Estado")

    try:
        url_geojson = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
        geojson_estados = requests.get(url_geojson).json()

        estados_nome_para_sigla = {
            'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM', 'Bahia': 'BA',
            'Ceará': 'CE', 'Distrito Federal': 'DF', 'Espírito Santo': 'ES', 'Goiás': 'GO',
            'Maranhão': 'MA', 'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG',
            'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR', 'Pernambuco': 'PE', 'Piauí': 'PI',
            'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN', 'Rio Grande do Sul': 'RS',
            'Rondônia': 'RO', 'Roraima': 'RR', 'Santa Catarina': 'SC', 'São Paulo': 'SP',
            'Sergipe': 'SE', 'Tocantins': 'TO'
        }
        sigla_para_nome = {v: k for k, v in estados_nome_para_sigla.items()}
        cargas_por_estado['Estado_Nome'] = cargas_por_estado['Estado'].map(sigla_para_nome)

        #estados_disponiveis = [f['properties']['name'] for f in geojson_estados['features']]
        #st.write("🔍 Estados no GeoJSON:", estados_disponiveis)
        #st.write("🧾 Estados com dados:", cargas_por_estado['Estado_Nome'].dropna().unique())

        mapa = px.choropleth(
            cargas_por_estado,
            geojson=geojson_estados,
            featureidkey="properties.name",
            locations='Estado_Nome',
            color='Quantidade',
            color_continuous_scale='Viridis',
            labels={'Quantidade': 'Cargas'},
        )
        mapa.update_geos(fitbounds="locations", visible=False)
        mapa.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        st.plotly_chart(mapa, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar o mapa: {e}")

    #  Gráfico - Tipos de Carga
    st.subheader("📦 Tipos de Carga mais Comuns")
    tipos = df['tipo_carga'].value_counts().head(10).reset_index()
    tipos.columns = ['Tipo de Carga', 'Total']
    fig2 = px.pie(tipos, names='Tipo de Carga', values='Total', title='Top 10 Tipos de Carga')
    st.plotly_chart(fig2, use_container_width=True)

    #  Download dos Dados
    st.subheader("💾 Exportar Dados Filtrados")
    st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), "dados_filtrados.csv", "text/csv")

#  Rodapé
st.markdown("---")
st.caption(f"Dashboard gerado em {date.today().strftime('%d/%m/%Y')} por Vinicius Lavoura")