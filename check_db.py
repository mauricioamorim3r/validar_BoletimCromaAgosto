import sqlite3


def check_database():
    conn = sqlite3.connect('boletins.db')
    cursor = conn.cursor()

    # Verificar quantos boletins existem
    cursor.execute('SELECT COUNT(*) FROM boletins')
    total = cursor.fetchone()[0]
    print(f'Total de boletins: {total}')

    # Ver primeiros 5 boletins
    cursor.execute('SELECT numero_boletim, data_coleta, numero_documento, plataforma FROM boletins LIMIT 5')
    print('\nPrimeiros 5 boletins:')
    for row in cursor.fetchall():
        print(f'Boletim: {row[0]}, Data: {row[1]}, Doc: {row[2]}, Plataforma: {row[3]}')

    # Verificar estrutura da tabela
    cursor.execute('PRAGMA table_info(boletins)')
    print('\nCampos da tabela boletins:')
    for col in cursor.fetchall():
        print(f'  {col[1]} ({col[2]})')

    # Verificar alguns campos específicos
    cursor.execute(
        'SELECT numero_boletim, identificacao_instalacao, agente_regulado FROM boletins WHERE numero_boletim = "PTJ/24-14803"')
    resultado = cursor.fetchone()
    if resultado:
        print('\nBoletim PTJ/24-14803:')
        print(f'  Identificação Instalação: {resultado[1]}')
        print(f'  Agente Regulado: {resultado[2]}')

    conn.close()


if __name__ == '__main__':
    check_database()
