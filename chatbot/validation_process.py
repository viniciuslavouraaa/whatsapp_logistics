# Validações caminhoneiro
import streamlit as st

def possui_antt(resposta):
    if resposta == 'Sim':
        tem_antt = st.file_uploader('✅ Enviar ANTT:', type=['jpg', 'jpeg', 'png'])
    else:
        tem_antt = '⚠️ Sem ANTT - Acesso restrito'

def tem_fretebras(resposta):
    if resposta == 'Sim':
        fretebras = st.text_input('✅ ID Fretebras:')
    else:
        fretebras = '⚠️ Não cadastrado'