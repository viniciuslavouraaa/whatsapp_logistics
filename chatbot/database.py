from sqlalchemy import create_engine, Column, Integer, String,Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd 

Base = declarative_base()
engine = create_engine('sqlite:///banco_lavoura_transportes.db') # Caminho do banco de dados
Session = sessionmaker(bind=engine)
session =Session()

class Empresa(Base):
    __tablename__ = 'empresas'
    id = Column(Integer, primary_key=True)
    nome_empresa = Column(String)
    cidade_origem = Column(String)
    estado_origem = Column(String)
    cidade_destino = Column(String)
    estado_destino = Column(String)
    tipo_carga = Column(String)
    valor_frete = Column(Float)
    frete = Column(String)
    forma_pagamento = Column(String)
    data_carregamento = Column(Date)
    data_descarregamento = Column(Date)
    implemento = Column(String)
    foto_caminhao = Column(String)
    tipo_caminhao = Column(String)
    tipo_carroceria = Column(String)
    tamanho_carroceria = Column(Float)
    
# Cria as tabelas se não existirem
Base.metadata.create_all(engine)

# Função para salvar a empresa no banco de dados
def salvar_empresa(**dados):
    nova_empresa = Empresa(**dados)
    session.add(nova_empresa)
    session.commit()
    
# Função para carregar os dados da empresa por nome
def carregar_empresa_por_nome(nome):
    query = f"SELECT * FROM empresas WHERE nome_empresa = '{nome}'"
    df = pd.read_sql(query, engine)
    return df

class Caminhoneiro(Base):
    __tablename__ = 'Caminhoneiros'
    id = Column(Integer, primary_key=True)
    nome_caminhoneiro = Column(String)
    # foto cnh
    cpf_caminhoneiro = Column(String)
    rg_caminhoneiro = Column(String)
    nome_banco = Column(String)
    agencia = Column(String)
    conta = Column(String)
    tipo_conta = Column(String)
    chave_pix = Column(String)
    # doc caminhao
    # antt
    fretebras = Column(String)