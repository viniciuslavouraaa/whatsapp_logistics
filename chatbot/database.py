# database.py

from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///banco_cargas.db')
Session = sessionmaker(bind=engine)
session = Session()

class Empresa(Base):
    __tablename__ = 'empresas'
    id = Column(Integer, primary_key=True)
    nome_empresa = Column(String)
    cnpj_empresa = Column(String)
    telefone_empresa = Column(String)
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
    tipo_caminhao = Column(String)
    tipo_carroceria = Column(String)
    tamanho_carroceria = Column(Float)

class Motorista(Base):
    __tablename__ = 'motoristas'
    id = Column(Integer, primary_key=True)
    nome_caminhoneiro = Column(String)
    cpf_caminhoneiro = Column(String)
    rg_caminhoneiro = Column(String)
    telefone_caminhoneiro = Column(String)
    nome_banco = Column(String)
    agencia = Column(String)
    conta = Column(String)
    tipo_conta = Column(String)
    chave_pix = Column(String)
    antt = Column(String)
    fretebras = Column(String)
    motorista_empresa = Column(String)
    nome_empresa = Column(String)
    cnpj_empresa = Column(String)
    telefone_empresa = Column(String)

Base.metadata.create_all(engine)

def salvar_empresa(**dados):
    nova = Empresa(**dados)
    session.add(nova)
    session.commit()

def salvar_motorista(**dados):
    novo = Motorista(**dados)
    session.add(novo)
    session.commit()
