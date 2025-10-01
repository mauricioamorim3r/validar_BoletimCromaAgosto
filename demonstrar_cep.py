#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para demonstrar como o cálculo do CEP é feito e como ele é mostrado ao usuário
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


def get_historico_componente(componente):
    """Busca histórico de valores para um componente específico"""
    db = conectar_banco()
    if not db:
        return []

    historico = db.execute('''
        SELECT valor FROM historico_componentes
        WHERE componente = ?
        ORDER BY data_coleta ASC
    ''', (componente,)).fetchall()

    db.close()
    return [row[0] for row in historico]


def calcular_limites_cep(componente, novo_valor=None):
    """
    Demonstra o cálculo completo dos limites CEP
    """
    print(f"\nTESTE: CÁLCULO CEP PARA: {componente}")
    print("=" * 60)

    # 1. Buscar histórico
    historico = get_historico_componente(componente)
    print(f"DADOS: Histórico disponível: {len(historico)} valores")

    if len(historico) < 2:
        print("AVISO: Histórico insuficiente para CEP")
        return True, None, None

    # 2. Usar últimas 8 amostras (ou todas se menos de 8)
    ultimas_amostras = historico[-8:] if len(historico) >= 8 else historico
    print(f"INFO: Usando últimas {len(ultimas_amostras)} amostras")
    print(f"   Valores: {[f'{v:.3f}%' for v in ultimas_amostras]}")

    # 3. Calcular média
    media = sum(ultimas_amostras) / len(ultimas_amostras)
    print(f"DADOS: Média (x̄): {media:.3f}%")

    # 4. Calcular amplitudes móveis (diferenças consecutivas)
    amplitudes = [abs(ultimas_amostras[i] - ultimas_amostras[i - 1])
                  for i in range(1, len(ultimas_amostras))]
    print(f"INFO: Amplitudes móveis: {[f'{a:.3f}' for a in amplitudes]}")

    # 5. Calcular média das amplitudes móveis
    media_amplitudes = sum(amplitudes) / len(amplitudes)
    print(f"DADOS: Média das amplitudes (MR̄): {media_amplitudes:.4f}")

    # 6. Aplicar fórmula CEP com constante d2
    d2 = 1.128  # Constante para amplitude móvel (n=2)
    print(f"INFO: Constante d2: {d2}")

    # 7. Calcular limites de controle (3 sigma)
    desvio = 3 * media_amplitudes / d2
    lcs = media + desvio  # Limite Superior de Controle
    lci = media - desvio  # Limite Inferior de Controle

    print("DADOS: Cálculo dos limites:")
    print(f"   LCS = x̄ + 3×MR̄/d2 = {media:.3f} + 3×{media_amplitudes:.4f}/{d2} = {lcs:.3f}%")
    print(f"   LCI = x̄ - 3×MR̄/d2 = {media:.3f} - 3×{media_amplitudes:.4f}/{d2} = {lci:.3f}%")

    # 8. Teste com novo valor (se fornecido)
    if novo_valor is not None:
        print(f"\nTESTE: TESTE COM NOVO VALOR: {novo_valor:.3f}%")
        validado = lci <= novo_valor <= lcs
        print(f"   Dentro dos limites? {lci:.3f}% ≤ {novo_valor:.3f}% ≤ {lcs:.3f}%")
        print(f"   STATUS CEP: {'OK: VALIDADO' if validado else 'ERRO: INVALIDADO'}")
        return validado, lci, lcs

    return True, lci, lcs


def demonstrar_exibicao_usuario():
    """
    Demonstra como o CEP é exibido ao usuário na interface
    """
    print("\n" + "=" * 60)
    print("INFO: EXIBIÇÃO PARA O USUÁRIO")
    print("=" * 60)

    print("""
RELATORIO: No Relatório de Validação, o usuário vê:

┌─────────────────────────────────────────────────────────────┐
│                   3) ANÁLISE CEP                            │
├─────────────┬────────┬─────────┬─────────────┬─────────────┤
│ Componente  │  Valor │   CEP   │ Lim. Inf.   │ Lim. Sup.   │
├─────────────┼────────┼─────────┼─────────────┼─────────────┤
│ Metano      │ 97.55% │ VALIDADO│    96.35%   │    99.15%   │
│ Etano       │  0.10% │ VALIDADO│     0.05%   │     0.16%   │
│ Propano     │  0.64% │ VALIDADO│    -0.51%   │     1.32%   │
│ CO2         │  0.79% │ VALIDADO│     0.69%   │     0.89%   │
└─────────────┴────────┴─────────┴─────────────┴─────────────┘

INFO: Código de Cores:
   OK: VALIDADO   = Verde (dentro dos limites CEP)
   ERRO: INVALIDADO = Vermelho (fora dos limites CEP)
""")

    print("""
INFO: Na Lista de Boletins (Dashboard), o usuário vê:

┌─────────────────────────────────────────────────────┐
│ Boletim │ Instalação    │ Status CEP  │ Status Geral│
├─────────┼───────────────┼─────────────┼─────────────┤
│ PTJ-001 │ PLATAFORMA A  │ OK: VALIDADO │ OK: VALIDADO │
│ PTJ-002 │ PLATAFORMA B  │ ERRO: INVALIDADO│ ERRO: INVALIDADO│
└─────────┴───────────────┴─────────────┴─────────────┘
""")


def analisar_componentes_problematicos():
    """
    Identifica componentes que frequentemente ficam fora dos limites CEP
    """
    print("\n" + "=" * 60)
    print("AVISO: ANÁLISE DE COMPONENTES PROBLEMÁTICOS")
    print("=" * 60)

    db = conectar_banco()
    if not db:
        return

    # Buscar componentes com status CEP invalidado
    componentes_problemas = db.execute('''
        SELECT nome as componente, COUNT(*) as total_invalidados,
               (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM componentes c2 WHERE c2.nome = c.nome)) as percentual
        FROM componentes c
        WHERE status_cep = 'INVALIDADO'
        GROUP BY nome
        ORDER BY total_invalidados DESC
    ''').fetchall()

    print("DADOS: Componentes com problemas de CEP:")
    for comp in componentes_problemas:
        print(f"   • {comp['componente']}: {comp['total_invalidados']} ocorrências ({comp['percentual']:.1f}%)")

    if not componentes_problemas:
        print("   OK: Nenhum componente com problemas de CEP detectado!")

    db.close()


def main():
    """Função principal para demonstração completa"""
    print("TESTE: DEMONSTRAÇÃO COMPLETA - CÁLCULO E EXIBIÇÃO CEP")
    print("=" * 60)

    # Verificar se estamos no diretório correto
    if not os.path.exists('boletins.db'):
        print("ERRO: Arquivo boletins.db não encontrado!")
        return False

    # Demonstrar cálculo para alguns componentes principais
    componentes_exemplo = ['Metano', 'Etano', 'Propano', 'CO2']

    for componente in componentes_exemplo:
        # Buscar último valor registrado como exemplo
        db = conectar_banco()
        if db:
            ultimo_registro = db.execute('''
                SELECT valor FROM historico_componentes
                WHERE componente = ?
                ORDER BY data_coleta DESC
                LIMIT 1
            ''', (componente,)).fetchone()

            if ultimo_registro:
                ultimo_valor = ultimo_registro[0]
                calcular_limites_cep(componente, ultimo_valor)
            else:
                calcular_limites_cep(componente)

            db.close()

    # Demonstrar como é exibido ao usuário
    demonstrar_exibicao_usuario()

    # Analisar componentes problemáticos
    analisar_componentes_problematicos()

    print("\n" + "=" * 60)
    print("OK: DEMONSTRAÇÃO CONCLUÍDA")
    print("=" * 60)

    return True


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
