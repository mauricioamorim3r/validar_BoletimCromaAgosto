# Configurações do Sistema de Validação de Boletins Cromatográficos
# BRAVA Energia - Campo de Atalaia

# Configurações do Servidor
HOST = '127.0.0.1'
PORT = 3000
DEBUG = True

# Configurações da Empresa
EMPRESA_NOME = 'BRAVA ENERGIA'
CAMPO = 'Campo de Atalaia'
SETOR = 'Controle de Qualidade'

# Limites A.G.A #8 (em percentual molar)
LIMITES_AGA8 = {
    'Metano': {'min': 0, 'max': 100},
    'Etano': {'min': 0, 'max': 100},
    'Propano': {'min': 0, 'max': 12},
    'i-Butano': {'min': 0, 'max': 6},
    'n-Butano': {'min': 0, 'max': 6},
    'i-Pentano': {'min': 0, 'max': 4},
    'n-Pentano': {'min': 0, 'max': 4},
    'Hexano': {'min': 0, 'max': 100},
    'Heptano': {'min': 0, 'max': 100},
    'Octano': {'min': 0, 'max': 100},
    'Nonano': {'min': 0, 'max': 100},
    'Decano': {'min': 0, 'max': 100},
    'Oxigênio': {'min': 0, 'max': 21},
    'Nitrogênio': {'min': 0, 'max': 100},
    'CO2': {'min': 0, 'max': 100}
}

# Massas Molares (g/mol)
MASSAS_MOLARES = {
    'Metano': 16.043,
    'Etano': 30.070,
    'Propano': 44.097,
    'i-Butano': 58.123,
    'n-Butano': 58.123,
    'i-Pentano': 72.150,
    'n-Pentano': 72.150,
    'Hexano': 86.177,
    'Heptano': 100.204,
    'Octano': 114.231,
    'Nonano': 128.258,
    'Decano': 142.285,
    'Oxigênio': 31.998,
    'Nitrogênio': 28.014,
    'CO2': 44.010
}

# Configurações CEP
CEP_AMOSTRAS_MIN = 8  # Mínimo de amostras para CEP
CEP_D2_CONSTANT = 1.128  # Constante d2 para amplitude móvel (n=2)
CEP_SIGMA_LIMIT = 3  # Limites de controle em sigma

# Configurações de Cálculo de Propriedades
# Condições padrão para cálculo da massa específica
TEMPERATURA_PADRAO = 293.15  # K (20°C)
PRESSAO_PADRAO = 101325  # Pa (1 atm)
CONSTANTE_R = 8314.47  # J/(kmol·K)

# Configurações do PDF
PDF_AUTHOR = 'BRAVA Energia - Sistema Automatizado'
PDF_TITLE_PREFIX = 'Relatório de Validação Cromatográfica'
PDF_MARGIN = 50  # pontos

# Configurações do Dashboard
DASHBOARD_BOLETINS_RECENTES = 10
DASHBOARD_COMPONENTES_PROBLEMAS = 10
DASHBOARD_HISTORICO_GRAFICO = 50

# Componentes principais para gráfico de tendências
COMPONENTES_PRINCIPAIS = ['Metano', 'Etano', 'Propano', 'Nitrogênio', 'CO2']

# Tolerância para soma de percentuais (±%)
TOLERANCIA_SOMA_PERCENTUAL = 2.0