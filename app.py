import streamlit as st
from chatbot import dashboard, dashboard_motoristas, clientFlow # ajuste os caminhos se estiverem diferentes

st.set_page_config(page_title='WhatsApp Logistics', layout='wide')
st.sidebar.title('🔀 Navegação')
pagina = st.sidebar.radio('Selecione a página:', [
    'Dashboard Empresas',
    'Dashboard Motoristas',
    'Chatbot'
])

if pagina == 'Dashboard Empresas':
    dashboard.show()
elif pagina == 'Dashboard Motoristas':
    dashboard_motoristas.show()
elif pagina == 'Chatbot':
    clientFlow.show()