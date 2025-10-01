import sqlite3

# Conectar ao banco
conn = sqlite3.connect('boletins.db')
cursor = conn.cursor()

# Executar a mesma query que está no app.py agora
cursor.execute('''
    SELECT b.id, b.numero_boletim, b.identificacao_instalacao, b.data_coleta, b.data_emissao, b.data_validacao, b.status
    FROM boletins b
    ORDER BY b.data_coleta DESC
''')

print("=== TESTE DA QUERY CORRIGIDA ===")
print("Primeiros 5 registros:")
print("ID | Boletim | Instalação | Data Coleta | Data Emissão | Data Validação | Status")
print("-" * 100)

registros = cursor.fetchall()
for i, reg in enumerate(registros[:5]):
    print(f"{reg[0]} | {reg[1]} | {reg[2]} | {reg[3]} | {reg[4]} | {reg[5]} | {reg[6]}")

print(f"\nTotal de registros retornados: {len(registros)}")

conn.close()
