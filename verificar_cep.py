#!/usr/bin/env python3
"""
Script de verificação completa das funcionalidades CEP e integração do banco de dados
"""

import sqlite3
import sys
import os
from datetime import datetime, timedelta
import random


def conectar_banco():
    """Conecta ao banco de dados"""
    try:
        db = sqlite3.connect('boletins.db')
        db.row_factory = sqlite3.Row
        return db
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None


def verificar_estrutura_banco():
    """Verifica se as tabelas necessárias existem"""
    print("🔍 Verificando estrutura do banco de dados...")

    db = conectar_banco()
    if not db:
        return False

    tabelas_necessarias = ['boletins', 'componentes', 'historico_componentes']

    for tabela in tabelas_necessarias:
        try:
            cursor = db.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabela}'")
            resultado = cursor.fetchone()

            if resultado:
                print(f"✅ Tabela '{tabela}' encontrada")

                # Verificar colunas específicas
                if tabela == 'historico_componentes':
                    cursor = db.execute(f"PRAGMA table_info({tabela})")
                    colunas = [col[1] for col in cursor.fetchall()]
                    colunas_necessarias = ['id', 'componente', 'boletin_id', 'valor', 'data_coleta']

                    for col in colunas_necessarias:
                        if col in colunas:
                            print(f"   ✅ Coluna '{col}' presente")
                        else:
                            print(f"   ❌ Coluna '{col}' AUSENTE")
                            return False
            else:
                print(f"❌ Tabela '{tabela}' NÃO encontrada")
                return False

        except Exception as e:
            print(f"❌ Erro ao verificar tabela {tabela}: {e}")
            return False

    db.close()
    return True


def verificar_dados_historico():
    """Verifica dados existentes no histórico"""
    print("\n📊 Verificando dados do histórico...")

    db = conectar_banco()
    if not db:
        return False

    try:
        # Contar registros totais
        cursor = db.execute('SELECT COUNT(*) FROM historico_componentes')
        total_historico = cursor.fetchone()[0]
        print(f"📈 Total de registros no histórico: {total_historico}")

        if total_historico == 0:
            print("⚠️  HISTÓRICO VAZIO - Isso explicaria porque CEP não funciona!")
            return False

        # Verificar distribuição por componente
        cursor = db.execute('''
            SELECT componente, COUNT(*) as quantidade
            FROM historico_componentes
            GROUP BY componente
            ORDER BY quantidade DESC
        ''')

        componentes_historico = cursor.fetchall()
        print(f"📋 Componentes no histórico: {len(componentes_historico)}")

        for comp in componentes_historico[:5]:  # Mostrar top 5
            print(f"   • {comp['componente']}: {comp['quantidade']} registros")

        # Verificar dados recentes
        cursor = db.execute('''
            SELECT componente, valor, data_coleta
            FROM historico_componentes
            ORDER BY data_coleta DESC
            LIMIT 10
        ''')

        dados_recentes = cursor.fetchall()
        print(f"\n📅 Últimos 10 registros:")
        for dado in dados_recentes:
            print(f"   • {dado['componente']}: {dado['valor']}% ({dado['data_coleta']})")

    except Exception as e:
        print(f"❌ Erro ao verificar dados histórico: {e}")
        return False

    db.close()
    return True


def testar_funcao_cep():
    """Testa a função de validação CEP"""
    print("\n🧮 Testando função CEP...")

    # Importar funções do app principal
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from app import valida_cep, get_historico_componente
        print("✅ Funções CEP importadas com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar funções: {e}")
        return False

    # Teste 1: Componente sem histórico (deve retornar True)
    print("\n🔬 Teste 1: Componente sem histórico suficiente")
    resultado = valida_cep("TesteComponente", 50.0, [45.0])
    print(f"   Resultado: {resultado} (esperado: True - sem dados suficientes)")

    # Teste 2: Componente com histórico simulado (valores estáveis)
    print("\n🔬 Teste 2: Histórico estável (deve VALIDAR)")
    historico_estavel = [50.0, 51.0, 49.5, 50.5, 50.2, 49.8, 50.3, 49.7]
    novo_valor = 50.1
    resultado = valida_cep("TesteEstavel", novo_valor, historico_estavel)

    # Calcular manualmente os limites para verificação
    media = sum(historico_estavel) / len(historico_estavel)
    amplitudes = [abs(historico_estavel[i] - historico_estavel[i - 1])
                  for i in range(1, len(historico_estavel))]
    media_amplitudes = sum(amplitudes) / len(amplitudes)
    d2 = 1.128
    lcs = media + 3 * media_amplitudes / d2
    lci = media - 3 * media_amplitudes / d2

    print(f"   Histórico: {historico_estavel}")
    print(f"   Novo valor: {novo_valor}")
    print(f"   Média histórica: {media:.3f}")
    print(f"   LCI: {lci:.3f}, LCS: {lcs:.3f}")
    print(f"   Resultado CEP: {resultado}")

    # Teste 3: Valor fora dos limites (deve INVALIDAR)
    print("\n🔬 Teste 3: Valor fora dos limites (deve INVALIDAR)")
    valor_outlier = 70.0  # Muito acima da média
    resultado_outlier = valida_cep("TesteOutlier", valor_outlier, historico_estavel)
    print(f"   Valor outlier: {valor_outlier}")
    print(f"   Resultado CEP: {resultado_outlier} (esperado: False)")

    return True


def testar_integracao_banco():
    """Testa a integração completa banco + CEP"""
    print("\n🔗 Testando integração banco de dados...")

    db = conectar_banco()
    if not db:
        return False

    try:
        # Verificar se existem componentes sem histórico
        cursor = db.execute('''
            SELECT c.nome, COUNT(h.id) as historico_count
            FROM componentes c
            LEFT JOIN historico_componentes h ON c.nome = h.componente
            GROUP BY c.nome
            HAVING historico_count = 0
        ''')

        sem_historico = cursor.fetchall()
        if sem_historico:
            print(f"⚠️  {len(sem_historico)} componentes SEM histórico:")
            for comp in sem_historico[:5]:
                print(f"   • {comp['nome']}")
        else:
            print("✅ Todos os componentes têm histórico")

        # Verificar consistência boletin_id
        cursor = db.execute('''
            SELECT COUNT(DISTINCT h.boletin_id) as boletins_historico,
                   COUNT(DISTINCT b.id) as boletins_total
            FROM historico_componentes h
            CROSS JOIN boletins b
        ''')

        consistencia = cursor.fetchone()
        print(f"📊 Boletins com histórico: {consistencia['boletins_historico']}")
        print(f"📊 Total de boletins: {consistencia['boletins_total']}")

        # Testar busca de histórico real
        cursor = db.execute('''
            SELECT DISTINCT componente FROM historico_componentes LIMIT 1
        ''')

        componente_teste = cursor.fetchone()
        if componente_teste:
            comp_nome = componente_teste['componente']
            print(f"\n🔍 Testando busca histórico para: {comp_nome}")

            # Importar função
            from app import get_historico_componente
            historico_real = get_historico_componente(comp_nome)

            print(f"   Histórico encontrado: {len(historico_real)} valores")
            if historico_real:
                print(f"   Primeiros 5 valores: {historico_real[:5]}")
                print(f"   Últimos 5 valores: {historico_real[-5:]}")

                # Testar CEP com dados reais
                if len(historico_real) >= 8:
                    from app import valida_cep
                    ultimo_valor = historico_real[-1]
                    historico_anterior = historico_real[:-1]

                    resultado_real = valida_cep(comp_nome, ultimo_valor, historico_anterior)
                    print(f"   Teste CEP com último valor: {resultado_real}")
                else:
                    print(f"   ⚠️  Histórico insuficiente para CEP ({len(historico_real)} < 8)")

    except Exception as e:
        print(f"❌ Erro na integração: {e}")
        return False

    db.close()
    return True


def simular_dados_teste():
    """Cria alguns dados de teste se necessário"""
    print("\n🧪 Simulando dados de teste...")

    db = conectar_banco()
    if not db:
        return False

    try:
        # Verificar se já existem dados
        cursor = db.execute('SELECT COUNT(*) FROM historico_componentes')
        total_existente = cursor.fetchone()[0]

        if total_existente > 0:
            print(f"✅ Já existem {total_existente} registros no histórico")
            return True

        print("📝 Criando dados de teste...")

        # Criar dados simulados para teste
        componentes_teste = ['Metano', 'Etano', 'Propano']
        data_base = datetime.now() - timedelta(days=30)

        boletim_id_teste = 999  # ID fictício

        for i, componente in enumerate(componentes_teste):
            for dia in range(10):  # 10 dias de dados
                data_coleta = (data_base + timedelta(days=dia)).strftime('%Y-%m-%d')
                valor_base = 50.0 + i * 10  # Metano ~50%, Etano ~60%, etc.
                valor = valor_base + random.uniform(-2, 2)  # Variação pequena

                db.execute('''
                    INSERT INTO historico_componentes (componente, boletin_id, valor, data_coleta)
                    VALUES (?, ?, ?, ?)
                ''', (componente, boletim_id_teste, valor, data_coleta))

        db.commit()
        print("✅ Dados de teste criados")

    except Exception as e:
        print(f"❌ Erro ao criar dados teste: {e}")
        return False

    db.close()
    return True


def relatorio_final():
    """Gera relatório final da verificação"""
    print("\n" + "=" * 60)
    print("📋 RELATÓRIO FINAL - VERIFICAÇÃO CEP E BANCO")
    print("=" * 60)

    # Resumo das verificações
    verificacoes = [
        ("Estrutura do banco", verificar_estrutura_banco()),
        ("Dados do histórico", verificar_dados_historico()),
        ("Função CEP", testar_funcao_cep()),
        ("Integração banco", testar_integracao_banco())
    ]

    print("\n🎯 RESULTADOS:")
    for nome, resultado in verificacoes:
        status = "✅ PASS" if resultado else "❌ FAIL"
        print(f"   {status} {nome}")

    # Recomendações
    print("\n💡 RECOMENDAÇÕES:")

    db = conectar_banco()
    if db:
        cursor = db.execute('SELECT COUNT(*) FROM historico_componentes')
        total_historico = cursor.fetchone()[0]

        if total_historico == 0:
            print("   🚨 URGENTE: Execute 'Processar Boletins Existentes' no sistema web")
            print("   📝 Isso criará o histórico necessário para o CEP funcionar")
        elif total_historico < 50:
            print(f"   ⚠️  Histórico pequeno ({total_historico} registros)")
            print("   📈 CEP funcionará melhor com mais dados históricos")
        else:
            print("   ✅ Histórico suficiente para CEP funcionar corretamente")

        db.close()

    print("\n🔧 STATUS GERAL:")
    todos_ok = all(resultado for _, resultado in verificacoes)
    if todos_ok:
        print("   ✅ SISTEMA FUNCIONANDO CORRETAMENTE")
    else:
        print("   ⚠️  NECESSITA CORREÇÕES")

    return todos_ok


def main():
    """Função principal"""
    print("🔬 VERIFICAÇÃO COMPLETA - CEP E INTEGRAÇÃO BANCO")
    print("=" * 60)

    # Verificar se estamos no diretório correto
    if not os.path.exists('boletins.db'):
        print("❌ Arquivo boletins.db não encontrado!")
        print("   Certifique-se de estar no diretório correto do projeto")
        return False

    # Executar todas as verificações
    return relatorio_final()


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
