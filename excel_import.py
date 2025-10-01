# Funcionalidades de importação de dados Excel
import pandas as pd
import sqlite3
from datetime import datetime


def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processar_excel_boletins(arquivo_path):
    """
    Processa arquivo Excel COMPLETO com dados de boletins cromatográficos

    Estrutura esperada do Excel:
    - Aba 1: Boletins (TODOS os campos do banco)
    - Aba 2: Componentes (15 componentes gasosos)
    - Aba 3: Propriedades (3 propriedades do fluido)
    - Aba 4: Checklist (15 itens NBR ISO/IEC 17025)
    """
    try:
        # Ler arquivo Excel
        results = {
            'success': 0,
            'errors': [],
            'boletins_processados': []
        }

        with pd.ExcelFile(arquivo_path) as xl_file:
            sheet_names = xl_file.sheet_names

            # Verificar abas necessárias
            abas_obrigatorias = ['Boletins', 'Componentes', 'Propriedades', 'Checklist']
            for aba in abas_obrigatorias:
                if aba not in sheet_names:
                    results['errors'].append(f"Aba '{aba}' não encontrada no arquivo")
                    return results

            # Ler dados das abas diretamente do Excel aberto
            df_boletins = xl_file.parse('Boletins')
            df_componentes = xl_file.parse('Componentes')
            df_propriedades = xl_file.parse('Propriedades')
            df_checklist = xl_file.parse('Checklist')

        # Conectar ao banco de dados
        conn = sqlite3.connect('boletins.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Processar cada boletim
        for index, boletim_row in df_boletins.iterrows():
            try:
                numero_boletim = str(boletim_row.get('numero_boletim', ''))
                # Processar boletim completo
                componentes_count = len(df_componentes[df_componentes['numero_boletim'] == numero_boletim])
                propriedades_count = len(df_propriedades[df_propriedades['numero_boletim'] == numero_boletim])
                checklist_count = len(df_checklist[df_checklist['numero_boletim'] == numero_boletim])
                boletim_data = processar_linha_boletim_completo(
                    boletim_row, df_componentes, df_propriedades,
                    df_checklist, cursor, conn
                )

                results['boletins_processados'].append({
                    'numero_boletim': numero_boletim,
                    'id': boletim_data,
                    'status': 'Processado com sucesso',
                    'componentes_processados': componentes_count,
                    'propriedades_processadas': propriedades_count,
                    'checklist_processados': checklist_count
                })
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


def processar_linha_boletim_completo(boletim_row, df_componentes, df_propriedades, df_checklist, cursor, conn):
    """Processa uma linha de boletim COMPLETA com todos os campos e relacionamentos"""

    # ===== EXTRAIR DADOS COMPLETOS DO BOLETIM =====
    numero_boletim = str(boletim_row.get('numero_boletim', ''))
    numero_documento = str(boletim_row.get('numero_documento', ''))

    # Datas - converter para formato do banco
    def safe_date_convert(date_val):
        if pd.isna(date_val) or date_val == '':
            return None
        try:
            return pd.to_datetime(date_val).strftime('%Y-%m-%d')
        except Exception:
            return None

    data_coleta = safe_date_convert(boletim_row.get('data_coleta'))
    data_recebimento = safe_date_convert(boletim_row.get('data_recebimento'))
    data_analise = safe_date_convert(boletim_row.get('data_analise'))
    data_emissao = safe_date_convert(boletim_row.get('data_emissao'))
    data_validacao = safe_date_convert(boletim_row.get('data_validacao'))

    # Informações da instalação
    identificacao_instalacao = str(boletim_row.get('identificacao_instalacao', 'FPSO ATLANTE'))
    plataforma = str(boletim_row.get('plataforma', 'FPSO ATLANTE'))
    sistema_medicao = str(boletim_row.get('sistema_medicao', 'GÁS COMBUSTÍVEL LP'))
    classificacao = str(boletim_row.get('classificacao', 'FISCAL'))
    ponto_coleta = str(boletim_row.get('ponto_coleta', 'LP FUEL GAS'))
    agente_regulado = str(boletim_row.get('agente_regulado', 'BRAVA ENERGIA'))

    # Responsáveis
    responsavel_amostragem = str(boletim_row.get('responsavel_amostragem', ''))
    responsavel_tecnico = str(boletim_row.get('responsavel_tecnico', ''))
    responsavel_elaboracao = str(boletim_row.get('responsavel_elaboracao', ''))
    responsavel_aprovacao = str(boletim_row.get('responsavel_aprovacao', ''))

    # Condições do processo
    def safe_float_convert(val):
        try:
            return float(val) if not pd.isna(val) else None
        except Exception:
            return None

    pressao = safe_float_convert(boletim_row.get('pressao'))
    temperatura = safe_float_convert(boletim_row.get('temperatura'))

    # Status de validação
    status = str(boletim_row.get('status', 'PENDENTE'))
    status_aga8 = str(boletim_row.get('status_aga8', 'PENDENTE'))
    status_cep = str(boletim_row.get('status_cep', 'PENDENTE'))
    status_checklist = str(boletim_row.get('status_checklist', 'PENDENTE'))

    # Observações
    observacoes = str(boletim_row.get('observacoes', ''))

    # ===== INSERIR BOLETIM COMPLETO =====
    cursor.execute('''
        INSERT INTO boletins (
            numero_boletim, numero_documento,
            data_coleta, data_recebimento, data_analise, data_emissao, data_validacao,
            identificacao_instalacao, plataforma, sistema_medicao, classificacao,
            ponto_coleta, agente_regulado,
            responsavel_amostragem, responsavel_tecnico, responsavel_elaboracao,
            responsavel_aprovacao,
            pressao, temperatura,
            status, status_aga8, status_cep, status_checklist,
            observacoes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        numero_boletim, numero_documento,
        data_coleta, data_recebimento, data_analise, data_emissao, data_validacao,
        identificacao_instalacao, plataforma, sistema_medicao, classificacao,
        ponto_coleta, agente_regulado,
        responsavel_amostragem, responsavel_tecnico, responsavel_elaboracao,
        responsavel_aprovacao,
        pressao, temperatura,
        status, status_aga8, status_cep, status_checklist,
        observacoes
    ))

    boletim_id = cursor.lastrowid

    # ===== PROCESSAR COMPONENTES =====
    componentes_boletim = df_componentes[df_componentes['numero_boletim'] == numero_boletim]
    for _, comp_row in componentes_boletim.iterrows():
        cursor.execute('''
            INSERT INTO componentes (
                boletin_id, nome, percentual_molar, status_aga, status_cep,
                limite_inferior_aga, limite_superior_aga, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            boletim_id,
            str(comp_row.get('componente', '')),
            safe_float_convert(comp_row.get('percentual_molar', 0)),
            str(comp_row.get('status_aga', 'PENDENTE')),
            str(comp_row.get('status_cep', 'PENDENTE')),
            safe_float_convert(comp_row.get('limite_inferior_aga', 0)),
            safe_float_convert(comp_row.get('limite_superior_aga', 100)),
            str(comp_row.get('observacoes', ''))
        ))

    # ===== PROCESSAR PROPRIEDADES =====
    propriedades_boletim = df_propriedades[df_propriedades['numero_boletim'] == numero_boletim]
    for _, prop_row in propriedades_boletim.iterrows():
        cursor.execute('''
            INSERT INTO propriedades (
                boletin_id, nome, valor, status_aga, status_cep, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            boletim_id,
            str(prop_row.get('propriedade', '')),
            safe_float_convert(prop_row.get('valor', 0)),
            str(prop_row.get('status_aga', 'PENDENTE')),
            str(prop_row.get('status_cep', 'PENDENTE')),
            str(prop_row.get('observacoes', ''))
        ))

    # ===== PROCESSAR CHECKLIST =====
    checklist_boletim = df_checklist[df_checklist['numero_boletim'] == numero_boletim]
    for _, check_row in checklist_boletim.iterrows():
        cursor.execute('''
            INSERT INTO checklist_itens (
                boletin_id, item_numero, descricao, situacao, nao_aplicavel, observacao
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            boletim_id,
            int(check_row.get('item_numero', 1)),
            str(check_row.get('descricao', '')),
            str(check_row.get('situacao', 'PENDENTE')),
            str(check_row.get('nao_aplicavel', 'Não')),
            str(check_row.get('observacao', ''))
        ))

    # Confirmar transação
    conn.commit()

    return boletim_id


def processar_linha_boletim(boletim_row, df_componentes, cursor, conn):
    """Processa uma linha de boletim e seus componentes - VERSÃO LEGADA"""

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
            agente_regulado, responsavel_amostragem,
            pressao, temperatura, observacoes, responsavel_tecnico,
            responsavel_elaboracao, responsavel_aprovacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        numero_boletim, data_coleta, data_emissao, instalacao,
        'FPSO ATLANTE', 'GÁS COMBUSTÍVEL LP', 'FISCAL', 'LP FUEL GAS',
        boletim_row.get('agente_regulado', ''),
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
    from config import LIMITES_AGA8

    if componente in LIMITES_AGA8:
        minimo = LIMITES_AGA8[componente]['min']
        maximo = LIMITES_AGA8[componente]['max']
        return minimo <= valor <= maximo
    return True


def valida_cep_import(componente, novo_valor, historico):
    """Validação CEP para importação"""
    from config import CEP_AMOSTRAS_MIN, CEP_D2_CONSTANT, CEP_SIGMA_LIMIT

    if len(historico) < 2:
        return True

    ultimas_amostras = historico[-CEP_AMOSTRAS_MIN:] if len(historico) >= CEP_AMOSTRAS_MIN else historico
    media = sum(ultimas_amostras) / len(ultimas_amostras)

    amplitudes = [abs(ultimas_amostras[i] - ultimas_amostras[i - 1])
                  for i in range(1, len(ultimas_amostras))]

    if not amplitudes:
        return True

    media_amplitudes = sum(amplitudes) / len(amplitudes)
    lcs = media + CEP_SIGMA_LIMIT * media_amplitudes / CEP_D2_CONSTANT
    lci = media - CEP_SIGMA_LIMIT * media_amplitudes / CEP_D2_CONSTANT

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
    """Cria um template Excel COMPLETO para importação com TODOS os campos do banco"""

    # Dados exemplo para o template - TODOS OS CAMPOS DO BOLETIM
    dados_boletins = {
        # ===== CAMPOS OBRIGATÓRIOS =====
        'numero_boletim': ['PTJ/24-EXEMPLO1', 'PTJ/24-EXEMPLO2'],
        'numero_documento': ['DOC-001-2024', 'DOC-002-2024'],

        # ===== DATAS =====
        'data_coleta': ['2024-01-15', '2024-01-16'],
        'data_recebimento': ['2024-01-16', '2024-01-17'],
        'data_analise': ['2024-01-17', '2024-01-18'],
        'data_emissao': ['2024-01-20', '2024-01-21'],
        'data_validacao': ['2024-01-21', '2024-01-22'],

        # ===== IDENTIFICAÇÃO E CLASSIFICAÇÃO =====
        'identificacao_instalacao': ['FPSO ATLANTE', 'FPSO ATLANTE'],
        'plataforma': ['FPSO ATLANTE', 'FPSO ATLANTE'],
        'sistema_medicao': ['GÁS COMBUSTÍVEL LP', 'GÁS COMBUSTÍVEL LP'],
        'classificacao': ['FISCAL', 'FISCAL'],
        'ponto_coleta': ['LP FUEL GAS', 'LP FUEL GAS'],
        'agente_regulado': ['BRAVA ENERGIA', 'BRAVA ENERGIA'],

        # ===== RESPONSÁVEIS =====
        'responsavel_amostragem': ['João Silva', 'Maria Santos'],
        'responsavel_tecnico': ['Dr. Carlos Oliveira', 'Dr. Carlos Oliveira'],
        'responsavel_elaboracao': ['Ana Costa', 'Pedro Silva'],
        'responsavel_aprovacao': ['Gerente QA', 'Gerente QA'],

        # ===== CONDIÇÕES DO PROCESSO =====
        'pressao': [1.013, 1.015],
        'temperatura': [25.0, 24.8],

        # ===== STATUS DE VALIDAÇÃO =====
        'status': ['PENDENTE', 'PENDENTE'],
        'status_aga8': ['PENDENTE', 'PENDENTE'],
        'status_cep': ['PENDENTE', 'PENDENTE'],
        'status_checklist': ['PENDENTE', 'PENDENTE'],

        # ===== OBSERVAÇÕES =====
        'observacoes': ['', 'Amostra coletada em condições normais']
    }

    dados_componentes = []
    componentes = [
        'Metano', 'Etano', 'Propano', 'i-Butano', 'n-Butano',
        'i-Pentano', 'n-Pentano', 'Hexano', 'Heptano', 'Octano',
        'Nonano', 'Decano', 'Oxigênio', 'Nitrogênio', 'CO2'
    ]

    # Valores exemplo realistas para componentes
    valores_exemplo = {
        'PTJ/24-EXEMPLO1': {
            'Metano': 85.245, 'Etano': 8.752, 'Propano': 3.456,
            'i-Butano': 0.875, 'n-Butano': 0.654, 'i-Pentano': 0.321,
            'n-Pentano': 0.298, 'Hexano': 0.156, 'Heptano': 0.089,
            'Octano': 0.045, 'Nonano': 0.023, 'Decano': 0.012,
            'Oxigênio': 0.045, 'Nitrogênio': 0.025, 'CO2': 0.004
        },
        'PTJ/24-EXEMPLO2': {
            'Metano': 86.125, 'Etano': 8.456, 'Propano': 3.234,
            'i-Butano': 0.756, 'n-Butano': 0.598, 'i-Pentano': 0.289,
            'n-Pentano': 0.267, 'Hexano': 0.134, 'Heptano': 0.078,
            'Octano': 0.034, 'Nonano': 0.018, 'Decano': 0.009,
            'Oxigênio': 0.002, 'Nitrogênio': 0.000, 'CO2': 0.000
        }
    }

    # Criar dados exemplo para componentes
    for boletim in ['PTJ/24-EXEMPLO1', 'PTJ/24-EXEMPLO2']:
        for comp in componentes:
            dados_componentes.append({
                'numero_boletim': boletim,
                'componente': comp,
                'percentual_molar': valores_exemplo[boletim][comp],
                'status_aga': 'PENDENTE',
                'status_cep': 'PENDENTE',
                'limite_inferior_aga': 0.0,
                'limite_superior_aga': 100.0,
                'observacoes': ''
            })

    # Dados exemplo para propriedades
    dados_propriedades = []
    propriedades = [
        'Fator de compressibilidade nas condições de base (15°C e 101,325 kPa)',
        'Massa específica relativa nas condições de base (15°C e 101,325 kPa)',
        'Massa molecular aparente'
    ]

    valores_props = {
        'PTJ/24-EXEMPLO1': [0.9876, 0.7234, 18.456],
        'PTJ/24-EXEMPLO2': [0.9823, 0.7189, 18.234]
    }

    for i, boletim in enumerate(['PTJ/24-EXEMPLO1', 'PTJ/24-EXEMPLO2']):
        for j, prop in enumerate(propriedades):
            dados_propriedades.append({
                'numero_boletim': boletim,
                'propriedade': prop,
                'valor': valores_props[boletim][j],
                'status_aga': 'PENDENTE',
                'status_cep': 'PENDENTE',
                'observacoes': ''
            })

    # Dados exemplo para checklist
    dados_checklist = []
    checklist_itens = [
        'A amostra foi identificada de forma única?',
        'O procedimento de amostragem foi seguido conforme norma?',
        'As condições de preservação da amostra foram adequadas?',
        'O transporte da amostra foi realizado corretamente?',
        'Os equipamentos de medição estavam calibrados?',
        'A rastreabilidade metrológica foi mantida?',
        'Os padrões de referência estão dentro da validade?',
        'As condições ambientais do laboratório foram controladas?',
        'O pessoal responsável pela análise está qualificado?',
        'Os registros de qualidade foram preenchidos?',
        'A incerteza de medição foi calculada?',
        'Os limites de detecção foram verificados?',
        'Cartas de controle foram analisadas?',
        'Ensaios de proficiência foram realizados?',
        'O relatório contém todas as informações necessárias?'
    ]

    for boletim in ['PTJ/24-EXEMPLO1', 'PTJ/24-EXEMPLO2']:
        for i, item in enumerate(checklist_itens, 1):
            dados_checklist.append({
                'numero_boletim': boletim,
                'item_numero': i,
                'descricao': item,
                'situacao': 'OK',
                'nao_aplicavel': 'Não',
                'observacao': ''
            })

    # Criar DataFrames
    df_boletins = pd.DataFrame(dados_boletins)
    df_componentes = pd.DataFrame(dados_componentes)
    df_propriedades = pd.DataFrame(dados_propriedades)
    df_checklist = pd.DataFrame(dados_checklist)

    # Salvar template Excel COMPLETO
    template_path = 'template_importacao_boletins.xlsx'
    with pd.ExcelWriter(template_path, engine='openpyxl') as writer:
        # ===== ABA 1: INFORMAÇÕES DOS BOLETINS =====
        df_boletins.to_excel(writer, sheet_name='Boletins', index=False)

        # ===== ABA 2: COMPONENTES GASOSOS =====
        df_componentes.to_excel(writer, sheet_name='Componentes', index=False)

        # ===== ABA 3: PROPRIEDADES DO FLUIDO =====
        df_propriedades.to_excel(writer, sheet_name='Propriedades', index=False)

        # ===== ABA 4: CHECKLIST NBR ISO/IEC 17025 =====
        df_checklist.to_excel(writer, sheet_name='Checklist', index=False)

        # ===== ABA 5: INSTRUÇÕES COMPLETAS =====
        instrucoes = pd.DataFrame({
            'MANUAL DE PREENCHIMENTO DO TEMPLATE - SISTEMA BRAVA ENERGIA': [
                '=== INSTRUÇÕES GERAIS ===',
                '1. Este template contém TODOS os campos do banco de dados do sistema',
                '2. Preencha todas as abas conforme orientações abaixo',
                '3. Use o numero_boletim como chave para relacionar dados entre abas',
                '4. Salve o arquivo e faça o upload no sistema',
                '5. O PDF final conterá 100% dos dados inseridos neste template',
                '',
                '=== ABA "BOLETINS" - INFORMAÇÕES PRINCIPAIS ===',
                '• numero_boletim: Código único (ex: PTJ/24-001)',
                '• numero_documento: Número do documento oficial',
                '• Datas: Use formato YYYY-MM-DD (ex: 2024-01-15)',
                '• data_coleta: Data da coleta da amostra',
                '• data_recebimento: Data de chegada no laboratório',
                '• data_analise: Data da análise laboratorial',
                '• data_emissao: Data de emissão do boletim',
                '• data_validacao: Data da validação técnica',
                '• identificacao_instalacao: Nome da instalação',
                '• plataforma: Nome da plataforma (ex: FPSO ATLANTE)',
                '• sistema_medicao: Sistema de medição utilizado',
                '• classificacao: Tipo de análise (FISCAL/CONTROLE)',
                '• ponto_coleta: Local específico da coleta',
                '• agente_regulado: Nome da empresa regulada',
                '• responsavel_amostragem: Técnico responsável pela coleta',
                '• responsavel_tecnico: Responsável técnico pela análise',
                '• responsavel_elaboracao: Quem elaborou o boletim',
                '• responsavel_aprovacao: Quem aprovou o boletim',
                '• pressao: Pressão em atm (número decimal)',
                '• temperatura: Temperatura em °C (número decimal)',
                '• status: PENDENTE/APROVADO/REJEITADO',
                '• status_aga8: Status validação A.G.A #8',
                '• status_cep: Status controle estatístico',
                '• status_checklist: Status do checklist ISO',
                '• observacoes: Observações gerais (opcional)',
                '',
                '=== ABA "COMPONENTES" - ANÁLISE CROMATOGRÁFICA ===',
                '• numero_boletim: Deve coincidir com aba Boletins',
                '• componente: Nome do componente químico',
                '• percentual_molar: % molar (número com 3 decimais)',
                '• status_aga: PENDENTE/OK/FORA_LIMITE',
                '• status_cep: PENDENTE/OK/FORA_CONTROLE',
                '• limite_inferior_aga: Limite mínimo A.G.A #8',
                '• limite_superior_aga: Limite máximo A.G.A #8',
                '• observacoes: Observações específicas do componente',
                '',
                'COMPONENTES OBRIGATÓRIOS (15 total):',
                'Metano, Etano, Propano, i-Butano, n-Butano,',
                'i-Pentano, n-Pentano, Hexano, Heptano, Octano,',
                'Nonano, Decano, Oxigênio, Nitrogênio, CO2',
                '',
                '=== ABA "PROPRIEDADES" - PROPRIEDADES DO FLUIDO ===',
                '• numero_boletim: Deve coincidir com aba Boletins',
                '• propriedade: Nome da propriedade física',
                '• valor: Valor numérico (4 decimais)',
                '• status_aga: Status validação A.G.A #8',
                '• status_cep: Status controle estatístico',
                '• observacoes: Observações específicas',
                '',
                'PROPRIEDADES OBRIGATÓRIAS:',
                '1. Fator de compressibilidade nas condições de base',
                '2. Massa específica relativa nas condições de base',
                '3. Massa molecular aparente',
                '',
                '=== ABA "CHECKLIST" - NBR ISO/IEC 17025 ===',
                '• numero_boletim: Deve coincidir com aba Boletins',
                '• item_numero: Número sequencial (1-15)',
                '• descricao: Texto do item de verificação',
                '• situacao: OK/NOK/PENDENTE',
                '• nao_aplicavel: Sim/Não',
                '• observacao: Comentários específicos do item',
                '',
                '=== VALIDAÇÃO RTM 52 - AUTOMÁTICA ===',
                'O sistema validará automaticamente:',
                '• Prazo coleta → emissão: máx 25 dias',
                '• Prazo emissão → validação: máx 1 dia',
                '• Prazo total: máx 28 dias (RTM 52 ANP)',
                '',
                '=== IMPORTANTE ===',
                '• Todos os campos preenchidos aparecerão no PDF final',
                '• O PDF será idêntico à tela de resultados',
                '• Sistema possui validação completa RTM 52',
                '• Backup dos dados é automático',
                '• Suporte técnico: sistema@bravaenergia.com'
            ]
        })
        instrucoes.to_excel(writer, sheet_name='Instruções', index=False)

        # ===== ABA 6: LIMITES E ESPECIFICAÇÕES =====
        especificacoes = pd.DataFrame({
            'LIMITES A.G.A #8 E ESPECIFICAÇÕES TÉCNICAS': [
                '=== LIMITES COMPONENTES A.G.A #8 ===',
                'Metano: 0% - 100%',
                'Etano: 0% - 100%',
                'Propano: 0% - 12%',
                'i-Butano: 0% - 6%',
                'n-Butano: 0% - 6%',
                'i-Pentano: 0% - 4%',
                'n-Pentano: 0% - 4%',
                'Hexano: 0% - 100%',
                'Heptano: 0% - 100%',
                'Octano: 0% - 100%',
                'Nonano: 0% - 100%',
                'Decano: 0% - 100%',
                'Oxigênio: 0% - 21%',
                'Nitrogênio: 0% - 100%',
                'CO2: 0% - 100%',
                '',
                '=== LIMITES PROPRIEDADES ===',
                'Fator Compressibilidade: 0.9 - 1.1',
                'Massa Específica: 0.65 - 0.9 kg/m³',
                'Massa Molecular: 16 - 22 g/mol',
                '',
                '=== PRAZOS RTM 52 ANP ===',
                'Coleta → Emissão: máximo 25 dias',
                'Emissão → Validação: máximo 1 dia',
                'Prazo Total: máximo 28 dias',
                '',
                '=== STATUS VÁLIDOS ===',
                'PENDENTE: Aguardando validação',
                'OK: Dentro dos limites',
                'NOK: Fora dos limites',
                'APROVADO: Boletim aprovado',
                'REJEITADO: Boletim rejeitado',
                'FORA_LIMITE: Componente fora A.G.A #8',
                'FORA_CONTROLE: Fora controle estatístico'
            ]
        })
        especificacoes.to_excel(writer, sheet_name='Especificações', index=False)

    print(f"OK: Template Excel COMPLETO criado: {template_path}")
    print("📊 Inclui TODOS os campos do banco de dados:")
    print("   - Aba Boletins: 25 campos completos")
    print("   - Aba Componentes: 15 componentes + status")
    print("   - Aba Propriedades: 3 propriedades + status")
    print("   - Aba Checklist: 15 itens ISO/IEC 17025")
    print("   - Aba Instruções: Manual completo")
    print("   - Aba Especificações: Limites e regras")

    return template_path
