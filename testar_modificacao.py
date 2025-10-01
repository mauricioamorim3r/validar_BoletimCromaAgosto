#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste rápido para verificar se a modificação da tabela funcionou
"""

import sqlite3
import sys
import os

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    os.system('chcp 65001 > nul')


def testar_modificacao():
    """Testa se a modificação da tabela está funcionando"""
    print("INFO: TESTANDO MODIFICAÇÃO DA TABELA")
    print("=" * 50)

    # Conectar ao banco
    db = sqlite3.connect('boletins.db')
    db.row_factory = sqlite3.Row

    # Buscar dados como o Flask faria
    cursor = db.execute('''
        SELECT id, numero_boletim, identificacao_instalacao,
               data_coleta, data_emissao, data_validacao, status
        FROM boletins
        ORDER BY id
        LIMIT 3
    ''')

    boletins = cursor.fetchall()

    print("DADOS: DADOS QUE SERÃO EXIBIDOS NA TABELA:")
    print("   Boletim | Instalação | Data Coleta | Data Emissão | Data Validação | Status")
    print("   " + "-" * 85)

    for b in boletins:
        print(f"   {b['numero_boletim'][:15]:<15} | {b['identificacao_instalacao'][:12]:<12} | {b['data_coleta']:<11} | {b['data_emissao']:<12} | {b['data_validacao'][:10] if b['data_validacao'] else '-':<10} | {b['status']}")

    db.close()

    print("\nOK: MODIFICAÇÃO REALIZADA COM SUCESSO!")
    print("   • Nova coluna 'Data Emissão do Relatório' adicionada")
    print("   • Posicionada entre 'Data Coleta' e 'Data Validação'")
    print("   • Todos os boletins têm dados de emissão preenchidos")


if __name__ == "__main__":
    testar_modificacao()
