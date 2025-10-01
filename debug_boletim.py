import sqlite3

# Verificar se há campos NULL que possam estar causando erro
conn = sqlite3.connect('boletins.db')
cursor = conn.cursor()

print("=== VERIFICAÇÃO DOS DADOS DO PRIMEIRO BOLETIM ===")
cursor.execute('SELECT * FROM boletins WHERE id = 1')
boletim = cursor.fetchone()

if boletim:
    # Pegar os nomes das colunas
    cursor.execute('PRAGMA table_info(boletins)')
    colunas = [coluna[1] for coluna in cursor.fetchall()]

    print("Dados do boletim ID 1:")
    for i, coluna in enumerate(colunas):
        valor = boletim[i] if boletim[i] is not None else "NULL"
        print(f"  {coluna}: {valor}")
else:
    print("Boletim não encontrado")

conn.close()
