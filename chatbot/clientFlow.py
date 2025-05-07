import streamlit as st
import pandas as pd
from database import salvar_empresa, salvar_motorista

st.title('Agenciamento de Cargas')

estados_brasil = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG',
    'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

if 'flow_step' not in st.session_state:
    st.session_state['flow_step'] = 'initial_choice'

# ETAPA INICIAL - ESCOLHA DO TIPO DE USUÁRIO
if st.session_state['flow_step'] == 'initial_choice':
    st.write('Olá! Bem-vindo ao nosso sistema de agenciamento de cargas.')
    with st.form(key='user_type_form'):
        user_type = st.radio('Você está:', ('Buscando cargas', 'Buscando motoristas parceiros'))
        submit_button = st.form_submit_button(label='Confirmar')

    if submit_button:
        if user_type == 'Buscando motoristas parceiros':
            st.session_state['user_type'] = 'empresa'
            st.session_state['flow_step'] = 'empresa_form1'
        else:
            st.session_state['user_type'] = 'caminhoneiro'
            st.session_state['flow_step'] = 'motorista_form1'
        st.rerun()

# EMPRESA - FORMULÁRIOS

elif st.session_state['flow_step'] == 'empresa_form1':
    with st.form(key='empresa_form1'):
        st.write('### 🏢 Dados da Empresa')
        nome_empresa = st.text_input('Nome da empresa:')
        cnpj_empresa = st.text_input('CNPJ:')
        telefone_empresa = st.text_input('Telefone de contato:')
        next_button = st.form_submit_button(label='Próximo')

    if next_button:
        st.session_state.update({
            'nome_empresa': nome_empresa,
            'cnpj_empresa': cnpj_empresa,
            'telefone_empresa': telefone_empresa,
            'flow_step': 'empresa_form2'
        })
        st.rerun()

elif st.session_state['flow_step'] == 'empresa_form2':
    with st.form(key='empresa_form2'):
        st.write('### 🚚 Informações da Carga')
        cidade_origem = st.text_input('Cidade de origem:')
        estado_origem = st.selectbox('Estado de origem:', estados_brasil)
        cidade_destino = st.text_input('Cidade de destino:')
        estado_destino = st.selectbox('Estado de destino:', estados_brasil)
        tipo_carga = st.selectbox('Tipo da carga:', ['barrilha', 'apara de papel', 'cimento', 'telha', 'bobina de ferro', 'piso', 'outros'])
        valor_frete = st.number_input('Valor do frete (R$)', min_value=0.0)
        if tipo_carga == 'outros':
            tipo_carga = st.text_input('Especifique o tipo de carga:')
        next_button = st.form_submit_button(label='Próximo')

    if next_button:
        st.session_state.update({
            'cidade_origem': cidade_origem,
            'estado_origem': estado_origem,
            'cidade_destino': cidade_destino,
            'estado_destino': estado_destino,
            'tipo_carga': tipo_carga,
            'valor_frete': valor_frete,
            'flow_step': 'empresa_form3'
        })
        st.rerun()

elif st.session_state['flow_step'] == 'empresa_form3':
    with st.form(key='empresa_form3'):
        st.write('### 🌍 Detalhes do Frete')
        frete = st.selectbox('Frete inclui pedágio?', ['Sim', 'Não'])
        forma_pagamento = st.selectbox('Forma de pagamento:', ['Pix', 'Cartão', 'Dinheiro'])
        data_carregamento = st.date_input('Data de carregamento')
        data_descarregamento = st.date_input('Data de descarregamento')
        implemento = st.selectbox('Implemento necessário:', ['lona', 'cinta', 'corda', 'cantoneiras', 'paletes', 'forro', 'pro chão', 'gancho', 'tapete de borracha', 'nenhum', 'outros'])
        if implemento == 'outros':
            implemento = st.text_input('Especifique o implemento:')
        foto_caminhao = st.selectbox('Exigir fotos do caminhão?', ['Sim', 'Não'])
        tipo_caminhao = st.selectbox('Tipo de caminhão:', ['Caminhão 3/4 ou VUC', 'Caminhão toco', 'Caminhão truck', 'Cavalo mecânico simples', 'Cavalo mecânico trucado', 'Carreta 2 eixos', 'Carreta 3 eixos', 'Bitrem ou treminhão', 'Rodotrem', 'Caminhão comboio', 'Caminhão basculante', 'Caminhão-tanque', 'Prancha', 'Munck'])
        tipo_carroceria = st.selectbox('Tipo de carroceria:', ['Caçamba ou baú', 'Tanque', 'Frigorífica', 'Sider', 'Carrocerias abertas', 'Basculante', 'Boiadeira', 'Florestal', 'Grade alta', 'Grade baixa', 'Munck', 'Poliguindaste', 'Prancha'])
        tamanho_carroceria = st.number_input('Tamanho da carroceria (em metros):', min_value=0.0)
        finalizar = st.form_submit_button('Finalizar Cadastro')

    if finalizar:
        st.session_state.update({
            'frete': frete,
            'forma_pagamento': forma_pagamento,
            'data_carregamento': data_carregamento,
            'data_descarregamento': data_descarregamento,
            'implemento': implemento,
            'foto_caminhao': foto_caminhao,
            'tipo_caminhao': tipo_caminhao,
            'tipo_carroceria': tipo_carroceria,
            'tamanho_carroceria': tamanho_carroceria
        })
        campos_empresa = [
            'nome_empresa', 'cnpj_empresa', 'telefone_empresa',
            'cidade_origem', 'estado_origem', 'cidade_destino', 'estado_destino',
            'tipo_carga', 'valor_frete', 'frete', 'forma_pagamento',
            'data_carregamento', 'data_descarregamento', 'implemento',
            'foto_caminhao', 'tipo_caminhao', 'tipo_carroceria', 'tamanho_carroceria'
        ]
        dados_empresa = {k: st.session_state[k] for k in campos_empresa if k in st.session_state}
        salvar_empresa(**dados_empresa)
        st.success('Cadastro da empresa finalizado com sucesso!')
        st.dataframe(pd.DataFrame([dados_empresa]))

# CAMINHONEIRO - FORMULÁRIOS

elif st.session_state['flow_step'] == 'motorista_form1':
    with st.form(key='motorista_form1'):
        st.write('### 🚗 Dados Pessoais do Caminhoneiro')
        nome_caminhoneiro = st.text_input('Nome Completo:')
        cpf_caminhoneiro = st.text_input('CPF:')
        rg_caminhoneiro = st.text_input('RG:')
        telefone_caminhoneiro = st.text_input('Telefone para contato:')
        # foto_cnh REMOVIDO
        next_button = st.form_submit_button('Próximo')

    if next_button:
        st.session_state.update({
            'nome_caminhoneiro': nome_caminhoneiro,
            'cpf_caminhoneiro': cpf_caminhoneiro,
            'rg_caminhoneiro': rg_caminhoneiro,
            'telefone_caminhoneiro': telefone_caminhoneiro,
            'flow_step': 'motorista_form2'
        })
        st.rerun()

elif st.session_state['flow_step'] == 'motorista_form2':
    with st.form(key='motorista_form2'):
        st.write('### 💳 Dados Bancários')
        nome_banco = st.text_input('Nome do Banco:')
        agencia = st.text_input('Agência:')
        conta = st.text_input('Conta:')
        tipo_conta = st.selectbox('Tipo da Conta:', ['Conta Corrente', 'Conta Poupança'])
        chave_pix = st.text_input('Chave Pix (opcional):')
        next_button = st.form_submit_button('Próximo')

    if next_button:
        st.session_state.update({
            'nome_banco': nome_banco,
            'agencia': agencia,
            'conta': conta,
            'tipo_conta': tipo_conta,
            'chave_pix': chave_pix,
            'flow_step': 'motorista_form3'
        })
        st.rerun()

elif st.session_state['flow_step'] == 'motorista_form3':
    with st.form(key='motorista_form3'):
        st.write('### 🚚 Veículo e Vinculação')
        # doc_caminhao, fotos_caminhao REMOVIDOS
        antt = st.selectbox('Possui ANTT?', ['Sim', 'Não'])
        fretebras = st.selectbox('Possui Fretebras?', ['Sim', 'Não'])
        motorista_empresa = st.selectbox('Motorista de empresa?', ['Sim', 'Não'])

        if motorista_empresa == 'Sim':
            with st.expander('Dados da empresa:'):
                nome_empresa = st.text_input('Nome da empresa:')
                cnpj_empresa = st.text_input('CNPJ da empresa:')
                telefone_empresa = st.text_input('Telefone da empresa:')
                st.session_state.update({
                    'nome_empresa': nome_empresa,
                    'cnpj_empresa': cnpj_empresa,
                    'telefone_empresa': telefone_empresa
                })

        finalizar = st.form_submit_button('Finalizar Cadastro')

    if finalizar:
        st.session_state.update({
            'antt': antt,
            'fretebras': fretebras,
            'motorista_empresa': motorista_empresa
        })
        campos_motorista = [
            'nome_caminhoneiro', 'cpf_caminhoneiro', 'rg_caminhoneiro', 'telefone_caminhoneiro',
            'nome_banco', 'agencia', 'conta', 'tipo_conta', 'chave_pix',
            'antt', 'fretebras', 'motorista_empresa',
            'nome_empresa', 'cnpj_empresa', 'telefone_empresa'
        ]
        dados_motorista = {k: st.session_state[k] for k in campos_motorista if k in st.session_state}
        salvar_motorista(**dados_motorista)
        st.success('Cadastro do caminhoneiro finalizado com sucesso!')
        st.dataframe(pd.DataFrame([dados_motorista]))
