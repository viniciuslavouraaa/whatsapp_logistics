import streamlit as st

st.title('Chatbot de Agênciamento de Cargas')

if 'flow_step' not in st.session_state:
    st.session_state['flow_step'] = 'initial_choice'

if st.session_state['flow_step'] == 'initial_choice':
    st.write('Olá! Bem-vindo ao nosso sistema de agenciamento de cargas.')
    user_type = st.radio(
        'Você está:',
        ('Buscando cargas', 'Buscando motoristas parceiros')
    )
    if st.button('Confirmar'):
        if user_type == 'Buscando motoristas parceiros':
            st.session_state['user_type'] = 'empresa'
            st.session_state['flow_step'] = 'empresa_info' # Próximo passo para empresa
        elif user_type == 'Buscando cargas':
            st.session_state['user_type'] = 'caminhoneiro'
            st.session_state['flow_step'] = 'motorista_info' # Próximo passo para caminhoneiro
        st.rerun()   
        
elif st.session_state['flow_step'] == 'empresa_info':
    st.write('Estamos felizes que você escolheu a Lavoura Transporte para cuidar da sua carga!')
    st.write('Aqui vamos coletar algumas informações da empresa')
    # Adicione aqui os campos para coletar informações da empresa

elif st.session_state['flow_step'] == 'motorista_info':
    st.write('Estamos felizes que você escolheu a Lavoura Transporte para buscar cargas')
    st.write('Aqui vamos coletar algumas informações da empresa')
    # Adicione aqui os campos para coletar informações do caminhoneiro