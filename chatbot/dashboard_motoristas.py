import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from datetime import date, datetime

def show():
    # Conexão com o banco de dados dos motoristas
    engine = create_engine('sqlite:///database/motorista.db')
    df = pd.read_sql('SELECT * FROM motoristas', con=engine)

    # Estilo visual
    #st.set_page_config(page_title='Dashboard Motoristas', layout='wide')
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

    # Indicadores principais
    st.markdown('## 📊 Indicadores Gerais')

    col1,col2 = st.columns(2)
    col3, col4, col5 = st.columns(3)

    # Total de motoristas
    with col1:
        st.markdown(f"""
            <div class='card'>
                <div class='metric-title'>Total de Motoristas</div>
                <div class='metric-value'>{len(df)}</div>
            </div>
        """, unsafe_allow_html=True)

    # % Vinculados a empresas
    with col2:
        perc_vinculados = df[df['motorista_empresa'] == 'Sim'].shape[0] / len(df) * 100 if len(df) > 0 else 0
        st.markdown(f"""
            <div class='card'>
                <div class='metric-title'>Vinculados a Empresas (%)</div>
                <div class='metric-value'>{perc_vinculados:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    # % com documentação completa
    with col3:
        completos = df[(df['antt'] == 'Sim') & (df['fretebras'] == 'Sim') & (df['chave_pix'].notnull())].shape[0]
        percent_completos = completos / len(df) * 100 if len(df) > 0 else 0
        st.markdown(f"""
            <div class='card'>
                <div class='metric-title'>Documentação Completa (%)</div>
                <div class='metric-value'>{percent_completos:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    # Quantos não têm nenhum documento
    with col4:
        sem_doc = df[(df['antt'] == 'Não') & (df['fretebras'] == 'Não')].shape[0]
        st.markdown(f"""
            <div class='card'>
                <div class='metric-title'>Sem Documentação Obrigatória</div>
                <div class='metric-value'>{sem_doc}</div>
            </div>
        """, unsafe_allow_html=True)

    # Com ao menos 1 documento
    with col5:
        docs_validos = df[(df['antt'] == 'Sim') | (df['fretebras'] == 'Sim')].shape[0]
        st.markdown(f"""
            <div class='card'>
                <div class='metric-title'>Com Documentação (ANTT/FreteBras)</div>
                <div class='metric-value'>{docs_validos}</div>
            </div>
        """, unsafe_allow_html=True)

        
    # Análise de Documentação
    st.markdown('## 🗃️ Análise de Documentação')
    doc_analysis = {
        'ANTT': df[df['antt'] == 'Sim'].shape[0],
        'FreteBras': df[df['fretebras'] == 'Sim'].shape[0],
        'Ambos': df[(df['antt'] == 'Sim') & (df['fretebras'] == 'Sim')].shape[0],
        'Nenhum': df[(df['antt'] == 'Não') & (df['fretebras'] == 'Não')].shape[0]
    }

    fig_doc = px.bar(
        x=list(doc_analysis.keys()),
        y=list(doc_analysis.values()),
        color=list(doc_analysis.keys()),
        title='Distribuição de Documentos',
        labels={'x': 'Documentos', 'y': 'Quantidade'}
    )

    fig_doc.update_layout(legend_title_text=None)
    st.plotly_chart(fig_doc, use_container_width=True)

    # Tabela com pendências
    """
    st.markdown('### Motoristas Sem Documentação Obrigatória')
    st.dataframe(df[(df['antt'] == 'Não') & (df['fretebras'] == 'Não')][['nome_caminhoneiro', 'cpf_caminhoneiro', 'telefone_caminhoneiro']])
    """
    # Bancos
    st.markdown('## 💸 Bancos e Formas de Pagamento')

    bancos = df['nome_banco'].value_counts().head(5).reset_index()
    bancos.columns = ['Banco', 'Quantidade']

    # Paleta personalizada
    cores_personalizadas = ['#0468BF', '#7EC6F2', '#F22E2E', '#F2A2A2', '#80F29D',
                            '#FFD700', '#FFA500', '#A569BD', '#5D6D7E', '#C0392B']  # extras para completar 10

    fig_bancos = px.bar(
        bancos,
        x='Quantidade',
        y='Banco',
        orientation='h',
        color='Banco',
        title='Top 10 Bancos mais usados',
        color_discrete_sequence=cores_personalizadas
    )

    fig_bancos.update_layout(
        yaxis=dict(),
        xaxis_title='Quantidade',
        yaxis_title='Banco'
    )

    st.plotly_chart(fig_bancos, use_container_width=True)

    # Contas
    st.markdown('## 💳 Distribuição por Tipo de Conta')

    tipos_conta = df['tipo_conta'].value_counts().reset_index()
    tipos_conta.columns = ['Tipo de Conta', 'Quantidade']

    # Cores personalizadas
    cores_conta = ['#0468BF', '#F22E2E']

    fig_contas = px.pie(
        tipos_conta,
        names='Tipo de Conta',
        values='Quantidade',
        title='Distribuição de Contas',
        color_discrete_sequence=cores_conta
    )

    st.plotly_chart(fig_contas, use_container_width=True)

    # Estados com mais motoristas (se houver estado)
    if 'estado_origem' in df.columns:
        st.markdown('## 📍 Distribuição por Estado')
        estados_motoristas = df['estado_origem'].value_counts().reset_index()
        estados_motoristas.columns = ['Estado', 'Quantidade']
        fig_estados = px.bar(estados_motoristas, x='Estado', y='Quantidade', color='Estado', title='Motoristas por Estado')
        st.plotly_chart(fig_estados, use_container_width=True)

    # Frequência de cadastro
    if 'data_cadastro' in df.columns:
        df['data_cadastro'] = pd.to_datetime(df['data_cadastro'])
        st.markdown('## 🔁 Cadastro de Motoristas ao Longo do Tempo')
        cadastros_mes = df.groupby(df['data_cadastro'].dt.to_period('M')).size().reset_index(name='Total')
        cadastros_mes['data'] = cadastros_mes['data_cadastro'].dt.to_timestamp()
        fig_line = px.line(cadastros_mes, x='data', y='Total', markers=True, title='Novos Motoristas por Mês')
        st.plotly_chart(fig_line, use_container_width=True)
        ultimos_30 = df[df['data_cadastro'] >= pd.Timestamp.today() - pd.Timedelta(days=30)].shape[0]
        st.metric('Cadastros nos últimos 30 dias', ultimos_30)

    # Alertas
    """
    st.markdown('## ⚠️ Alertas Gerenciais')
    alertas = df[(df['nome_banco'].isnull()) | (df['motorista_empresa'] == 'Não') | ((df['antt'] == 'Não') & (df['fretebras'] == 'Não'))]
    st.dataframe(alertas[['nome_caminhoneiro', 'cpf_caminhoneiro', 'nome_banco', 'motorista_empresa', 'antt', 'fretebras']])
    """
    # Comparações com empresas: empresas com mais motoristas vinculados
    if 'cnpj_empresa' in df.columns:
        st.markdown('## 🧮 Empresas com Mais Motoristas Vinculados')
        
        vinculados = df[df['motorista_empresa'] == 'Sim']
        empresas_vinculadas = vinculados.groupby('nome_empresa').size().reset_index(name='Motoristas')
        empresas_vinculadas = empresas_vinculadas[empresas_vinculadas['nome_empresa'].notnull()].sort_values(by='Motoristas', ascending=False).head(10)
        
        fig_emp = px.bar(
            empresas_vinculadas,
            x='Motoristas',
            y='nome_empresa',
            orientation='h',
            title='Top5 Empresas com Mais Motoristas',
            color='Motoristas',
            color_continuous_scale=['#93C5FD', '#3B82F6', '#1E3A8A']
        )
        fig_emp.update_layout(yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig_emp, use_container_width=True)


    # Segmentação para ações
    st.markdown('## 🎯 Segmentação Estratégica')
    with st.expander('📌 Motoristas para Atualizar Cadastro'):
        atualizar = df[(df['antt'] == 'Não') | (df['fretebras'] == 'Não') | (df['nome_banco'].isnull())]
        st.dataframe(atualizar[['nome_caminhoneiro', 'cpf_caminhoneiro', 'antt', 'fretebras', 'nome_banco']])

    with st.expander('📌 Motoristas por Região'):
        if 'estado_origem' in df.columns:
            por_regiao = df['estado_origem'].value_counts().reset_index()
            por_regiao.columns = ['Estado', 'Total']
            st.dataframe(por_regiao)

    # Rodapé
    st.markdown('---')
    st.caption(f'Dashboard gerado em {date.today().strftime("%d/%m/%Y")} por Vinicius Lavoura')
