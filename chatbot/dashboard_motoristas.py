# dashboard_motoristas.py - Análise de Motoristas

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from datetime import date

# Conexão com o banco de dados dos motoristas
engine = create_engine('sqlite:///database/motorista.db')
df = pd.read_sql('SELECT * FROM motoristas', con=engine)

# Estilo visual
st.set_page_config(page_title='Dashboard Motoristas', layout='wide')
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

# Título
st.markdown("""
    <h1 style='text-align: center; color: #1F2937;'>🚛 Dashboard de Motoristas</h1>
""", unsafe_allow_html=True)

# Filtros
with st.sidebar:
    st.title('🔍 Filtros')
    tipo_conta = st.multiselect('Tipo de Conta Bancária', df['tipo_conta'].unique())
    possui_antt = st.selectbox('Possui ANTT?', ['Todos', 'Sim', 'Não'])
    possui_fretebras = st.selectbox('Possui FreteBras?', ['Todos', 'Sim', 'Não'])

# Aplicar filtros
if tipo_conta:
    df = df[df['tipo_conta'].isin(tipo_conta)]
if possui_antt != 'Todos':
    df = df[df['antt'] == possui_antt]
if possui_fretebras != 'Todos':
    df = df[df['fretebras'] == possui_fretebras]

# Indicadores
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class='card'>
            <div class='metric-title'>Total de Motoristas</div>
            <div class='metric-value'>{len(df)}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    perc_vinculados = df[df['motorista_empresa'] == 'Sim'].shape[0] / len(df) * 100 if len(df) > 0 else 0
    st.markdown(f"""
        <div class='card'>
            <div class='metric-title'>Vinculados a Empresas (%)</div>
            <div class='metric-value'>{perc_vinculados:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    docs_validos = df[(df['antt'] == 'Sim') | (df['fretebras'] == 'Sim')].shape[0]
    st.markdown(f"""
        <div class='card'>
            <div class='metric-title'>Com Documentação (ANTT/FreteBras)</div>
            <div class='metric-value'>{docs_validos}</div>
        </div>
    """, unsafe_allow_html=True)

# Empresas com mais motoristas
st.subheader('🏢 Empresas com mais Motoristas Vinculados')
df_empresas = df[df['motorista_empresa'] == 'Sim']
top_empresas = df_empresas['nome_empresa'].value_counts().head(10).reset_index()
top_empresas.columns = ['Empresa', 'Motoristas']
fig_empresas = px.bar(top_empresas, x='Motoristas', y='Empresa', orientation='h', color='Motoristas', color_continuous_scale='blues')
fig_empresas.update_layout(yaxis=dict(autorange='reversed'))
st.plotly_chart(fig_empresas, use_container_width=True)

# Distribuição por banco
st.subheader('🏦 Distribuição de Bancos Usados')
bancos = df['nome_banco'].value_counts().head(10).reset_index()
bancos.columns = ['Banco', 'Quantidade']
fig_bancos = px.pie(bancos, names='Banco', values='Quantidade', title='Top 10 Bancos mais usados')
st.plotly_chart(fig_bancos, use_container_width=True)

# Tipos de Conta
st.subheader('💳 Tipo de Conta Bancária')
contas = df['tipo_conta'].value_counts().reset_index()
contas.columns = ['Tipo de Conta', 'Quantidade']
fig_contas = px.bar(contas, x='Tipo de Conta', y='Quantidade', color='Tipo de Conta', title='Distribuição de Contas')
st.plotly_chart(fig_contas, use_container_width=True)

# Alertas
st.subheader('⚠️ Motoristas com Pendências de Documentos')
pendentes = df[(df['antt'] == 'Não') & (df['fretebras'] == 'Não')]
if not pendentes.empty:
    st.dataframe(pendentes[['nome_caminhoneiro', 'cpf_caminhoneiro', 'telefone_caminhoneiro', 'nome_empresa']])
else:
    st.success('Todos os motoristas possuem pelo menos um documento (ANTT ou FreteBras).')

# Rodapé
st.markdown('---')
st.caption(f'Dashboard gerado em {date.today().strftime("%d/%m/%Y")} por Vinicius Lavoura')
