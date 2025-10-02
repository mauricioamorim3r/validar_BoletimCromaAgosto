# -*- coding: utf-8 -*-
"""
Script para criar template Excel completo e coerente com o banco de dados
Inclui TODOS os campos do banco de dados para importação
"""
import pandas as pd
from datetime import datetime


def criar_template_excel_completo():
    """Cria template Excel com TODOS os campos do banco de dados"""

    print("Criando template Excel completo...")

    # ===== ABA 1: INFORMAÇÕES DO BOLETIM =====
    dados_boletins = {
        # Campos obrigatórios do sistema
        'numero_boletim': ['PTJ/24-001', 'PTJ/24-002'],
        'numero_documento': ['DOC-2024-001', 'DOC-2024-002'],
        'data_coleta': ['2024-01-15', '2024-01-16'],
        'data_recebimento': ['2024-01-16', '2024-01-17'],
        'data_analise': ['2024-01-17', '2024-01-18'],
        'data_emissao': ['2024-01-20', '2024-01-21'],
        'data_validacao': ['2024-01-21', '2024-01-22'],

        # Informações da instalação e processo
        'identificacao_instalacao': ['FPSO ATLANTE', 'FPSO ATLANTE'],
        'plataforma': ['FPSO ATLANTE', 'FPSO ATLANTE'],
        'sistema_medicao': ['GÁS COMBUSTÍVEL LP', 'GÁS COMBUSTÍVEL LP'],
        'classificacao': ['FISCAL', 'FISCAL'],
        'ponto_coleta': ['LP FUEL GAS', 'LP FUEL GAS'],
        'agente_regulado': ['SGM LTDA', 'SGM LTDA'],

        # Responsáveis e condições
        'responsavel_amostragem': ['João Silva', 'Maria Santos'],
        'pressao': [1.013, 1.015],
        'temperatura': [25.0, 24.8],

        # Responsáveis técnicos
        'responsavel_tecnico': ['Dr. Carlos Ferreira', 'Dr. Carlos Ferreira'],
        'responsavel_elaboracao': ['Ana Costa', 'Pedro Lima'],
        'responsavel_aprovacao': ['Gerente QA', 'Gerente QA'],

        # Observações
        'observacoes': ['Análise conforme procedimento padrão', 'Verificar condições ambientais']
    }

    # ===== ABA 2: COMPONENTES GASOSOS =====
    componentes_lista = [
        'Metano, CH₄',
        'Etano, C₂H₆',
        'Propano, C₃H₈',
        'i-Butano, i-C₄H₁₀',
        'n-Butano, n-C₄H₁₀',
        'i-Pentano, i-C₅H₁₂',
        'n-Pentano, n-C₅H₁₂',
        'n-Hexano, n-C₆H₁₄',
        'n-Heptano, n-C₇H₁₆',
        'n-Octano, n-C₈H₁₈',
        'n-Nonano, n-C₉H₂₀',
        'n-Decano, n-C₁₀H₂₂',
        'Oxigênio, O₂',
        'Nitrogênio, N₂',
        'Dióxido de Carbono, CO₂'
    ]

    # Percentuais exemplo que somam 100%
    percentuais_exemplo_1 = [
        85.234,  # Metano
        8.567,   # Etano
        3.123,   # Propano
        0.876,   # i-Butano
        1.234,   # n-Butano
        0.445,   # i-Pentano
        0.321,   # n-Pentano
        0.123,   # Hexano
        0.045,   # Heptano
        0.012,   # Octano
        0.008,   # Nonano
        0.005,   # Decano
        0.002,   # Oxigênio
        0.003,   # Nitrogênio
        0.002    # CO2
    ]

    percentuais_exemplo_2 = [
        86.123,  # Metano
        7.890,   # Etano
        2.987,   # Propano
        0.765,   # i-Butano
        1.098,   # n-Butano
        0.543,   # i-Pentano
        0.298,   # n-Pentano
        0.156,   # Hexano
        0.078,   # Heptano
        0.034,   # Octano
        0.015,   # Nonano
        0.008,   # Decano
        0.003,   # Oxigênio
        0.001,   # Nitrogênio
        0.001    # CO2
    ]

    dados_componentes = []
    for i, boletim in enumerate(['PTJ/24-001', 'PTJ/24-002']):
        percentuais = percentuais_exemplo_1 if i == 0 else percentuais_exemplo_2
        for j, comp in enumerate(componentes_lista):
            dados_componentes.append({
                'numero_boletim': boletim,
                'componente': comp,
                'percentual_molar': percentuais[j],
                'unidade': '% mol'
            })

    # ===== ABA 3: PROPRIEDADES DO FLUIDO =====
    propriedades_lista = [
        'Fator de compressibilidade Condição de Referência (20°C / 1 atm)',
        'Massa Específica Condição de Referência (20°C / 1 atm)',
        'Massa Molecular'
    ]

    unidades_propriedades = [
        'adimensional',
        'kg/m³',
        'g/mol'
    ]

    valores_exemplo_1 = [0.9876, 0.7234, 18.567]
    valores_exemplo_2 = [0.9823, 0.7156, 18.234]

    dados_propriedades = []
    for i, boletim in enumerate(['PTJ/24-001', 'PTJ/24-002']):
        valores = valores_exemplo_1 if i == 0 else valores_exemplo_2
        for j, prop in enumerate(propriedades_lista):
            dados_propriedades.append({
                'numero_boletim': boletim,
                'propriedade': prop,
                'valor': valores[j],
                'unidade': unidades_propriedades[j]
            })

    # ===== ABA 4: CHECKLIST NBR ISO/IEC 17025 =====
    checklist_itens = [
        'Identificação do boletim de resultados analíticos',
        'Identificação da amostra',
        'Descrição da data de amostragem',
        'Descrição da data de recebimento da amostra pelo laboratório',
        'Descrição da data de realização das análises',
        'Descrição da data de emissão do BRA',
        'Identificação do campo produtor ou da instalação',
        'Identificação do agente regulado',
        'Identificação do ponto de medição e/ou do poço quando aplicável',
        'Resultados das análises e normas ou procedimentos utilizados',
        'Descrição das características do processo do ponto de amostragem do fluido (pressão e temperatura)',
        'Identificação do responsável pela amostragem',
        'Indicação dos incertezas de medição, com descrição do nível de confiança e fator de abrangência',
        'Identificação dos responsáveis técnicos pela realização da análise',
        'Identificação dos responsáveis pela elaboração e aprovação do boletim'
    ]

    dados_checklist = []
    for boletim in ['PTJ/24-001', 'PTJ/24-002']:
        for i, item in enumerate(checklist_itens, 1):
            dados_checklist.append({
                'numero_boletim': boletim,
                'item_numero': i,
                'descricao': item,
                'situacao': '✓ OK',  # Exemplo: pode ser '✓ OK' ou '✗ NOK'
                'nao_aplicavel': 'Não',  # 'Sim' ou 'Não'
                'observacao': ''  # Observações específicas
            })

    # ===== CRIAR ARQUIVO EXCEL =====
    df_boletins = pd.DataFrame(dados_boletins)
    df_componentes = pd.DataFrame(dados_componentes)
    df_propriedades = pd.DataFrame(dados_propriedades)
    df_checklist = pd.DataFrame(dados_checklist)

    # Salvar template Excel completo
    template_path = 'template_importacao_boletins_completo.xlsx'
    with pd.ExcelWriter(template_path, engine='openpyxl') as writer:
        # Aba 1: Informações do Boletim
        df_boletins.to_excel(writer, sheet_name='1_Informacoes_Boletim', index=False)

        # Aba 2: Componentes
        df_componentes.to_excel(writer, sheet_name='2_Componentes_Gasosos', index=False)

        # Aba 3: Propriedades
        df_propriedades.to_excel(writer, sheet_name='3_Propriedades_Fluido', index=False)

        # Aba 4: Checklist
        df_checklist.to_excel(writer, sheet_name='4_Checklist_ISO17025', index=False)

        # Aba 5: Instruções detalhadas
        instrucoes_detalhadas = pd.DataFrame({
            'INSTRUÇÕES COMPLETAS DE USO DO TEMPLATE': [
                '=== INSTRUÇÕES PARA IMPORTAÇÃO DE BOLETINS CROMATOGRÁFICOS ===',
                '',
                '1. ABA "1_Informacoes_Boletim":',
                '   - Preencha TODOS os campos obrigatórios',
                '   - Use formato de data YYYY-MM-DD (ex: 2024-01-15)',
                '   - numero_boletim deve ser único no sistema',
                '   - Todas as datas devem respeitar a sequência cronológica',
                '   - Atenção às regras RTM 52 da ANP para prazos',
                '',
                '2. ABA "2_Componentes_Gasosos":',
                '   - OBRIGATÓRIO: todos os 15 componentes para cada boletim',
                '   - O somatório dos percentuais deve ser 100%',
                '   - Use ponto (.) como separador decimal',
                '   - numero_boletim deve corresponder ao da Aba 1',
                '',
                '3. ABA "3_Propriedades_Fluido":',
                '   - Inclua as 3 propriedades obrigatórias para cada boletim',
                '   - Valores devem estar dentro dos limites AGA#8',
                '   - Precision adequada para cada propriedade',
                '',
                '4. ABA "4_Checklist_ISO17025":',
                '   - Todos os 15 itens são obrigatórios',
                '   - Situação: use "✓ OK" ou "✗ NOK"',
                '   - nao_aplicavel: "Sim" ou "Não"',
                '   - Adicione observações quando necessário',
                '',
                '5. VALIDAÇÕES AUTOMÁTICAS:',
                '   - Soma dos percentuais = 100% ±0.001%',
                '   - Limites normativos A.G.A #8',
                '   - Controle estatístico de processo (CEP)',
                '   - Validação RTM 52 da ANP (prazos)',
                '   - Checklist NBR ISO/IEC 17025 completo',
                '',
                '6. APÓS O PREENCHIMENTO:',
                '   - Salve o arquivo Excel',
                '   - Faça upload na página "Importar Excel"',
                '   - Verifique os relatórios gerados',
                '   - Aprove os boletins validados',
                '',
                '=== COMPONENTES OBRIGATÓRIOS (15 itens) ===',
                'Metano, CH₄',
                'Etano, C₂H₆',
                'Propano, C₃H₈',
                'i-Butano, i-C₄H₁₀',
                'n-Butano, n-C₄H₁₀',
                'i-Pentano, i-C₅H₁₂',
                'n-Pentano, n-C₅H₁₂',
                'n-Hexano, n-C₆H₁₄',
                'n-Heptano, n-C₇H₁₆',
                'n-Octano, n-C₈H₁₈',
                'n-Nonano, n-C₉H₂₀',
                'n-Decano, n-C₁₀H₂₂',
                'Oxigênio, O₂',
                'Nitrogênio, N₂',
                'Dióxido de Carbono, CO₂',
                '',
                '=== PROPRIEDADES OBRIGATÓRIAS (3 itens) ===',
                'Fator de compressibilidade Condição de Referência (20°C / 1 atm)',
                'Massa Específica Condição de Referência (20°C / 1 atm)',
                'Massa Molecular',
                '',
                '=== REGRAS RTM 52 DA ANP ===',
                'Prazo Coleta → Emissão: máximo 25 dias',
                'Prazo Emissão → Validação: máximo 1 dia',
                'Prazo Total (Coleta → Validação): máximo 28 dias',
                '',
                '=== LIMITES A.G.A #8 (Exemplos) ===',
                'Metano: 0-100% mol',
                'Propano: 0-12% mol',
                'Butanos: 0-6% mol cada',
                'Pentanos: 0-4% mol cada',
                'Oxigênio: 0-21% mol',
                '',
                '=== SUPORTE ===',
                'Em caso de dúvidas, consulte a documentação do sistema',
                'ou entre em contato com a equipe técnica.',
                '',
                'Template criado em: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
        })

        instrucoes_detalhadas.to_excel(writer, sheet_name='INSTRUÇÕES', index=False)

        # Ajustar largura das colunas para melhor visualização
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except Exception:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

    print(f"✅ Template Excel completo criado: {template_path}")
    print("\n📋 ESTRUTURA DO TEMPLATE:")
    print("   🗂️  Aba 1: Informações do Boletim (24 campos)")
    print("   🧪 Aba 2: Componentes Gasosos (15 componentes)")
    print("   📊 Aba 3: Propriedades do Fluido (3 propriedades)")
    print("   ✅ Aba 4: Checklist ISO/IEC 17025 (15 itens)")
    print("   📖 Aba 5: Instruções Completas")
    print(f"\n🎯 Total de campos por boletim: {len(dados_boletins)} + {len(componentes_lista)} componentes + 3 propriedades + 15 checklist = 57+ campos")

    return template_path


if __name__ == "__main__":
    template_path = criar_template_excel_completo()
    print(f"\n🚀 Template disponível em: {template_path}")
