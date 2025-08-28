import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('boletins.db')
cursor = conn.cursor()

# Verificar total de boletins
cursor.execute('SELECT COUNT(*) FROM boletins')
total_boletins = cursor.fetchone()[0]
print(f'Total de boletins: {total_boletins}')

# Ver alguns exemplos
cursor.execute('SELECT numero_boletim, data_coleta, status FROM boletins ORDER BY data_coleta DESC LIMIT 5')
result = cursor.fetchall()
print('\nPrimeiros 5 boletins mais recentes:')
for row in result:
    print(f'  Boletim: {row[0]} - Data: {row[1]} - Status: {row[2]}')

# Verificar histórico de componentes
cursor.execute('SELECT COUNT(*) FROM historico_componentes')
total_historico = cursor.fetchone()[0]
print(f'\nTotal de registros no histórico: {total_historico}')

# Ver alguns componentes
cursor.execute('SELECT componente, COUNT(*) as quantidade FROM historico_componentes GROUP BY componente LIMIT 5')
componentes = cursor.fetchall()
print('\nComponentes no histórico:')
for comp in componentes:
    print(f'  {comp[0]}: {comp[1]} registros')

conn.close()
