# Configuração de Produção
# BRAVA ENERGIA - Sistema de Validação de Boletins Cromatográficos

# Configurações do servidor
DEBUG = False
HOST = '0.0.0.0'
PORT = 8080

# Configurações de segurança
SECRET_KEY = 'CHANGE_THIS_IN_PRODUCTION_FOR_SECURITY'

# Configurações do banco de dados
DATABASE_PATH = 'boletins.db'

# Configurações de upload
MAX_UPLOAD_SIZE = 16 * 1024 * 1024  # 16MB

# Configurações CEP
CEP_AMOSTRAS_MIN = 8
CEP_D2_CONSTANT = 1.128
CEP_SIGMA_LIMIT = 3

print("OK: Sistema configurado para produção")
print("AVISO:  LEMBRE-SE: Altere SECRET_KEY em produção!")
