#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar a discrepância entre boletins importados e registros históricos
"""

import sqlite3
import sys
import os

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    os.system('chcp 65001 > nul')


def conectar_banco():
    """Conecta ao banco de dados"""
    try:
        db = sqlite3.connect('boletins.db')
        db.row_factory = sqlite3.Row
        return db
    except Exception as e:
        print(f"ERRO: Erro ao conectar ao banco: {e}")
        return None


def analisar_boletins():
    """Analisa os boletins na tabela principal"""
    print("DADOS: ANÁLISE DOS BOLETINS")
    print("=" * 50)

    db = conectar_banco()
    if not db:
        return

    # Total de boletins
    cursor = db.execute('SELECT COUNT(*) FROM boletins')
    total_boletins = cursor.fetchone()[0]
    print(f"DADOS: Total de boletins na tabela 'boletins': {total_boletins}")

    # Boletins por origem (se campo existir)
    try:
        cursor = db.execute('''
            SELECT COUNT(*) as total,
                   CASE
                       WHEN numero_boletim LIKE 'PTJ%' THEN 'Importados'
                       ELSE 'Manuais'
                   END as origem
            FROM boletins
            GROUP BY origem
        ''')

        origens = cursor.fetchall()
        for origem in origens:
            print(f"   • {origem['origem']}: {origem['total']} boletins")

    except Exception as e:
        print(f"   Não foi possível determinar origem: {e}")

    # Listar alguns boletins para verificar
    cursor = db.execute('''
        SELECT id, numero_boletim, data_coleta, data_validacao
        FROM boletins
        ORDER BY id
        LIMIT 10
    ''')

    boletins = cursor.fetchall()
    print(f"\nRELATORIO: Primeiros {len(boletins)} boletins:")
    for b in boletins:
        print(f"   ID: {b['id']} | Número: {b['numero_boletim']} | Coleta: {b['data_coleta']} | Validação: {b['data_validacao']}")

    if total_boletins > 10:
        print(f"   ... e mais {total_boletins - 10} boletins")

    db.close()


def analisar_historico():
    """Analisa a tabela historico_componentes"""
    print("\nDADOS: ANÁLISE DO HISTÓRICO DE COMPONENTES")
    print("=" * 50)

    db = conectar_banco()
    if not db:
        return

    # Total de registros históricos
    cursor = db.execute('SELECT COUNT(*) FROM historico_componentes')
    total_historico = cursor.fetchone()[0]
    print(f"DADOS: Total de registros na tabela 'historico_componentes': {total_historico}")

    # Registros por boletim
    cursor = db.execute('''
        SELECT boletin_id, COUNT(*) as componentes_por_boletim
        FROM historico_componentes
        GROUP BY boletin_id
        ORDER BY boletin_id
    ''')

    registros_por_boletim = cursor.fetchall()
    print(f"\nRELATORIO: Componentes por boletim (total: {len(registros_por_boletim)} boletins):")

    for i, registro in enumerate(registros_por_boletim):
        if i < 10:  # Mostrar apenas os primeiros 10
            print(f"   Boletim ID {registro['boletin_id']}: {registro['componentes_por_boletim']} componentes")
        elif i == 10:
            print(f"   ... e mais {len(registros_por_boletim) - 10} boletins")
            break

    # Verificar se todos os boletins têm a mesma quantidade de componentes
    cursor = db.execute('''
        SELECT componentes_por_boletim, COUNT(*) as quantidade_boletins
        FROM (
            SELECT boletin_id, COUNT(*) as componentes_por_boletim
            FROM historico_componentes
            GROUP BY boletin_id
        )
        GROUP BY componentes_por_boletim
    ''')

    distribuicao = cursor.fetchall()
    print("\nDADOS: Distribuição de componentes por boletim:")
    for dist in distribuicao:
        print(f"   • {dist['componentes_por_boletim']} componentes: {dist['quantidade_boletins']} boletins")

    # Componentes únicos
    cursor = db.execute('''
        SELECT DISTINCT componente
        FROM historico_componentes
        ORDER BY componente
    ''')

    componentes = cursor.fetchall()
    print(f"\nTESTE: Componentes únicos no histórico ({len(componentes)}):")
    for comp in componentes:
        print(f"   • {comp['componente']}")

    db.close()


def calcular_explicacao():
    """Calcula e explica a discrepância"""
    print("\nINFO: EXPLICAÇÃO DA DISCREPÂNCIA")
    print("=" * 50)

    db = conectar_banco()
    if not db:
        return

    # Contar boletins únicos no histórico
    cursor = db.execute('SELECT COUNT(DISTINCT boletin_id) FROM historico_componentes')
    boletins_com_historico = cursor.fetchone()[0]

    # Contar total de boletins
    cursor = db.execute('SELECT COUNT(*) FROM boletins')
    total_boletins = cursor.fetchone()[0]

    # Contar componentes médios por boletim
    cursor = db.execute('''
        SELECT AVG(componentes_por_boletim) as media_componentes
        FROM (
            SELECT boletin_id, COUNT(*) as componentes_por_boletim
            FROM historico_componentes
            GROUP BY boletin_id
        )
    ''')

    media_componentes = cursor.fetchone()[0]

    print("DADOS: NÚMEROS:")
    print(f"   • Total de boletins: {total_boletins}")
    print(f"   • Boletins com histórico: {boletins_com_historico}")
    print(f"   • Média de componentes por boletim: {media_componentes:.1f}")

    # Calcular expectativa
    total_registros_esperados = boletins_com_historico * media_componentes

    cursor = db.execute('SELECT COUNT(*) FROM historico_componentes')
    total_registros_reais = cursor.fetchone()[0]

    print("\nDADOS: CÁLCULO:")
    print(f"   • {boletins_com_historico} boletins × {media_componentes:.1f} componentes = {total_registros_esperados:.0f} registros esperados")
    print(f"   • Total real de registros: {total_registros_reais}")

    print("\nINFO: EXPLICAÇÃO:")
    if boletins_com_historico != total_boletins:
        print(f"   AVISO: Nem todos os boletins têm histórico! ({boletins_com_historico}/{total_boletins})")

    if total_registros_reais > boletins_com_historico:
        print("   OK: Cada boletim gera múltiplos registros históricos (um por componente)")
        print(f"   OK: {total_registros_reais} registros ÷ {boletins_com_historico} boletins = {total_registros_reais / boletins_com_historico:.1f} componentes por boletim")

    # Verificar origem dos dados
    cursor = db.execute('''
        SELECT b.numero_boletim,
               CASE
                   WHEN b.numero_boletim LIKE 'PTJ%' THEN 'Importado'
                   ELSE 'Manual'
               END as origem,
               COUNT(h.id) as registros_historico
        FROM boletins b
        LEFT JOIN historico_componentes h ON b.id = h.boletin_id
        GROUP BY b.id, origem
        ORDER BY b.id
    ''')

    origem_dados = cursor.fetchall()
    importados = sum(1 for x in origem_dados if x['origem'] == 'Importado')
    manuais = sum(1 for x in origem_dados if x['origem'] == 'Manual')

    print("\nDADOS: ORIGEM DOS DADOS:")
    print(f"   • Boletins importados: {importados}")
    print(f"   • Boletins manuais: {manuais}")
    print(f"   • Total: {importados + manuais}")

    db.close()


def verificar_processo_importacao():
    """Verifica como o processo de importação funciona"""
    print("\nINFO: PROCESSO DE IMPORTAÇÃO")
    print("=" * 50)

    print("""
INFO: COMO FUNCIONA:

1. IMPORTAÇÃO DE BOLETINS:
   • Excel contém múltiplos boletins históricos
   • Cada linha do Excel = 1 boletim completo
   • Sistema insere na tabela 'boletins'

2. CRIAÇÃO DO HISTÓRICO:
   • Para CADA boletim importado
   • Para CADA componente do boletim (15 componentes)
   • Sistema cria 1 registro na tabela 'historico_componentes'
   • Total = Boletins × 15 componentes

3. EXEMPLO:
   • 9 boletins importados
   • 15 componentes por boletim
   • 9 × 15 = 135 registros históricos MÍNIMO

   • Mas se houve mais boletins (manuais ou outros)
   • O histórico cresce proporcionalmente
""")


def main():
    """Função principal"""
    print("TESTE: ANÁLISE DE DISCREPÂNCIA - BOLETINS vs HISTÓRICO")
    print("=" * 60)

    analisar_boletins()
    analisar_historico()
    calcular_explicacao()
    verificar_processo_importacao()

    print("\n" + "=" * 60)
    print("OK: ANÁLISE CONCLUÍDA")
    print("=" * 60)


if __name__ == "__main__":
    main()
