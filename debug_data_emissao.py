import sqlite3

# Conectar ao banco
conn = sqlite3.connect('boletins.db')
cursor = conn.cursor()

# Verificar estrutura da tabela boletins
print('=== ESTRUTURA DA TABELA BOLETINS ===')
cursor.execute('PRAGMA table_info(boletins)')
colunas = cursor.fetchall()
for coluna in colunas:
    print(f'{coluna[1]} - {coluna[2]} - Not Null: {coluna[3]} - Default: {coluna[4]}')

print('\n=== PRIMEIROS 5 REGISTROS COM data_emissao ===')
cursor.execute('SELECT id, numero_boletim, data_coleta, data_validacao, data_emissao FROM boletins LIMIT 5')
registros = cursor.fetchall()
for reg in registros:
    print(f'ID: {reg[0]} | Boletim: {reg[1]} | Coleta: {reg[2]} | Validação: {reg[3]} | Emissão: {reg[4]}')

print('\n=== CONTAGEM DE REGISTROS ===')
cursor.execute('SELECT COUNT(*) FROM boletins WHERE data_emissao IS NOT NULL AND data_emissao != ""')
count_preenchidos = cursor.fetchone()[0]
print(f'Registros com data_emissao preenchida: {count_preenchidos}')

cursor.execute('SELECT COUNT(*) FROM boletins WHERE data_emissao IS NULL OR data_emissao = ""')
count_vazios = cursor.fetchone()[0]
print(f'Registros com data_emissao vazia: {count_vazios}')

print('\n=== TODOS OS REGISTROS COM data_emissao ===')
cursor.execute('SELECT id, numero_boletim, data_emissao FROM boletins ORDER BY id')
todos_registros = cursor.fetchall()
for reg in todos_registros:
    print(f'ID: {reg[0]} | Boletim: {reg[1]} | Emissão: "{reg[2]}"')

conn.close()
