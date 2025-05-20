import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from datetime import date
import requests


def show():
    # Conexão com banco
    df = pd.read_sql('SELECT * FROM empresas', con=create_engine('sqlite:///database/empresa.db'))

    # Estilo visual
    #st.set_page_config(page_title='Dashboard Empresas', layout='wide')
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

    # Filtros
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

    # Título
    st.markdown('<h1 style="text-align: center; color: #1F2937;">📦 Dashboard de Agenciamento de Cargas</h1>', unsafe_allow_html=True)

    if df.empty:
        st.warning('⚠️ Nenhum dado encontrado com os filtros aplicados.')
    else:
        # Indicadores
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class='card'>
                    <div class='metric-title'>Total de Cargas</div>
                    <div class='metric-value'>{len(df)}</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            valor_medio = df['valor_frete'].mean()
            valor_formatado = f"R$ {valor_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.markdown(f"""
                <div class='card'>
                    <div class='metric-title'>Valor Médio do Frete (R$)</div>
                    <div class='metric-value'>{valor_formatado}</div>
                </div>
            """, unsafe_allow_html=True)


        with col3:
            st.markdown(f"""
                <div class='card'>
                    <div class='metric-title'>Estados Atendidos</div>
                    <div class='metric-value'>{df['estado_destino'].nunique()}</div>
                </div>
            """, unsafe_allow_html=True)
            
        # Total de fretes e frete mais caro (com design unificado)
        col4, col5 = st.columns(2)

        with col4:
            total_fretes = df["valor_frete"].sum()
            total_formatado = f"R$ {total_fretes:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.markdown(f"""
                <div class='card'>
                    <div class='metric-title'>💰 Total em Fretes (R$)</div>
                    <div class='metric-value'>{total_formatado}</div>
                </div>
            """, unsafe_allow_html=True)


        with col5:
            rota_mais_cara = df[df['valor_frete'] == df['valor_frete'].max()]
            rota = f"{rota_mais_cara['cidade_origem'].values[0]} → {rota_mais_cara['cidade_destino'].values[0]}"
            valor = f"R$ {rota_mais_cara['valor_frete'].values[0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.markdown(f"""
                <div class='card'>
                    <div class='metric-title'>🏆 Frete Mais Caro</div>
                    <div class='metric-value'>{rota} ({valor})</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown('---')

        # Top 5 maiores fretes
        st.subheader('💰 5 Maiores Fretes por Rota')
        top_fretes = df.copy()
        top_fretes['Rota'] = top_fretes['cidade_origem'] + '→' + top_fretes['cidade_destino']
        top_fretes = top_fretes.sort_values(by='valor_frete', ascending=False).head(5)
        fig_top = px.bar(top_fretes, x='valor_frete', y='Rota', orientation='h', color='valor_frete',
        color_continuous_scale=['#93C5FD','#3B82F6','#1E3A8A'],  # azul escuro → azul médio → azul claro forte
        labels={'valor_frete': 'Valor do Frete (R$)', 'Rota': 'Rota'})
        fig_top.update_layout(yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig_top, use_container_width=True)

        st.markdown('---')

        # Evolução temporal
        st.subheader('📈 Evolução dos Fretes por Dia de Carregamento')
        fretes_por_dia = df.groupby('data_carregamento')['valor_frete'].mean().reset_index()
        fig_linha = px.line(fretes_por_dia, x='data_carregamento', y='valor_frete', markers=True,
                            labels={'data_carregamento': 'Data', 'valor_frete': 'Total de Fretes (R$)'})
        fig_linha.update_traces(line=dict(color='#6366F1', width=3))
        st.plotly_chart(fig_linha, use_container_width=True)

        st.markdown('---')

        # Tipos de carga
        st.subheader('📦 Tipos de Carga mais Comuns')
        tipos = df['tipo_carga'].value_counts().head(5).reset_index()
        tipos.columns = ['Tipo de Carga', 'Total']

        cores_personalizadas = [
            '#0468BF', '#7EC6F2', '#F22E2E', '#F2A2A2',
            '#80F29D'
        ]

        fig_bar_tipos = px.bar(
            tipos,
            x='Total',
            y='Tipo de Carga',
            orientation='h',
            color='Tipo de Carga',  # color pela categoria
            color_discrete_sequence=cores_personalizadas,
            title='Top 5 Tipos de Carga'
        )

        fig_bar_tipos.update_layout(
            yaxis=dict(),
            showlegend=False
        )
        st.plotly_chart(fig_bar_tipos, use_container_width=True)

        st.markdown('---')

        # Cargas por estado
        st.subheader('📍 Cargas por Estado de Destino')
        cargas_estado = df['estado_destino'].value_counts().head(10).reset_index()
        cargas_estado.columns = ['Estado', 'Quantidade']
        fig_bar = px.bar(cargas_estado, x='Estado', y='Quantidade', color='Estado', title='Cargas por Estado')
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown('---')

        # Mapa
        """
        st.subheader('🗺️ Mapa de Cargas por Estado')
        url_geojson = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
        geojson = requests.get(url_geojson).json()
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
        cargas_estado['Estado_Nome'] = cargas_estado['Estado'].map(sigla_para_nome)
        fig_mapa = px.choropleth(
            cargas_estado,
            geojson=geojson,
            locations='Estado_Nome',
            featureidkey='properties.name',
            color='Quantidade',
            color_continuous_scale=['#ff0000', '#ffbaba', '#00ff7f', '#006400'],
            labels={'Quantidade': 'Cargas'}
        )
        fig_mapa.update_geos(fitbounds='locations', visible=False)
        st.plotly_chart(fig_mapa, use_container_width=True)
        """
        st.markdown('---')

        # Formas de pagamento
        st.subheader('💳 Formas de Pagamento mais Utilizadas')
        formas_pag = df['forma_pagamento'].value_counts().reset_index()
        formas_pag.columns = ['Forma de Pagamento', 'Quantidade']
        fig_pag = px.pie(formas_pag, names='Forma de Pagamento', values='Quantidade', title='Formas de Pagamento')
        st.plotly_chart(fig_pag, use_container_width=True)

        st.markdown('---')

        # Implementos
        st.subheader('🔧 Implementos Mais Utilizados')
        implementos = df['implemento'].value_counts().head(5).reset_index()
        implementos.columns = ['Implemento', 'Quantidade']
        fig_impl = px.bar(implementos, x='Quantidade', y='Implemento', orientation='h', color='Quantidade',
        color_continuous_scale=['#93C5FD','#3B82F6','#1E3A8A'],
        title='Top 5 Implementos')
        fig_impl.update_layout(yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig_impl, use_container_width=True)

        st.markdown('---')

        # Rotas mais comuns
        """
        st.subheader('🛣️ Rotas Mais Comuns')
        df['Rota'] = df['cidade_origem'] + ' → ' + df['cidade_destino']
        rotas_comuns = df['Rota'].value_counts().head(5).reset_index()
        rotas_comuns.columns = ['Rota', 'Quantidade']

        # Defina uma lista de cores para as 5 rotas
        cores_rotas = ['#93C5FD', '#3B82F6', '#1E3A8A', '#64B5F6', '#42A5F5'] # Exemplo de 5 cores

        fig_rotas = px.bar(rotas_comuns, x='Quantidade', y='Rota', orientation='h', color='Quantidade',
        color_continuous_scale=['#93C5FD','#3B82F6','#1E3A8A'],
        title='Top 5 Rotas Mais Atendidas')
        fig_rotas.update_layout(yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig_rotas, use_container_width=True)

        st.markdown('---')
        """
        # Download
        st.subheader('💾 Exportar Dados Filtrados')
        st.download_button('📥 Baixar CSV', df.to_csv(index=False).encode('utf-8'), 'dados_filtrados.csv', 'text/csv')

    # Rodapé
    st.markdown('---')
    st.caption(f'Dashboard gerado em {date.today().strftime("%d/%m/%Y")} por Vinicius Lavoura')
