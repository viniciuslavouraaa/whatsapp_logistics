import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import requests
from jinja2 import Template
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Teste Simplificado de Bibliotecas")

st.subheader("Streamlit")
st.write("Streamlit está funcionando!")
st.markdown("---")

st.subheader("Pandas")
try:
    df = pd.DataFrame({'col1': [1], 'col2': [2]})
    st.write("Pandas carregado. DataFrame:")
    st.dataframe(df)
except ImportError as e:
    st.error(f"Erro ao importar Pandas: {e}")
except Exception as e:
    st.error(f"Erro ao usar Pandas: {e}")
st.markdown("---")

st.subheader("SQLAlchemy")
try:
    engine = create_engine("sqlite:///:memory:")  # Conexão em memória para teste
    st.success("SQLAlchemy carregado e engine criado!")
except ImportError as e:
    st.error(f"Erro ao importar SQLAlchemy: {e}")
except Exception as e:
    st.error(f"Erro ao usar SQLAlchemy: {e}")
st.markdown("---")

# --- Teste python-dotenv ---
st.subheader("python-dotenv")
load_dotenv()
if os.getenv("TEST_VAR"):
    st.success(f"python-dotenv carregado. Variável 'TEST_VAR': {os.getenv('TEST_VAR')}")
else:
    st.info("python-dotenv carregado. Crie um arquivo '.env' com 'TEST_VAR=valor' para testar.")
st.markdown("---")

# --- Teste Requests ---
st.subheader("Requests")
try:
    response = requests.get("https://httpbin.org/status/200", timeout=5)
    response.raise_for_status()
    st.success(f"Requests carregado. Status da requisição: {response.status_code}")
except ImportError as e:
    st.error(f"Erro ao importar Requests: {e}")
except requests.exceptions.RequestException as e:
    st.warning(f"Erro ao fazer requisição com Requests: {e}")
st.markdown("---")

# --- Teste Jinja2 ---
st.subheader("Jinja2")
try:
    template = Template("Olá!")
    st.success(f"Jinja2 carregado. Template renderizado: {template.render()}")
except ImportError as e:
    st.error(f"Erro ao importar Jinja2: {e}")
except Exception as e:
    st.error(f"Erro ao usar Jinja2: {e}")
st.markdown("---")

# --- Teste Matplotlib ---
st.subheader("Matplotlib")
try:
    plt.plot([1, 2], [3, 4])
    st.pyplot(plt)
    st.success("Matplotlib carregado e gráfico básico exibido.")
except ImportError as e:
    st.error(f"Erro ao importar Matplotlib: {e}")
except Exception as e:
    st.warning(f"Erro ao usar Matplotlib.")
st.markdown("---")

# --- Teste Plotly ---
st.subheader("Plotly")
try:
    fig = px.scatter(x=[1], y=[2])
    st.plotly_chart(fig)
    st.success("Plotly carregado e gráfico básico exibido.")
except ImportError as e:
    st.error(f"Erro ao importar Plotly: {e}")
except Exception as e:
    st.warning(f"Erro ao usar Plotly.")