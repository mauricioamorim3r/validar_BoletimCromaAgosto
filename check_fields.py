import sqlite3


def compare_fields():
    conn = sqlite3.connect('boletins.db')
    cursor = conn.cursor()

    # Buscar boletim PTJ/24-14803 para comparar campos
    cursor.execute('''
        SELECT numero_boletim, numero_documento, data_coleta, data_emissao, data_validacao,
               identificacao_instalacao, plataforma, sistema_medicao, classificacao,
               ponto_coleta, agente_regulado, responsavel_amostragem,
               pressao, temperatura, observacoes,
               responsavel_tecnico, responsavel_elaboracao, responsavel_aprovacao
        FROM boletins WHERE numero_boletim = "PTJ/24-14803"
    ''')

    boletim = cursor.fetchone()
    if boletim:
        print("Campos do boletim PTJ/24-14803:")
        fields = [
            'numero_boletim', 'numero_documento', 'data_coleta', 'data_emissao', 'data_validacao',
            'identificacao_instalacao', 'plataforma', 'sistema_medicao', 'classificacao',
            'ponto_coleta', 'agente_regulado', 'responsavel_amostragem',
            'pressao', 'temperatura', 'observacoes',
            'responsavel_tecnico', 'responsavel_elaboracao', 'responsavel_aprovacao'
        ]

        for i, field in enumerate(fields):
            value = boletim[i] if boletim[i] else "(vazio)"
            print(f"  {field}: {value}")

    # Verificar quantos boletins foram carregados vs cadastrados manualmente
    cursor.execute('SELECT COUNT(*) FROM boletins WHERE numero_documento LIKE "%/%"')
    historicos = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM boletins WHERE numero_documento LIKE "%/2025"')
    manuais = cursor.fetchone()[0]

    print("\nEstatísticas:")
    print(f"  Boletins históricos carregados: {historicos}")
    print(f"  Boletins cadastrados manualmente: {manuais}")

    conn.close()


if __name__ == '__main__':
    compare_fields()
