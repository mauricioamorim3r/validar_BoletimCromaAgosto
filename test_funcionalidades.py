# -*- coding: utf-8 -*-
import sqlite3
import requests
import sys
import os

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    os.system('chcp 65001 > nul')

# Teste para verificar se as funcionalidades estão funcionando

print("=== TESTE DAS FUNCIONALIDADES DE EDITAR/EXCLUIR ===")

# Verificar se o servidor está rodando
try:
    response = requests.get('http://localhost:3000/boletins')
    print(f"OK: Servidor rodando - Status: {response.status_code}")
    if response.status_code == 200:
        print("OK: Página dos boletins carregando corretamente")
    else:
        print(f"ERRO: Problema na página dos boletins: {response.status_code}")
except Exception as e:
    print(f"ERRO: Servidor não está rodando ou não acessível: {e}")

# Verificar estrutura do banco para confirmar IDs disponíveis
conn = sqlite3.connect('boletins.db')
cursor = conn.cursor()

cursor.execute('SELECT id, numero_boletim FROM boletins LIMIT 3')
boletins = cursor.fetchall()

print("\n=== BOLETINS DISPONÍVEIS PARA TESTE ===")
for boletim in boletins:
    print(f"ID: {boletim[0]} - Boletim: {boletim[1]}")

    # Testar se a rota de edição responde
    try:
        url_edit = f'http://localhost:3000/editar/{boletim[0]}'
        response = requests.get(url_edit)
        if response.status_code == 200:
            print(f"  OK: Rota de edição funcionando: {url_edit}")
        else:
            print(f"  ERRO: Problema na rota de edição: {response.status_code}")
    except Exception as e:
        print(f"  ERRO: Erro ao testar edição: {e}")

conn.close()
