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

# Estilo CSS para cartões e modernização visual
st.markdown('''
    <style>
        .card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
            text-align: center;
        }
        .metric-title {
            font-weight: 600;
            color: #4B5563;
            margin-bottom: 0.3rem;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #6366F1;
        }
    </style>
''', unsafe_allow_html=True)

# Barra Lateral (Sidebar)
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_example.png/480px-Logo_example.png', width=150)
st.sidebar.title('📋 Filtros de Visualização')

with st.sidebar.expander('🔎 Filtros Personalizados'):
    estados = st.multiselect('Estado de Destino', df['estado_destino'].unique())
    tipos_carga = st.multiselect('Tipo de Carga', df['tipo_carga'].unique())
    valor_min = st.slider('Valor Mínimo do Frete (R$)', float(df['valor_frete'].min()), float(df['valor_frete'].max()), float(df['valor_frete'].min()))

if estados:
    df = df[df['estado_destino'].isin(estados)]
if tipos_carga:
    df = df[df['tipo_carga'].isin(tipos_carga)]
df = df[df['valor_frete'] >= valor_min]

# Título Principal
st.markdown('''
    <h1 style='text-align: center; color: #1F2937;'>📦 Dashboard de Agenciamento de Cargas</h1>
''', unsafe_allow_html=True)

if df.empty:
    st.warning('⚠️ Nenhum dado encontrado com os filtros aplicados.')
else:
    # Indicadores em Cards
    st.markdown('<br>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('''
            <div class='card'>
                <div class='metric-title'>Total de Cargas</div>
                <div class='metric-value'>{}</div>
            </div>
        '''.format(len(df)), unsafe_allow_html=True)

    with col2:
        st.markdown('''
            <div class='card'>
                <div class='metric-title'>Valor Médio do Frete (R$)</div>
                <div class='metric-value'>{:.2f}</div>
            </div>
        '''.format(df['valor_frete'].mean()), unsafe_allow_html=True)

    with col3:
        st.markdown('''
            <div class='card'>
                <div class='metric-title'>Estados Atendidos</div>
                <div class='metric-value'>{}</div>
            </div>
        '''.format(df['estado_destino'].nunique()), unsafe_allow_html=True)
        
    # Top 5 Maiores Fretes por Rota
    st.subheader('💰 Top 5 Maiores Fretes')
    
    top_fretes = df.copy()
    top_fretes['Rota'] = top_fretes['cidade_origem'] +  '→' + top_fretes['cidade_destino']
    top_fretes = top_fretes.sort_values(by='valor_frete', ascending=False).head(5)
    
    fig_top_fretes = px.bar(
        top_fretes,
        x='valor_frete',
        y='Rota',
        orientation='h',
        color='valor_frete',
        color_continuous_scale='blues',
        labels={'valor_frete': 'Valor do Frete (R$)', 'Rota': 'Rota'},
        title='Top 5 Maiores Fretes por Rota'
    )
    fig_top_fretes.update_layout(yaxis=dict(autorange='reversed'))
    st.plotly_chart(fig_top_fretes, use_container_width=True)
    
    # Evolução Temporal dos Fretes por Data de Carregamento
    st.subheader('📅 Evolução dos Fretes por Dia de Carregamento')
    
    fretes_por_data = df.groupby('data_carregamento')['valor_frete'].sum().reset_index()
    fretes_por_data = fretes_por_data.sort_values('data_carregamento')
    
    fig_evolucao = px.line(
        fretes_por_data,
        x='data_carregamento',
        y='valor_frete',
        markers=True,
        title='Total de Fretes por Dia',
        labels={'data_carregamento': 'Data', 'valor_frete': 'Total de Fretes (R$)'},
        template='plotly_white'
    )
    fig_evolucao.update_traces(line=dict(color='#6366F1', width=3))
    st.plotly_chart(fig_evolucao,use_container_width=True)
    
    # Gráfico - Cargas por Estado
    st.markdown('---')
    st.subheader('📍 Distribuição de Cargas por Estado de Destino')
    cargas_por_estado = df['estado_destino'].value_counts().reset_index()
    cargas_por_estado.columns = ['Estado', 'Quantidade']
    fig1 = px.bar(cargas_por_estado, x='Estado', y='Quantidade', color='Estado', title='Cargas por Estado')
    st.plotly_chart(fig1, use_container_width=True)

    # Mapa - Cargas por Estado
    st.subheader('🗺️ Mapa de Cargas por Estado')
    url_geojson = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
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

    mapa = px.choropleth(
        cargas_por_estado,
        geojson=geojson_estados,
        featureidkey='properties.name',
        locations='Estado_Nome',
        color='Quantidade',
        color_continuous_scale='Viridis',
        labels={'Quantidade': 'Cargas'}
    )
    mapa.update_geos(fitbounds='locations', visible=False)
    mapa.update_layout(margin={'r':0,'t':30,'l':0,'b':0})
    st.plotly_chart(mapa, use_container_width=True)

    # Gráfico - Tipos de Carga
    st.subheader('📦 Tipos de Carga mais Comuns')
    tipos = df['tipo_carga'].value_counts().head(10).reset_index()
    tipos.columns = ['Tipo de Carga', 'Total']
    fig2 = px.pie(tipos, names='Tipo de Carga', values='Total', title='Top 10 Tipos de Carga')
    st.plotly_chart(fig2, use_container_width=True)

    # Download dos Dados
    st.subheader('💾 Exportar Dados Filtrados')
    st.download_button('📥 Baixar CSV', df.to_csv(index=False).encode('utf-8'), 'dados_filtrados.csv', 'text/csv')

# Rodapé
st.markdown('---')
st.caption(f'Dashboard gerado em {date.today().strftime("%d/%m/%Y")} por Vinicius Lavoura')
