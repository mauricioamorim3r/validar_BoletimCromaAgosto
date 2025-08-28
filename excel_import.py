# Funcionalidades de importação de dados Excel
import pandas as pd
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename


def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processar_excel_boletins(arquivo_path):
    """
    Processa arquivo Excel com dados de boletins cromatográficos

    Estrutura esperada do Excel:
    - Aba 1: Dados do Boletim (cabeçalho)
    - Aba 2: Componentes (Metano, Etano, etc.)
    - Aba 3: Propriedades (opcional)
    """
    try:
        # Ler arquivo Excel
        xl_file = pd.ExcelFile(arquivo_path)

        results = {
            'success': 0,
            'errors': [],
            'boletins_processados': []
        }

        # Verificar abas necessárias
        if 'Boletins' not in xl_file.sheet_names:
            results['errors'].append("Aba 'Boletins' não encontrada no arquivo")
            return results

        if 'Componentes' not in xl_file.sheet_names:
            results['errors'].append("Aba 'Componentes' não encontrada no arquivo")
            return results

        # Ler dados das abas
        df_boletins = pd.read_excel(arquivo_path, sheet_name='Boletins')
        df_componentes = pd.read_excel(arquivo_path, sheet_name='Componentes')

        # Conectar ao banco de dados
        conn = sqlite3.connect('boletins.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Processar cada boletim
        for index, boletim_row in df_boletins.iterrows():
            try:
                boletim_data = processar_linha_boletim(boletim_row, df_componentes, cursor, conn)
                results['boletins_processados'].append(boletim_data)
                results['success'] += 1

            except Exception as e:
                results['errors'].append(f"Erro ao processar boletim linha {index + 2}: {str(e)}")

        conn.close()
        return results

    except Exception as e:
        return {
            'success': 0,
            'errors': [f"Erro ao processar arquivo: {str(e)}"],
            'boletins_processados': []
        }


def processar_linha_boletim(boletim_row, df_componentes, cursor, conn):
    """Processa uma linha de boletim e seus componentes"""

    # Extrair dados do boletim
    numero_boletim = str(boletim_row.get('numero_boletim', ''))
    data_coleta = pd.to_datetime(boletim_row.get('data_coleta')).strftime('%Y-%m-%d')
    data_emissao = pd.to_datetime(boletim_row.get('data_emissao')).strftime('%Y-%m-%d')
    instalacao = str(boletim_row.get('identificacao_instalacao', 'FPSO ATLANTE'))

    # Inserir boletim
    cursor.execute('''
        INSERT INTO boletins (
            numero_boletim, data_coleta, data_emissao, identificacao_instalacao,
            plataforma, sistema_medicao, classificacao, ponto_coleta,
            agente_regulado, ponto_medicao, responsavel_amostragem,
            pressao, temperatura, observacoes, responsavel_tecnico,
            responsavel_elaboracao, responsavel_aprovacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        numero_boletim, data_coleta, data_emissao, instalacao,
        'FPSO ATLANTE', 'GÁS COMBUSTÍVEL LP', 'FISCAL', 'LP FUEL GAS',
        boletim_row.get('agente_regulado', ''),
        boletim_row.get('ponto_medicao', ''),
        boletim_row.get('responsavel_amostragem', ''),
        float(boletim_row.get('pressao', 0)),
        float(boletim_row.get('temperatura', 0)),
        str(boletim_row.get('observacoes', '')),
        str(boletim_row.get('responsavel_tecnico', '')),
        str(boletim_row.get('responsavel_elaboracao', '')),
        str(boletim_row.get('responsavel_aprovacao', ''))
    ))

    boletim_id = cursor.lastrowid

    # Buscar componentes para este boletim
    componentes_boletim = df_componentes[df_componentes['numero_boletim'] == numero_boletim]

    # Lista de componentes esperados
    componentes_esperados = [
        'Metano', 'Etano', 'Propano', 'i-Butano', 'n-Butano',
        'i-Pentano', 'n-Pentano', 'Hexano', 'Heptano', 'Octano',
        'Nonano', 'Decano', 'Oxigênio', 'Nitrogênio', 'CO2'
    ]

    for componente in componentes_esperados:
        # Buscar valor do componente na planilha
        comp_row = componentes_boletim[componentes_boletim['componente'] == componente]

        if not comp_row.empty:
            valor = float(comp_row.iloc[0]['percentual_molar'])
        else:
            valor = 0.0  # Valor padrão se não encontrado

        # Validações
        status_aga = "VALIDADO" if valida_aga8_import(componente, valor) else "INVALIDADO"
        historico = get_historico_componente_import(componente, cursor)
        status_cep = "VALIDADO" if valida_cep_import(componente, valor, historico) else "INVALIDADO"

        # Inserir componente
        cursor.execute('''
            INSERT INTO componentes (boletin_id, nome, percentual_molar, status_aga, status_cep)
            VALUES (?, ?, ?, ?, ?)
        ''', (boletim_id, componente, valor, status_aga, status_cep))

        # Inserir no histórico
        cursor.execute('''
            INSERT INTO historico_componentes (componente, boletin_id, valor, data_coleta)
            VALUES (?, ?, ?, ?)
        ''', (componente, boletim_id, valor, data_coleta))

    # Calcular status geral do boletim
    cursor.execute('''
        SELECT COUNT(*) FROM componentes
        WHERE boletin_id = ? AND (status_aga = ? OR status_cep = ?)
    ''', (boletim_id, 'INVALIDADO', 'INVALIDADO'))

    componentes_invalidos = cursor.fetchone()[0]
    status_geral = "INVALIDADO" if componentes_invalidos > 0 else "VALIDADO"
    data_validacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Atualizar boletim com status
    cursor.execute('''
        UPDATE boletins SET status = ?, data_validacao = ? WHERE id = ?
    ''', (status_geral, data_validacao, boletim_id))

    conn.commit()

    return {
        'numero_boletim': numero_boletim,
        'status': status_geral,
        'componentes_processados': len(componentes_esperados)
    }


def valida_aga8_import(componente, valor):
    """Validação A.G.A #8 para importação"""
    limites = {
        "Metano": (0, 100), "Etano": (0, 100), "Propano": (0, 12),
        "i-Butano": (0, 6), "n-Butano": (0, 6), "i-Pentano": (0, 4),
        "n-Pentano": (0, 4), "Hexano": (0, 100), "Heptano": (0, 100),
        "Octano": (0, 100), "Nonano": (0, 100), "Decano": (0, 100),
        "Oxigênio": (0, 21), "Nitrogênio": (0, 100), "CO2": (0, 100)
    }

    if componente in limites:
        minimo, maximo = limites[componente]
        return minimo <= valor <= maximo
    return True


def valida_cep_import(componente, novo_valor, historico):
    """Validação CEP para importação"""
    if len(historico) < 2:
        return True

    ultimas_amostras = historico[-8:] if len(historico) >= 8 else historico
    media = sum(ultimas_amostras) / len(ultimas_amostras)

    amplitudes = [abs(ultimas_amostras[i] - ultimas_amostras[i - 1])
                  for i in range(1, len(ultimas_amostras))]

    if not amplitudes:
        return True

    media_amplitudes = sum(amplitudes) / len(amplitudes)
    d2 = 1.128
    lcs = media + 3 * media_amplitudes / d2
    lci = media - 3 * media_amplitudes / d2

    return lci <= novo_valor <= lcs


def get_historico_componente_import(componente, cursor):
    """Busca histórico para validação CEP durante importação"""
    cursor.execute('''
        SELECT valor FROM historico_componentes
        WHERE componente = ?
        ORDER BY data_coleta ASC
    ''', (componente,))

    historico = cursor.fetchall()
    return [row[0] for row in historico]


def criar_template_excel():
    """Cria um template Excel para importação de dados"""

    # Dados exemplo para o template
    dados_boletins = {
        'numero_boletim': ['PTJ/24-EXEMPLO1', 'PTJ/24-EXEMPLO2'],
        'data_coleta': ['2024-01-15', '2024-01-16'],
        'data_emissao': ['2024-01-20', '2024-01-21'],
        'identificacao_instalacao': ['FPSO ATLANTE', 'FPSO ATLANTE'],
        'agente_regulado': ['BRAVA ENERGIA', 'BRAVA ENERGIA'],
        'ponto_medicao': ['PM-001', 'PM-002'],
        'responsavel_amostragem': ['João Silva', 'Maria Santos'],
        'pressao': [1.013, 1.015],
        'temperatura': [25.0, 24.8],
        'observacoes': ['', ''],
        'responsavel_tecnico': ['Dr. Carlos', 'Dr. Carlos'],
        'responsavel_elaboracao': ['Ana Costa', 'Ana Costa'],
        'responsavel_aprovacao': ['Gerente QA', 'Gerente QA']
    }

    dados_componentes = []
    componentes = ['Metano', 'Etano', 'Propano', 'i-Butano', 'n-Butano',
                   'i-Pentano', 'n-Pentano', 'Hexano', 'Heptano', 'Octano',
                   'Nonano', 'Decano', 'Oxigênio', 'Nitrogênio', 'CO2']

    # Criar dados exemplo para componentes
    for boletim in ['PTJ/24-EXEMPLO1', 'PTJ/24-EXEMPLO2']:
        for comp in componentes:
            dados_componentes.append({
                'numero_boletim': boletim,
                'componente': comp,
                'percentual_molar': 0.0  # Valor exemplo
            })

    # Criar DataFrames
    df_boletins = pd.DataFrame(dados_boletins)
    df_componentes = pd.DataFrame(dados_componentes)

    # Salvar template Excel
    template_path = 'template_importacao_boletins.xlsx'
    with pd.ExcelWriter(template_path, engine='openpyxl') as writer:
        df_boletins.to_excel(writer, sheet_name='Boletins', index=False)
        df_componentes.to_excel(writer, sheet_name='Componentes', index=False)

        # Adicionar aba de instruções
        instrucoes = pd.DataFrame({
            'INSTRUÇÕES DE USO': [
                '1. Preencha a aba "Boletins" com os dados básicos de cada boletim',
                '2. Preencha a aba "Componentes" com os percentuais molares',
                '3. Certifique-se de que numero_boletim seja igual nas duas abas',
                '4. Todos os 15 componentes devem estar presentes para cada boletim',
                '5. Use formato de data YYYY-MM-DD (ex: 2024-01-15)',
                '6. Salve o arquivo e faça o upload no sistema',
                '',
                'COMPONENTES OBRIGATÓRIOS:',
                'Metano, Etano, Propano, i-Butano, n-Butano,',
                'i-Pentano, n-Pentano, Hexano, Heptano, Octano,',
                'Nonano, Decano, Oxigênio, Nitrogênio, CO2'
            ]
        })
        instrucoes.to_excel(writer, sheet_name='Instruções', index=False)

    return template_path
