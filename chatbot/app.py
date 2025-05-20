import streamlit as st
st.set_page_config(page_title="WhatsApp Logistics", layout="wide")
import dashboard
import dashboard_motoristas
import clientFlow

st.sidebar.title("🚚 Navegação")

opcao = st.sidebar.selectbox("Selecione o módulo:", [
    "📦 Dashboard de Empresas",
    "🚛 Dashboard de Motoristas",
    "💬 Cadastro"
])

if opcao == "📦 Dashboard de Empresas":
    dashboard.show()
elif opcao == "🚛 Dashboard de Motoristas":
    dashboard_motoristas.show()
elif opcao == "💬 Cadastro":
    clientFlow.show()
