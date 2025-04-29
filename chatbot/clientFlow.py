import streamlit as st
import pandas as pd
# Em clientFlow.py
from database import salvar_empresa

st.title('Chatbot de Agênciamento de Cargas')

if 'flow_step' not in st.session_state:
    st.session_state['flow_step'] = 'initial_choice'

if st.session_state['flow_step'] == 'initial_choice':
    st.write('Olá! Bem-vindo ao nosso sistema de agenciamento de cargas.')
    
    with st.form(key='user_type_form'):
        
        user_type = st.radio(
            'Você está:',
            ('Buscando cargas', 'Buscando motoristas parceiros')
        )
        submit_button = st.form_submit_button(label='Confirmar')
        
    if submit_button:
        if user_type == 'Buscando motoristas parceiros':
            st.session_state['user_type'] = 'empresa'
            st.session_state['flow_step'] = 'empresa_info' # Próximo passo para empresa
        elif user_type == 'Buscando cargas':
            st.session_state['user_type'] = 'caminhoneiro'
            st.session_state['flow_step'] = 'motorista_info' # Próximo passo para caminhoneiro
        st.rerun()   

  # FORMULÁRIO ETAPA 1: origem, destino e tipo de carga     
elif st.session_state['flow_step'] == 'empresa_info':
    st.write('Estamos felizes que você escolheu a Lavoura Transporte para cuidar da sua carga!')
    st.write('Aqui vamos coletar algumas informações da empresa')
    
    with st.form(key='empresa_form'):
        nome_empresa = st.text_input('Qual o nome da sua empresa?')
        cidade_origem = st.text_input('📍 Cidade de origem da carga:')
        estado_origem = st.selectbox('📍 Estado de origem da carga:', [
                                        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
                                        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'])
        cidade_destino = st.text_input('🏁 Cidade de destino da carga:')
        estado_destino = st.selectbox('🏁 Estado de destino da carga:', [
                                        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
                                        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'])
        tipo_carga = st.selectbox('📦 Tipo de carga:', ['barrilha', 'apara de papel', 'cimento', 'telha', 'bobina de ferro', 'piso', 'outros'])
        valor_frete = st.number_input(label='💰 Valor do frete',value=0.0)
        
        if tipo_carga == 'outros':
           tipo_carga_outros = st.text_input('Tipo de carga:')
        
        # Condicional se frete nao incluir pedágio
        next_button = st.form_submit_button(label='Próximo')
    
    # Adiciona os valores ao st.session_state 
    if next_button:
        st.session_state['nome_empresa'] = nome_empresa
        st.session_state['cidade_origem'] = cidade_origem
        st.session_state['estado_origem'] = estado_origem
        st.session_state['cidade_destino'] = cidade_destino
        st.session_state['estado_destino'] = estado_destino
        st.session_state['tipo_carga'] = tipo_carga if tipo_carga != 'outros' else tipo_carga_outros
        st.session_state['valor_frete'] = valor_frete
        
        # Avançar para próxima etapa do formulário
        st.session_state['flow_step'] = 'empresa_form2'
        st.rerun()   
        
#FORMULÁRIO ETAPA 2: frete, pagamento, datas e implementos
elif st.session_state['flow_step'] == 'empresa_form2':
    with st.form(key='empresa_form2'):
        frete = st.selectbox('Frete inclui pedágio?', ['Sim', 'Não'])
        forma_pagamento = st.selectbox('💸 Forma de pagamento:', ['Pix', 'Cartão', 'Dinheiro'])
        data_carregamento = st.date_input('📅 Data de carregamento')
        data_descarregamento = st.date_input('📅 Data de descarregamento')
        implemento = st.selectbox('🔧 Implementos necessários', [ 'lona', 'cinta', 'corda', 'cantoneiras', 'paletes', 'forro', 'pro chão', 'gancho', 'tapete de borracha', 'nenhum', 'outros'])
        
        if implemento == 'outros':
            implemento_outros = st.text_input('Qual implemento necessário:')
    
        next_button = st.form_submit_button(label='Próximo')
        
    # Adiciona os valores ao st.session_state
    if next_button:
        st.session_state['frete'] = frete
        st.session_state['forma_pagamento'] = forma_pagamento
        st.session_state['data_carregamento'] = data_carregamento
        st.session_state['data_descarregamento'] = data_descarregamento
        st.session_state['implemento'] = implemento if implemento != 'outros' else implemento_outros
        
        # Avançar para próxima etapa do formulário
        st.session_state['flow_step'] = 'empresa_form3'
        st.rerun()

#FORMULÁRIO ETAPA 3: foto do caminhao, tipo do caminhao, tipo carroceria e tamanho
elif st.session_state['flow_step'] == 'empresa_form3':
    with st.form(key='empresa_form3'):
        foto_caminhao = st.selectbox('Exigir fotos do caminhão?',['Sim', 'Não'])
        tipo_caminhao = st.selectbox('🚛 Tipo de caminhão', [
        "Caminhão 3/4 ou VUC",
        "Caminhão toco",
        "Caminhão truck",
        "Cavalo mecânico simples",
        "Cavalo mecânico trucado",
        "Carreta 2 eixos",
        "Carreta 3 eixos",
        "Bitrem ou treminhão",
        "Rodotrem",
        "Caminhão comboio",
        "Caminhão basculante",
        "Caminhão-tanque",
        "Prancha",
        "Munck"
        ]) 
        tipo_carroceria = st.selectbox('🚚 Tipo de carroceria', [
        "Caçamba ou baú",
        "Tanque",
        "Frigorífica",
        "Sider",
        "Carrocerias abertas",
        "Basculante",
        "Boiadeira",
        "Florestal",
        "Grade alta",
        "Grade baixa",
        "Munck",
        "Poliguindaste",
        "Prancha"
    ]) 
        tamanho_carroceria = st.number_input(label='📏 Tamanho da carroceria', value= 0.00)
        
        finalizar_button = st.form_submit_button(label='Finalizar Cadastro')
        
    # Adiciona os valores ao st.session_state
    if finalizar_button:
        # Salva informações coletadas nesta etapa
        st.session_state['foto_caminhao'] = foto_caminhao
        st.session_state['tipo_caminhao'] = tipo_caminhao
        st.session_state['tipo_carroceria'] = tipo_carroceria
        st.session_state['tamanho_carroceria'] = tamanho_carroceria
        
        # Juntando todos os dados
        dados_empresa = {
            "nome_empresa": st.session_state.get("nome_empresa"),
            "cidade_origem": st.session_state.get("cidade_origem"),
            "estado_origem": st.session_state.get("estado_origem"),
            "cidade_destino": st.session_state.get("cidade_destino"),
            "estado_destino": st.session_state.get("estado_destino"),
            "tipo_carga": st.session_state.get("tipo_carga"),
            "valor_frete": st.session_state.get("valor_frete"),
            "frete": st.session_state.get("frete"),
            "forma_pagamento": st.session_state.get("forma_pagamento"),
            "data_carregamento": st.session_state.get("data_carregamento"),
            "data_descarregamento": st.session_state.get("data_descarregamento"),
            "implemento": st.session_state.get("implemento"),
            "foto_caminhao": st.session_state.get("foto_caminhao"),
            "tipo_caminhao": st.session_state.get("tipo_caminhao"),
            "tipo_carroceria": st.session_state.get("tipo_carroceria"),
            "tamanho_carroceria": st.session_state.get("tamanho_carroceria"),
    }

    # Salvar no banco de dados
    salvar_empresa(**dados_empresa)
    st.success('Cadastro realizado com sucesso!')
    st.write(pd.DataFrame([dados_empresa])) 
    
# FOMULÁRIO CAMINHONEIRO 1: nome, cnh, cpf, rg
elif st.session_state['flow_step'] == 'motorista_info':
    st.write('Estamos felizes que você escolheu a Lavoura Transporte para buscar cargas')
    st.write('Aqui vamos coletar algumas informações da empresa')
    
    with st.form(key='motorista_info'):
        nome_caminhoneiro = st.text_input('Nome Completo:')
        foto_cnh = st.file_uploader('📄 Foto da Habilitação:',type=["jpg", "jpeg", "png"])
        cpf_caminhoneiro = st.text_input('📇 Digite seu CPF:', placeholder='000.000.000-00')
        rg_caminhoneiro = st.text_input('🪪 Digite seu RG:', placeholder='00.000.000-00')
        
        next_button = st.form_submit_button(label='Próximo')
    
    if next_button:
        st.session_state['nome_caminhoneiro'] = nome_caminhoneiro
        st.session_state['foto_cnh'] = foto_cnh
        st.session_state['cpf_caminhoneiro'] = cpf_caminhoneiro
        st.session_state['rg_caminhoneiro'] = rg_caminhoneiro
        
        st.session_state['flow_step'] = 'motorista_form1'
        st.rerun()
        
elif st.session_state['flow_step'] == 'motorista_form1':

    with st.form(key='motorista_info1'):
        with st.expander('Dados Bancários (Clique para preencher)'):
            nome_banco = st.text_input('Nome do Banco:')
            agencia = st.text_input('Agência (com dígito):')
            conta = st.text_input('Conta (com dígito):')
            tipo_conta = st.selectbox('Tipo da Conta:', ['Conta Corrente', 'Conta Poupança'])
            chave_pix = st.text_input('Chave Pix (opcional):')
            
        next_button = st.form_submit_button(label='Próximo')
        
    if next_button:
        st.session_state['nome_banco'] = nome_banco
        st.session_state['agencia'] = agencia
        st.session_state['conta'] = conta
        st.session_state['tipo_conta'] = tipo_conta
        st.session_state['chave_pix'] = chave_pix
        
        st.session_state['flow_step'] = 'motorista_form2'
        st.rerun()