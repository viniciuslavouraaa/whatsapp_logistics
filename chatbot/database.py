from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker

BaseEmpresa = declarative_base()
engine_empresa = create_engine('sqlite:///database/empresa.db')
SessionEmpresa = sessionmaker(bind=engine_empresa)
session_empresa = SessionEmpresa()

class Empresa(BaseEmpresa):
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
    foto_caminhao = Column(String)
    tipo_caminhao = Column(String)
    tipo_carroceria = Column(String)
    tamanho_carroceria = Column(Float)

BaseEmpresa.metadata.create_all(engine_empresa)

BaseMotorista = declarative_base()
engine_motorista = create_engine('sqlite:///database/motorista.db')
SessionMotorista = sessionmaker(bind=engine_motorista)
session_motorista = SessionMotorista()

class Motorista(BaseMotorista):
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

BaseMotorista.metadata.create_all(engine_motorista)

# Funções de salvamento
def salvar_empresa(**dados):
    nova = Empresa(**dados)
    session_empresa.add(nova)
    session_empresa.commit()

def salvar_motorista(**dados):
    novo = Motorista(**dados)
    session_motorista.add(novo)
    session_motorista.commit()
