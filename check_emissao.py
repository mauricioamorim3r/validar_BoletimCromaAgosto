# -*- coding: utf-8 -*-
import sqlite3
import sys
import os

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    os.system('chcp 65001 > nul')

db = sqlite3.connect('boletins.db')
cursor = db.execute('SELECT numero_boletim, data_coleta, data_emissao, data_validacao FROM boletins LIMIT 5')
print('DADOS: SAMPLE DE DATAS DOS BOLETINS:')
rows = cursor.fetchall()
for row in rows:
    emissao = row[2] if row[2] else "-"
    validacao = row[3] if row[3] else "-"
    print(f'   {row[0]} | {row[1]} | {emissao} | {validacao}')

cursor = db.execute("SELECT COUNT(*) FROM boletins WHERE data_emissao IS NOT NULL AND data_emissao != ''")
com_emissao = cursor.fetchone()[0]
cursor = db.execute('SELECT COUNT(*) FROM boletins')
total = cursor.fetchone()[0]

print('\nDADOS: ESTATÍSTICAS:')
print(f'   • Com data emissão: {com_emissao}/{total}')
print(f'   • Sem data emissão: {total - com_emissao}/{total}')

db.close()
