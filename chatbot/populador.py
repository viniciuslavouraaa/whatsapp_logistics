from faker import Faker
import random
from database import salvar_empresa, salvar_motorista
from datetime import date, timedelta
fake = Faker('pt_BR')

estados= [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG',
    'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]
tipos_carga= [
    'barrilha', 'apara de papel','cimento','telha','bobina de ferro','piso','sucata',
    'grãos (soja, milho, etc.)','farelo','adubo','calcário','madeira (toras, serrada, etc.)',
    'pallets','embalagens','produtos alimentícios (secos, refrigerados, congelados)',
    'bebidas (engarrafadas, enlatadas)','produtos de higiene e limpeza','medicamentos',
    'cosméticos','componentes eletrônicos','eletrodomésticos','móveis','máquinas e equipamentos',
    'veículos (novos, usados)','contêineres','carga viva (animais)','produtos químicos (embalados, a granel)',
    'gases industriais','minérios (ferro, alumínio, etc.)','asfalto','combustíveis','mudanças '
]
implementos= [
    'lona','corda','cinta','nenhum','cantoneiras','paletes','forro','pro chão (proteção para o assoalho)',
    'gancho','tapete de borracha','catraca','corrente','moitão','barra de contenção','rede de proteção','plástico bolha',
    'fitas adesivas','adesivos de segurança','cones de sinalização','calços de segurança','extintor de incêndio (verificar validade)',
    'kit de primeiros socorros','cabo de aço','macaquinho hidráulico','chave de roda','triângulo de sinalização',
]
tipos_caminhao= [
    "Caminhão 3/4 ou VUC (Veículo Urbano de Carga)","Caminhão toco (eixo simples na traseira)","Caminhão truck (dois eixos na traseira)",
    "Cavalo mecânico simples (uma tração)","Cavalo mecânico trucado (duas trações)","Carreta 2 eixos","Carreta 3 eixos","Bitrem (cavalo mecânico + 2 semirreboques)",
    "Treminhão (cavalo mecânico + 3 semirreboques)","Rodotrem (cavalo mecânico + 2 semirreboques interligados por Dolly)","Caminhão comboio (tanque com carroceria)",
    "Caminhão basculante","Caminhão-tanque","Prancha (para cargas indivisíveis)","Munck (com guindaste)","Sider (carroceria com cortinas laterais)","Baú (carroceria fechada)",
    "Graneleiro (para cargas a granel)","Florestal (para transporte de toras)","Boieiro (para transporte de animais)","Cegonha (para transporte de veículos)",
    "Plataforma (para diversos tipos de carga)"
]
tipos_carroceria= [
    "Baú (fechada, para cargas secas e protegidas)","Sider (laterais de lona, flexível para carga e descarga lateral)","Grade alta (laterais gradeadas, para cargas como toras, cana)",
    "Grade baixa (laterais baixas, para diversos tipos de carga)","Aberta (plataforma, sem laterais ou com laterais removíveis)","Caçamba (para transporte de materiais a granel, como areia, pedra)",
    "Tanque (para líquidos, gases)","Frigorífica (refrigerada ou congelada, para produtos perecíveis)","Basculante (carga e descarga por tombamento)","Boadeira (para transporte de gado)",
    "Florestal (específica para transporte de toras de madeira)","Cegonha (para transporte de veículos)","Munck (com guindaste para carga e descarga)","Poliguindaste (para transporte de caçambas)",
    "Prancha (para cargas indivisíveis e equipamentos pesados)","Porta-contêiner (para transporte de contêineres)","Carroceria para bebidas (estruturada para garrafas e engradados)","Carroceria para gás (específica para cilindros de gás)"
]
formas_pagamento= ['Pix', 'Cartão', 'Dinheiro']
tipos_conta= ['Conta Corrente', 'Conta Poupança']

# Popular empresas
for _ in range(50):
    salvar_empresa(
        nome_empresa=fake.company(),
        cnpj_empresa=fake.cnpj(),
        telefone_empresa=fake.phone_number(),
        cidade_origem=fake.city(),
        estado_origem=random.choice(estados),
        cidade_destino=fake.city(),
        estado_destino=random.choice(estados),
        tipo_carga=random.choice(tipos_carga),
        valor_frete=round(random.uniform(500, 3000), 2),
        frete=random.choice(['Sim', 'Não']),
        forma_pagamento=random.choice(formas_pagamento),
        data_carregamento=date.today(),
        data_descarregamento=date.today() + timedelta(days=random.randint(1, 7)),
        implemento=random.choice(implementos),
        foto_caminhao=random.choice(['Sim', 'Não']),
        tipo_caminhao=random.choice(tipos_caminhao),
        tipo_carroceria=random.choice(tipos_carroceria),
        tamanho_carroceria=round(random.uniform(6.0, 15.0), 2)
    )

# Popular motoristas

for _ in range(50):
    salvar_motorista(
        nome_caminhoneiro=fake.name(),
        cpf_caminhoneiro= fake.cpf(),
        rg_caminhoneiro=fake.rg(),
        telefone_caminhoneiro=fake.phone_number(),
        nome_banco=fake.company(),
        agencia=fake.bban(),
        conta=fake.bban(),
        tipo_conta=random.choice(tipos_conta),
        chave_pix=random.choice([fake.email(), fake.phone_number()]),
        antt=random.choice(['Sim', 'Não']),
        fretebras=random.choice(['Sim', 'Não']),
        motorista_empresa=random.choice(['Sim', 'Não']),
        nome_empresa=fake.company(),
        cnpj_empresa=fake.cnpj(),
        telefone_empresa=fake.phone_number()
    )
    
print("Base populada com sucesso!")