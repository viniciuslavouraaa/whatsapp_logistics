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

    if user_type == 'Buscando motoristas parceiros':
        st.session_state['user_type'] = 'empresa'
        st.session_state['flow_step'] = 'empresa_info' # Próximo passo para empresa
             # Força o Streamlit a executar o script novamente para exibir a próxima etapa
    elif user_type == 'Buscando cargas':
        st.session_state['user_type'] = 'caminhoneiro'
        st.session_state['flow_step'] = 'motorista_info' # Próximo passo para caminhoneiro