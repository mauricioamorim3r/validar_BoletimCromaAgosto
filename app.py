from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from config import DEBUG, HOST, PORT
from excel_import import processar_excel_boletins, criar_template_excel, allowed_file

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_flask'

# Funções do banco de dados


def get_db():
    """Obtém conexão com o banco de dados"""
    db = sqlite3.connect('boletins.db')
    db.row_factory = sqlite3.Row
    return db


def init_db():
    """Inicializa o banco de dados"""
    db = get_db()

    # Criar tabela de boletins
    db.execute('''
    CREATE TABLE IF NOT EXISTS boletins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_boletim TEXT NOT NULL,
        numero_documento TEXT,
        data_coleta TEXT NOT NULL,
        data_recebimento TEXT,
        data_analise TEXT,
        data_emissao TEXT,
        data_validacao TEXT,
        identificacao_instalacao TEXT,
        plataforma TEXT,
        sistema_medicao TEXT,
        classificacao TEXT,
        ponto_medicao TEXT,
        ponto_coleta TEXT,
        agente_regulado TEXT,
        responsavel_amostragem TEXT,
        pressao REAL,
        temperatura REAL,
        observacoes TEXT,
        status TEXT,
        status_cep TEXT,
        status_aga8 TEXT,
        status_checklist TEXT,
        responsavel_tecnico TEXT,
        responsavel_elaboracao TEXT,
        responsavel_aprovacao TEXT
    )
    ''')

    # Criar tabela de componentes
    db.execute('''
    CREATE TABLE IF NOT EXISTS componentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        boletin_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        percentual_molar REAL NOT NULL,
        status_aga TEXT,
        status_cep TEXT,
        FOREIGN KEY (boletin_id) REFERENCES boletins (id) ON DELETE CASCADE
    )
    ''')

    # Criar tabela de propriedades
    db.execute('''
    CREATE TABLE IF NOT EXISTS propriedades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        boletin_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        valor REAL NOT NULL,
        status_aga TEXT,
        status_cep TEXT,
        FOREIGN KEY (boletin_id) REFERENCES boletins (id) ON DELETE CASCADE
    )
    ''')

    # Criar tabela de histórico de componentes
    db.execute('''
    CREATE TABLE IF NOT EXISTS historico_componentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        componente TEXT NOT NULL,
        boletin_id INTEGER NOT NULL,
        valor REAL NOT NULL,
        data_coleta TEXT NOT NULL,
        FOREIGN KEY (boletin_id) REFERENCES boletins (id) ON DELETE CASCADE
    )
    ''')

    # Criar tabela de histórico de propriedades
    db.execute('''
    CREATE TABLE IF NOT EXISTS historico_propriedades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        propriedade TEXT NOT NULL,
        boletin_id INTEGER NOT NULL,
        valor REAL NOT NULL,
        data_coleta TEXT NOT NULL,
        FOREIGN KEY (boletin_id) REFERENCES boletins (id) ON DELETE CASCADE
    )
    ''')

    # Criar tabela de checklist
    db.execute('''
    CREATE TABLE IF NOT EXISTS checklist_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        boletin_id INTEGER NOT NULL,
        item_numero INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        situacao TEXT NOT NULL DEFAULT 'OK',
        nao_aplicavel BOOLEAN DEFAULT FALSE,
        observacao TEXT,
        FOREIGN KEY (boletin_id) REFERENCES boletins (id) ON DELETE CASCADE
    )
    ''')

    db.commit()


# Inicializar o banco de dados
init_db()

# Funções de validação


def valida_aga8(componente, valor):
    """Valida componente contra os limites da norma A.G.A #8"""
    limites = {
        "Metano": (0, 100),
        "Etano": (0, 100),
        "Propano": (0, 12),
        "i-Butano": (0, 6),
        "n-Butano": (0, 6),
        "i-Pentano": (0, 4),
        "n-Pentano": (0, 4),
        "Hexano": (0, 100),
        "Heptano": (0, 100),
        "Octano": (0, 100),
        "Nonano": (0, 100),
        "Decano": (0, 100),
        "Oxigênio": (0, 21),
        "Nitrogênio": (0, 100),
        "CO2": (0, 100)
    }
    if componente in limites:
        minimo, maximo = limites[componente]
        return minimo <= valor <= maximo
    return True


def valida_cep(componente, novo_valor, historico):
    """Valida componente usando Controle Estatístico de Processo"""
    ultimas_amostras = historico[-8:]

    if len(ultimas_amostras) < 2:
        return True

    media = sum(ultimas_amostras) / len(ultimas_amostras)

    amplitudes = [abs(ultimas_amostras[i] - ultimas_amostras[i - 1])
                  for i in range(1, len(ultimas_amostras))]

    media_amplitudes = sum(amplitudes) / len(amplitudes)

    d2 = 1.128
    lcs = media + 3 * media_amplitudes / d2
    lci = media - 3 * media_amplitudes / d2

    return lci <= novo_valor <= lcs


def get_historico_componente(componente):
    """Busca histórico de valores para um componente específico"""
    db = get_db()
    historico = db.execute('''
        SELECT valor FROM historico_componentes
        WHERE componente = ?
        ORDER BY data_coleta ASC
    ''', (componente,)).fetchall()
    return [row[0] for row in historico]


def calcular_propriedades_fluido(componentes_data):
    """Calcula propriedades do fluido baseado na composição dos componentes"""
    propriedades = {}

    # Massas molares dos componentes (g/mol)
    massas_molares = {
        'Metano': 16.043, 'Etano': 30.070, 'Propano': 44.097,
        'i-Butano': 58.123, 'n-Butano': 58.123, 'i-Pentano': 72.150,
        'n-Pentano': 72.150, 'Hexano': 86.177, 'Heptano': 100.204,
        'Octano': 114.231, 'Nonano': 128.258, 'Decano': 142.285,
        'Oxigênio': 31.998, 'Nitrogênio': 28.014, 'CO2': 44.010
    }

    # Cálculo da Massa Molecular
    massa_molecular = 0.0
    total_percentual = 0.0

    for comp_nome, percentual in componentes_data.items():
        if comp_nome in massas_molares:
            massa_molecular += (percentual / 100.0) * massas_molares[comp_nome]
            total_percentual += percentual

    propriedades['Massa Molecular'] = massa_molecular

    # Cálculo simplificado do Fator de Compressibilidade (Z)
    # Baseado na composição do gás (valores típicos para gás natural)
    metano_perc = componentes_data.get('Metano', 0) / 100.0
    co2_perc = componentes_data.get('CO2', 0) / 100.0
    n2_perc = componentes_data.get('Nitrogênio', 0) / 100.0

    # Fator Z simplificado para condições padrão (15°C, 1 atm)
    z_base = 0.998  # Fator base para gás ideal
    z_correcao = -0.001 * co2_perc - 0.0005 * n2_perc + 0.0002 * metano_perc

    propriedades['Fator de Compressibilidade'] = z_base + z_correcao

    # Cálculo da Massa Específica (kg/m³ a 20°C, 101.325 kPa)
    # ρ = (P × M) / (Z × R × T)
    P = 101325  # Pa
    R = 8314.47  # J/(kmol·K)
    T = 293.15  # K (20°C)

    massa_especifica = (P * massa_molecular) / (propriedades['Fator de Compressibilidade'] * R * T)

    propriedades['Massa Específica'] = massa_especifica

    return propriedades


def get_historico_propriedade(propriedade_nome):
    """Busca histórico de valores para uma propriedade específica"""
    db = get_db()
    historico = db.execute('''
        SELECT valor FROM historico_propriedades
        WHERE propriedade = ?
        ORDER BY data_coleta ASC
    ''', (propriedade_nome,)).fetchall()

    return [row[0] for row in historico]


def valida_cep_propriedade(propriedade_nome, novo_valor):
    """Valida propriedade usando Controle Estatístico de Processo"""
    historico = get_historico_propriedade(propriedade_nome)

    if len(historico) < 2:
        return True  # Aceita se não há histórico suficiente

    # Usar apenas as últimas 8 amostras para CEP
    ultimas_amostras = historico[-8:] if len(historico) >= 8 else historico

    if len(ultimas_amostras) < 2:
        return True

    media = sum(ultimas_amostras) / len(ultimas_amostras)

    # Cálculo dos limites de controle usando amplitude móvel
    amplitudes = [abs(ultimas_amostras[i] - ultimas_amostras[i - 1])
                  for i in range(1, len(ultimas_amostras))]

    if not amplitudes:
        return True

    media_amplitudes = sum(amplitudes) / len(amplitudes)

    # Constante d2 para n=2 (amplitude móvel)
    d2 = 1.128

    # Limites de controle (3 sigma)
    lcs = media + 3 * media_amplitudes / d2
    lci = media - 3 * media_amplitudes / d2

    return lci <= novo_valor <= lcs


def criar_checklist_padrao(boletin_id):
    """Cria checklist padrão para um boletim"""
    itens_checklist = [
        "Identificação do boletim de resultados analíticos",
        "Identificação da amostra",
        "Descrição da data de amostragem",
        "Descrição da data de recebimento da amostra pelo laboratório",
        "Descrição da data de realização das análises",
        "Descrição da data de emissão do BRA",
        "Identificação do campo produtor ou da instalação",
        "Identificação do agente regulado",
        "Identificação do ponto de medição e/ou do poço quando aplicável",
        "Resultados das análises e normas ou procedimentos utilizados",
        "Descrição das características do processo do ponto de amostragem do fluido (pressão e temperatura)",
        "Identificação do responsável pela amostragem",
        "Indicação dos incertezas de medição, com descrição do nível de confiança e fator de abrangência",
        "Identificação dos responsáveis técnicos pela realização da análise",
        "Identificação dos responsáveis pela elaboração e aprovação do boletim"
    ]

    db = get_db()
    for i, descricao in enumerate(itens_checklist, 1):
        db.execute('''
            INSERT INTO checklist_itens (boletin_id, item_numero, descricao, situacao)
            VALUES (?, ?, ?, ?)
        ''', (boletin_id, i, descricao, 'OK'))
    db.commit()


def gerar_pdf_relatorio(boletim_id):
    """Gera PDF do relatório de validação"""
    db = get_db()

    # Buscar dados do boletim
    boletim = db.execute('SELECT * FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
    if not boletim:
        return None

    componentes = db.execute('SELECT * FROM componentes WHERE boletin_id = ?', (boletim_id,)).fetchall()
    propriedades = db.execute('SELECT * FROM propriedades WHERE boletin_id = ?', (boletim_id,)).fetchall()
    checklist = db.execute(
        'SELECT * FROM checklist_itens WHERE boletin_id = ? ORDER BY item_numero',
        (boletim_id,
         )).fetchall()

    # Criar PDF em memória
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)

    # Estilos
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle('CustomTitle', parent=styles['Title'],
                                  fontSize=16, spaceAfter=20, alignment=TA_CENTER,
                                  textColor=colors.HexColor('#1e40af'))

    secao_style = ParagraphStyle('Section', parent=styles['Heading2'],
                                 fontSize=12, spaceAfter=10,
                                 textColor=colors.HexColor('#1e40af'))

    normal_style = styles['Normal']

    # Conteúdo do PDF
    story = []

    # Cabeçalho BRAVA
    titulo = Paragraph("BRAVA ENERGIA",
                       ParagraphStyle('Logo', fontSize=20, textColor=colors.HexColor('#fbbf24'),
                                      alignment=TA_CENTER, spaceAfter=10))
    story.append(titulo)

    subtitulo = Paragraph("RELATÓRIO DE VALIDAÇÃO DE BOLETIM DE ANÁLISES QUÍMICAS", titulo_style)
    story.append(subtitulo)

    # Informações do Boletim
    story.append(Spacer(1, 20))
    story.append(Paragraph("1) INFORMAÇÕES DO BOLETIM", secao_style))

    info_data = [
        ['Nº Boletim:', boletim['numero_boletim'], 'Nº Documento:', boletim['numero_documento'] or ''],
        ['Data Coleta:', boletim['data_coleta'], 'Data Validação:', boletim['data_validacao'] or ''],
        ['Data Emissão:', boletim['data_emissao'], 'Plataforma:', boletim['plataforma'] or ''],
        ['Sistema Medição:', boletim['sistema_medicao'] or '', 'Classificação:', boletim['classificacao'] or ''],
        ['Agente Regulado:', boletim['agente_regulado'], 'Ponto Medição:', boletim['ponto_medicao']],
        ['Responsável:', boletim['responsavel_amostragem'], 'Pressão:',
         f"{boletim['pressao']} atm" if boletim['pressao'] else ''],
        ['Temperatura:', f"{boletim['temperatura']} °C" if boletim['temperatura'] else '', '', '']
    ]

    info_table = Table(info_data, colWidths=[100, 150, 100, 150])
    info_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
    ]))
    story.append(info_table)

    # Checklist
    story.append(Spacer(1, 20))
    story.append(Paragraph("2) CHECK LIST", secao_style))

    checklist_data = [['Item', 'Descrição', 'Status']]
    for item in checklist:
        checklist_data.append([
            str(item['item_numero']),
            item['descricao'][:60] + '...' if len(item['descricao']) > 60 else item['descricao'],
            '✓' if item['situacao'] == 'OK' else '✗'
        ])

    checklist_table = Table(checklist_data, colWidths=[30, 350, 50])
    checklist_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
    ]))
    story.append(checklist_table)

    # Análise CEP - Componentes
    story.append(Spacer(1, 20))
    story.append(Paragraph("3) ANÁLISE CEP - COMPONENTES", secao_style))

    comp_data = [['Componente', '% Molar', 'A.G.A #8', 'CEP', 'Limite A.G.A Min', 'Limite A.G.A Max']]
    for comp in componentes:
        comp_data.append([
            comp['nome'],
            f"{comp['percentual_molar']:.3f}%",
            comp['status_aga'],
            comp['status_cep'],
            '0%' if comp['nome'] != 'Propano' else '0%',  # Simplificado
            '100%' if comp['nome'] not in [
                'Propano',
                'i-Butano',
                'n-Butano',
                'i-Pentano',
                'n-Pentano',
                'Oxigênio'] else (
                '12%' if comp['nome'] == 'Propano' else (
                    '6%' if 'Butano' in comp['nome'] else (
                        '4%' if 'Pentano' in comp['nome'] else '21%')))
        ])

    comp_table = Table(comp_data, colWidths=[80, 60, 60, 60, 60, 60])
    comp_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(comp_table)

    # Propriedades
    story.append(Spacer(1, 15))
    story.append(Paragraph("PROPRIEDADES DO FLUIDO", secao_style))

    prop_data = [['Propriedade', 'Valor', 'Status A.G.A #8', 'Status CEP']]
    for prop in propriedades:
        prop_data.append([
            prop['nome'],
            f"{prop['valor']:.4f}",
            prop['status_aga'],
            prop['status_cep']
        ])

    prop_table = Table(prop_data, colWidths=[200, 80, 80, 80])
    prop_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(prop_table)

    # Resultado Final
    story.append(Spacer(1, 20))
    story.append(Paragraph("RESULTADO DA VALIDAÇÃO", secao_style))

    resultado_data = [['CEP', 'A.G.A #8', 'CHECKLIST'],
                      [boletim['status_cep'] or 'PENDENTE',
                       boletim['status_aga8'] or 'PENDENTE',
                       boletim['status_checklist'] or 'PENDENTE']]

    resultado_table = Table(resultado_data, colWidths=[150, 150, 150])
    resultado_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 2, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(resultado_table)

    # Observações
    if boletim['observacoes']:
        story.append(Spacer(1, 20))
        story.append(Paragraph("4) OBSERVAÇÕES", secao_style))
        story.append(Paragraph(boletim['observacoes'], normal_style))

    # Responsáveis
    story.append(Spacer(1, 30))
    story.append(Paragraph("RESPONSÁVEIS PELA VALIDAÇÃO", secao_style))

    resp_data = [
        ['Responsável Técnico', 'Responsável Elaboração', 'Responsável Aprovação'],
        [boletim['responsavel_tecnico'], boletim['responsavel_elaboracao'], boletim['responsavel_aprovacao']],
        ['_' * 20, '_' * 20, '_' * 20],
        ['Assinatura', 'Assinatura', 'Assinatura']
    ]

    resp_table = Table(resp_data, colWidths=[150, 150, 150])
    resp_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 2), (-1, 2), 1, colors.black),
    ]))
    story.append(resp_table)

    # Gerar PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# Rotas da aplicação


@app.route('/favicon.ico')
def favicon():
    """Serve a simple favicon"""
    # Create a minimal ICO response to prevent 404 errors
    ico_header = b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
    ico_header += b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00\x08'
    ico_header += b'\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ico_header += b'\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00'
    ico_data = ico_header + b'\x00' * 320 + b'\x00' * 64

    response = app.response_class(
        ico_data,
        mimetype='image/x-icon',
        headers={'Cache-Control': 'public, max-age=86400'}  # Cache for 1 day
    )
    return response


@app.route('/')
def index():
    """Redireciona para o dashboard"""
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    """Página principal com estatísticas e gráficos"""
    db = get_db()

    # Parâmetros de filtro
    periodo = request.args.get('periodo', '')
    status_filter = request.args.get('status_filter', '')
    componente_filter = request.args.get('componente_filter', '')

    # Construir condições WHERE para filtros
    where_conditions = []
    params = []

    if periodo:
        days = int(periodo)
        where_conditions.append("DATE(b.data_coleta) >= DATE('now', '-' || ? || ' days')")
        params.append(days)

    if status_filter:
        where_conditions.append("b.status = ?")
        params.append(status_filter)

    where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""

    # Estatísticas gerais (com filtros aplicados)
    stats = {}
    base_query = f"SELECT COUNT(*) FROM boletins b {where_clause}"
    stats['total_boletins'] = db.execute(base_query, params).fetchone()[0]

    # Estatísticas de validação (com filtros)
    if where_clause:
        validados_query = f"SELECT COUNT(*) FROM boletins b {where_clause} AND b.status = 'VALIDADO'"
        invalidados_query = f"SELECT COUNT(*) FROM boletins b {where_clause} AND b.status = 'INVALIDADO'"
        aga8_query = f"SELECT COUNT(*) FROM boletins b {where_clause} AND b.status_aga8 = 'VALIDADO'"
        cep_query = f"SELECT COUNT(*) FROM boletins b {where_clause} AND b.status_cep = 'VALIDADO'"
        checklist_query = f"SELECT COUNT(*) FROM boletins b {where_clause} AND b.status_checklist = 'VALIDADO'"

        stats['boletins_validados'] = db.execute(validados_query, params + ['VALIDADO']).fetchone()[0]
        stats['boletins_invalidados'] = db.execute(invalidados_query, params + ['INVALIDADO']).fetchone()[0]
        stats['aga8_aprovados'] = db.execute(aga8_query, params + ['VALIDADO']).fetchone()[0]
        stats['cep_aprovados'] = db.execute(cep_query, params + ['VALIDADO']).fetchone()[0]
        stats['checklist_aprovados'] = db.execute(checklist_query, params + ['VALIDADO']).fetchone()[0]
    else:
        stats['boletins_validados'] = db.execute(
            'SELECT COUNT(*) FROM boletins WHERE status = ?', ('VALIDADO',)).fetchone()[0]
        stats['boletins_invalidados'] = db.execute(
            'SELECT COUNT(*) FROM boletins WHERE status = ?', ('INVALIDADO',)).fetchone()[0]
        stats['aga8_aprovados'] = db.execute(
            'SELECT COUNT(*) FROM boletins WHERE status_aga8 = ?', ('VALIDADO',)).fetchone()[0]
        stats['cep_aprovados'] = db.execute(
            'SELECT COUNT(*) FROM boletins WHERE status_cep = ?', ('VALIDADO',)).fetchone()[0]
        stats['checklist_aprovados'] = db.execute(
            'SELECT COUNT(*) FROM boletins WHERE status_checklist = ?', ('VALIDADO',)).fetchone()[0]

    stats['taxa_validacao'] = (
        stats['boletins_validados'] /
        stats['total_boletins'] *
        100) if stats['total_boletins'] > 0 else 0

    # Últimos boletins (com filtros aplicados)
    boletins_query = f'''
        SELECT b.id, b.numero_boletim, b.identificacao_instalacao, b.data_coleta,
               b.data_validacao, b.status, b.status_aga8, b.status_cep, b.status_checklist
        FROM boletins b
        {where_clause}
        ORDER BY b.data_coleta DESC
        LIMIT 10
    '''
    boletins_recentes = db.execute(boletins_query, params).fetchall()

    # Componentes com mais problemas CEP (com filtros de componente se aplicável)
    comp_where = []
    comp_params = []

    if componente_filter:
        comp_where.append("c.nome = ?")
        comp_params.append(componente_filter)

    if periodo:
        comp_where.append("DATE(b.data_coleta) >= DATE('now', '-' || ? || ' days')")
        comp_params.append(int(periodo))

    comp_where_clause = "WHERE " + " AND ".join(comp_where) if comp_where else ""

    componentes_query = f'''
        SELECT c.nome,
               COUNT(*) as total,
               SUM(CASE WHEN c.status_cep = "INVALIDADO" THEN 1 ELSE 0 END) as invalidados,
               ROUND(SUM(CASE WHEN c.status_cep = "INVALIDADO" THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 2) as taxa_erro
        FROM componentes c
        JOIN boletins b ON c.boletin_id = b.id
        {comp_where_clause}
        GROUP BY c.nome
        HAVING total > 0
        ORDER BY taxa_erro DESC, total DESC
        LIMIT 10
    '''
    componentes_problemas = db.execute(componentes_query, comp_params).fetchall()

    # Histórico recente para gráfico (com filtros aplicados)
    hist_where = ["hc.componente IN ('Metano', 'Etano', 'Propano', 'Nitrogênio', 'CO2')"]
    hist_params = []

    if componente_filter:
        hist_where = [f"hc.componente = '{componente_filter}'"]

    if periodo:
        hist_where.append("DATE(hc.data_coleta) >= DATE('now', '-' || ? || ' days')")
        hist_params.append(int(periodo))

    hist_query = f'''
        SELECT hc.componente, b.numero_boletim, hc.data_coleta, hc.valor, c.status_aga, c.status_cep
        FROM historico_componentes hc
        JOIN boletins b ON hc.boletin_id = b.id
        JOIN componentes c ON hc.componente = c.nome AND hc.boletin_id = c.boletin_id
        WHERE {" AND ".join(hist_where)}
        ORDER BY hc.data_coleta DESC, hc.componente
        LIMIT 50
    '''
    historico_grafico_rows = db.execute(hist_query, hist_params).fetchall()

    # Converter Row objects para dicionários para JSON serialization
    historico_grafico = []
    for row in historico_grafico_rows:
        historico_grafico.append({
            'componente': row['componente'],
            'numero_boletim': row['numero_boletim'],
            'data_coleta': row['data_coleta'],
            'valor': row['valor'],
            'status_aga': row['status_aga'],
            'status_cep': row['status_cep']
        })

    return render_template('dashboard.html',
                           stats=stats,
                           boletins_recentes=boletins_recentes,
                           componentes_problemas=componentes_problemas,
                           historico_grafico=historico_grafico)


@app.route('/boletins')
def listar_boletins():
    """Página para listar, filtrar e visualizar todos os boletins cadastrados"""
    db = get_db()
    boletins = db.execute('''
        SELECT b.id, b.numero_boletim, b.identificacao_instalacao, b.data_coleta, b.data_validacao, b.status
        FROM boletins b
        ORDER BY b.data_coleta DESC
    ''').fetchall()

    historico = db.execute('''
        SELECT hc.componente, b.numero_boletim, hc.data_coleta, hc.valor, c.status_aga, c.status_cep
        FROM historico_componentes hc
        JOIN boletins b ON hc.boletin_id = b.id
        JOIN componentes c ON hc.componente = c.nome AND hc.boletin_id = c.boletin_id
        ORDER BY hc.data_coleta DESC, hc.componente
    ''').fetchall()

    return render_template('main.html', boletins=boletins, historico=historico)


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    """Página para cadastrar novos boletins de cromatografia"""
    if request.method == 'POST':
        # Capturar dados do formulário
        dados_boletim = {
            'numero_boletim': request.form['numero_boletim'],
            'data_coleta': request.form['data_coleta'],
            'data_recebimento': request.form['data_recebimento'],
            'data_analise': request.form['data_analise'],
            'data_emissao': request.form['data_emissao'],
            'identificacao_instalacao': request.form['identificacao_instalacao'],
            'agente_regulado': request.form['agente_regulado'],
            'ponto_medicao': request.form['ponto_medicao'],
            'responsavel_amostragem': request.form['responsavel_amostragem'],
            'pressao': float(request.form['pressao']),
            'temperatura': float(request.form['temperatura']),
            'observacoes': request.form['observacoes'],
            'responsavel_tecnico': request.form['responsavel_tecnico'],
            'responsavel_elaboracao': request.form['responsavel_elaboracao'],
            'responsavel_aprovacao': request.form['responsavel_aprovacao']
        }

        # Adicionar novos campos do Figma
        dados_boletim.update({
            'numero_documento': f"{dados_boletim['numero_boletim']}/2025",
            'plataforma': request.form.get('plataforma', 'FPSO ATLANTE'),
            'sistema_medicao': request.form.get('sistema_medicao', 'GÁS COMBUSTÍVEL LP'),
            'classificacao': request.form.get('classificacao', 'FISCAL'),
            'ponto_coleta': request.form.get('ponto_coleta', 'LP FUEL GAS')
        })

        # Inserir boletim no banco com novos campos
        db = get_db()
        db.execute('''
            INSERT INTO boletins (
                numero_boletim, numero_documento, data_coleta, data_recebimento, data_analise, data_emissao,
                identificacao_instalacao, plataforma, sistema_medicao, classificacao,
                ponto_medicao, ponto_coleta, agente_regulado, responsavel_amostragem,
                pressao, temperatura, observacoes, responsavel_tecnico, responsavel_elaboracao,
                responsavel_aprovacao, data_validacao, status, status_cep, status_aga8, status_checklist
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dados_boletim['numero_boletim'], dados_boletim['numero_documento'],
            dados_boletim['data_coleta'], dados_boletim['data_recebimento'],
            dados_boletim['data_analise'], dados_boletim['data_emissao'],
            dados_boletim['identificacao_instalacao'], dados_boletim['plataforma'],
            dados_boletim['sistema_medicao'], dados_boletim['classificacao'],
            dados_boletim['ponto_medicao'], dados_boletim['ponto_coleta'],
            dados_boletim['agente_regulado'], dados_boletim['responsavel_amostragem'],
            dados_boletim['pressao'], dados_boletim['temperatura'], dados_boletim['observacoes'],
            dados_boletim['responsavel_tecnico'], dados_boletim['responsavel_elaboracao'],
            dados_boletim['responsavel_aprovacao'], None, None, None, None, None
        ))
        boletim_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        db.commit()

        # Inserir componentes
        componentes = [
            'Metano', 'Etano', 'Propano', 'i-Butano', 'n-Butano',
            'i-Pentano', 'n-Pentano', 'Hexano', 'Heptano', 'Octano',
            'Nonano', 'Decano', 'Oxigênio', 'Nitrogênio', 'CO2'
        ]

        componentes_data = {}
        for comp in componentes:
            valor = float(request.form[comp])
            componentes_data[comp] = valor
            status_aga = "VALIDADO" if valida_aga8(comp, valor) else "INVALIDADO"
            historico = get_historico_componente(comp)
            status_cep = "VALIDADO" if valida_cep(comp, valor, historico) else "INVALIDADO"

            db.execute('''
                INSERT INTO componentes (boletin_id, nome, percentual_molar, status_aga, status_cep)
                VALUES (?, ?, ?, ?, ?)
            ''', (boletim_id, comp, valor, status_aga, status_cep))

            db.execute('''
                INSERT INTO historico_componentes (componente, boletin_id, valor, data_coleta)
                VALUES (?, ?, ?, ?)
            ''', (comp, boletim_id, valor, dados_boletim['data_coleta']))

        # Calcular propriedades automaticamente
        propriedades_calculadas = calcular_propriedades_fluido(componentes_data)

        # Inserir propriedades calculadas
        for nome_prop, valor_calculado in propriedades_calculadas.items():
            # Validação CEP para propriedades
            status_cep_prop = "VALIDADO" if valida_cep_propriedade(nome_prop, valor_calculado) else "INVALIDADO"

            db.execute('''
                INSERT INTO propriedades (boletin_id, nome, valor, status_aga, status_cep)
                VALUES (?, ?, ?, ?, ?)
            ''', (boletim_id, nome_prop, valor_calculado, "N/A", status_cep_prop))

            # Salvar no histórico de propriedades
            db.execute('''
                INSERT INTO historico_propriedades (propriedade, boletin_id, valor, data_coleta)
                VALUES (?, ?, ?, ?)
            ''', (nome_prop, boletim_id, valor_calculado, dados_boletim['data_coleta']))

        # Manter propriedades do formulário para compatibilidade (se existirem)
        propriedades_form = []
        if 'fator_compressibilidade' in request.form:
            propriedades_form = [
                ('Fator de Compressibilidade', float(request.form['fator_compressibilidade'])),
                ('Massa Específica', float(request.form['massa_especifica'])),
                ('Massa Molecular', float(request.form['massa_molecular']))
            ]

        for nome, valor in propriedades_form:
            status_aga = "VALIDADO"
            status_cep = "VALIDADO"

            db.execute('''
                INSERT INTO propriedades (boletin_id, nome, valor, status_aga, status_cep)
                VALUES (?, ?, ?, ?, ?)
            ''', (boletim_id, nome, valor, status_aga, status_cep))

        db.commit()

        # Criar checklist automático
        criar_checklist_padrao(boletim_id)

        # Verificar status separados (Figma pattern)
        # Status A.G.A #8
        componentes_aga_invalidos = db.execute('''
            SELECT COUNT(*) FROM componentes
            WHERE boletin_id = ? AND status_aga = ?
        ''', (boletim_id, 'INVALIDADO')).fetchone()[0]
        status_aga8 = "INVALIDADO" if componentes_aga_invalidos > 0 else "VALIDADO"

        # Status CEP
        componentes_cep_invalidos = db.execute('''
            SELECT COUNT(*) FROM componentes
            WHERE boletin_id = ? AND status_cep = ?
        ''', (boletim_id, 'INVALIDADO')).fetchone()[0]
        status_cep = "INVALIDADO" if componentes_cep_invalidos > 0 else "VALIDADO"

        # Status Checklist (sempre VALIDADO por enquanto)
        status_checklist = "VALIDADO"

        # Status Geral
        status = "INVALIDADO" if (status_aga8 == "INVALIDADO" or status_cep == "INVALIDADO") else "VALIDADO"
        data_validacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db.execute('''
            UPDATE boletins SET status = ?, status_cep = ?, status_aga8 = ?,
                               status_checklist = ?, data_validacao = ? WHERE id = ?
        ''', (status, status_cep, status_aga8, status_checklist, data_validacao, boletim_id))
        db.commit()

        flash('Boletim cadastrado com sucesso!')
        return redirect(url_for('relatorio', boletim_id=boletim_id))

    return render_template('cadastrar.html')


@app.route('/relatorio/<int:boletim_id>')
def relatorio(boletim_id):
    """Exibe o relatório detalhado de um boletim específico"""
    db = get_db()
    boletim = db.execute('SELECT * FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
    if boletim is None:
        flash('Boletim não encontrado!')
        return redirect(url_for('listar_boletins'))

    componentes = db.execute('''
        SELECT * FROM componentes WHERE boletin_id = ?
    ''', (boletim_id,)).fetchall()

    propriedades = db.execute('''
        SELECT * FROM propriedades WHERE boletin_id = ?
    ''', (boletim_id,)).fetchall()

    return render_template('relatorio_excel.html', boletim=boletim, componentes=componentes, propriedades=propriedades)


@app.route('/revalidar/<int:boletim_id>', methods=['POST'])
def revalidar_boletim(boletim_id):
    """Revalida um boletim existente aplicando as regras A.G.A #8 e CEP"""
    db = get_db()

    # Verificar se o boletim existe
    boletim = db.execute('SELECT * FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
    if boletim is None:
        flash('Boletim não encontrado!')
        return redirect(url_for('listar_boletins'))

    # Buscar todos os componentes do boletim
    componentes = db.execute('''
        SELECT * FROM componentes WHERE boletin_id = ?
    ''', (boletim_id,)).fetchall()

    # Revalidar cada componente
    for componente in componentes:
        # Validação A.G.A #8
        status_aga = "VALIDADO" if valida_aga8(componente['nome'], componente['percentual_molar']) else "INVALIDADO"

        # Validação CEP
        historico = get_historico_componente(componente['nome'])
        status_cep = "VALIDADO" if valida_cep(
            componente['nome'],
            componente['percentual_molar'],
            historico) else "INVALIDADO"

        # Atualizar status do componente
        db.execute('''
            UPDATE componentes SET status_aga = ?, status_cep = ?
            WHERE id = ?
        ''', (status_aga, status_cep, componente['id']))

    # Recalcular status geral do boletim
    componentes_aga_invalidos = db.execute('''
        SELECT COUNT(*) FROM componentes
        WHERE boletin_id = ? AND status_aga = ?
    ''', (boletim_id, 'INVALIDADO')).fetchone()[0]
    status_aga8 = "INVALIDADO" if componentes_aga_invalidos > 0 else "VALIDADO"

    componentes_cep_invalidos = db.execute('''
        SELECT COUNT(*) FROM componentes
        WHERE boletin_id = ? AND status_cep = ?
    ''', (boletim_id, 'INVALIDADO')).fetchone()[0]
    status_cep = "INVALIDADO" if componentes_cep_invalidos > 0 else "VALIDADO"

    # Status Checklist (sempre VALIDADO por enquanto)
    status_checklist = "VALIDADO"

    # Status Geral
    status = "INVALIDADO" if (status_aga8 == "INVALIDADO" or status_cep == "INVALIDADO") else "VALIDADO"
    data_validacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Atualizar o boletim
    db.execute('''
        UPDATE boletins SET status = ?, status_cep = ?, status_aga8 = ?,
                           status_checklist = ?, data_validacao = ? WHERE id = ?
    ''', (status, status_cep, status_aga8, status_checklist, data_validacao, boletim_id))

    db.commit()

    flash(f'Boletim revalidado com sucesso! Status: {status}')
    return redirect(url_for('relatorio', boletim_id=boletim_id))


@app.route('/revalidar_todos', methods=['POST'])
def revalidar_todos_boletins():
    """Revalida todos os boletins pendentes no sistema"""
    db = get_db()

    # Buscar todos os boletins com status pendente ou nulo
    boletins_pendentes = db.execute('''
        SELECT id FROM boletins
        WHERE status IS NULL OR status = 'PENDENTE' OR status = ''
    ''').fetchall()

    contador_validados = 0
    contador_invalidados = 0

    for boletim in boletins_pendentes:
        boletim_id = boletim['id']

        # Buscar todos os componentes do boletim
        componentes = db.execute('''
            SELECT * FROM componentes WHERE boletin_id = ?
        ''', (boletim_id,)).fetchall()

        # Revalidar cada componente
        for componente in componentes:
            # Validação A.G.A #8
            status_aga = "VALIDADO" if valida_aga8(componente['nome'], componente['percentual_molar']) else "INVALIDADO"

            # Validação CEP
            historico = get_historico_componente(componente['nome'])
            status_cep = "VALIDADO" if valida_cep(
                componente['nome'],
                componente['percentual_molar'],
                historico) else "INVALIDADO"

            # Atualizar status do componente
            db.execute('''
                UPDATE componentes SET status_aga = ?, status_cep = ?
                WHERE id = ?
            ''', (status_aga, status_cep, componente['id']))

        # Recalcular status geral do boletim
        componentes_aga_invalidos = db.execute('''
            SELECT COUNT(*) FROM componentes
            WHERE boletin_id = ? AND status_aga = ?
        ''', (boletim_id, 'INVALIDADO')).fetchone()[0]
        status_aga8 = "INVALIDADO" if componentes_aga_invalidos > 0 else "VALIDADO"

        componentes_cep_invalidos = db.execute('''
            SELECT COUNT(*) FROM componentes
            WHERE boletin_id = ? AND status_cep = ?
        ''', (boletim_id, 'INVALIDADO')).fetchone()[0]
        status_cep = "INVALIDADO" if componentes_cep_invalidos > 0 else "VALIDADO"

        # Status Checklist (sempre VALIDADO por enquanto)
        status_checklist = "VALIDADO"

        # Status Geral
        status = "INVALIDADO" if (status_aga8 == "INVALIDADO" or status_cep == "INVALIDADO") else "VALIDADO"
        data_validacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Atualizar o boletim
        db.execute('''
            UPDATE boletins SET status = ?, status_cep = ?, status_aga8 = ?,
                               status_checklist = ?, data_validacao = ? WHERE id = ?
        ''', (status, status_cep, status_aga8, status_checklist, data_validacao, boletim_id))

        if status == "VALIDADO":
            contador_validados += 1
        else:
            contador_invalidados += 1

    db.commit()

    total_processados = len(boletins_pendentes)
    flash(f'Processados {total_processados} boletins: {contador_validados} validados, '
          f'{contador_invalidados} invalidados')
    return redirect(url_for('listar_boletins'))


@app.route('/relatorio/<int:boletim_id>/pdf')
def relatorio_pdf(boletim_id):
    """Gera e retorna PDF do relatório"""
    try:
        pdf_buffer = gerar_pdf_relatorio(boletim_id)
        if pdf_buffer is None:
            flash('Boletim não encontrado!')
            return redirect(url_for('dashboard'))

        # Buscar nome do boletim para o arquivo
        db = get_db()
        boletim = db.execute('SELECT numero_boletim FROM boletins WHERE id = ?',
                             (boletim_id,)).fetchone()
        if boletim:
            filename = f"Boletim_{boletim['numero_boletim'].replace('/', '_')}.pdf"
        else:
            filename = f"Boletim_{boletim_id}.pdf"

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Erro ao gerar PDF: {str(e)}')
        return redirect(url_for('relatorio', boletim_id=boletim_id))


# Configuração para upload de arquivos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max


@app.route('/importar_excel')
def importar_excel():
    """Página de importação de arquivos Excel"""
    return render_template('importar_excel.html')


@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    """Processa upload e importação de arquivo Excel"""
    if 'arquivo' not in request.files:
        flash('Nenhum arquivo foi selecionado!')
        return redirect(request.url)

    arquivo = request.files['arquivo']

    if arquivo.filename == '':
        flash('Nenhum arquivo foi selecionado!')
        return redirect(request.url)

    if arquivo and allowed_file(arquivo.filename):
        try:
            filename = secure_filename(arquivo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            arquivo.save(filepath)

            # Processar arquivo Excel
            resultado = processar_excel_boletins(filepath)

            # Limpar arquivo temporário
            os.remove(filepath)

            # Mostrar resultados
            if resultado['success'] > 0:
                flash(f'✅ Importação concluída: {resultado["success"]} boletins '
                      f'processados com sucesso!')

                for boletim in resultado['boletins_processados']:
                    flash(f'📋 Boletim {boletim["numero_boletim"]}: {boletim["status"]} '
                          f'({boletim["componentes_processados"]} componentes)')

            if resultado['errors']:
                for erro in resultado['errors']:
                    flash(f'❌ {erro}', 'error')

            return redirect(url_for('listar_boletins'))

        except Exception as e:
            flash(f'Erro ao processar arquivo: {str(e)}', 'error')
            return redirect(url_for('importar_excel'))
    else:
        flash('Tipo de arquivo não suportado! Use .xlsx, .xls ou .csv', 'error')
        return redirect(url_for('importar_excel'))


@app.route('/download_template')
def download_template():
    """Download do template Excel para importação"""
    try:
        template_path = criar_template_excel()

        return send_file(
            template_path,
            as_attachment=True,
            download_name='Template_Importacao_Boletins.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        flash(f'Erro ao gerar template: {str(e)}')
        return redirect(url_for('importar_excel'))


@app.route('/processar_boletins_existentes')
def processar_boletins_existentes():
    """Processa boletins existentes que não têm componentes"""
    try:
        db = get_db()

        # Buscar boletins sem componentes
        boletins = db.execute('''
            SELECT * FROM boletins
            WHERE id NOT IN (SELECT DISTINCT boletin_id FROM componentes WHERE boletin_id IS NOT NULL)
            OR status IS NULL
        ''').fetchall()

        contador = 0
        for boletim in boletins:
            # Para boletins existentes sem dados de componentes,
            # vamos criar componentes com valores zerados e status PENDENTE
            componentes = [
                'Metano', 'Etano', 'Propano', 'i-Butano', 'n-Butano',
                'i-Pentano', 'n-Pentano', 'Hexano', 'Heptano', 'Octano',
                'Nonano', 'Decano', 'Oxigênio', 'Nitrogênio', 'CO2'
            ]

            for componente in componentes:
                # Verificar se componente já existe
                existe = db.execute('''
                    SELECT id FROM componentes
                    WHERE boletin_id = ? AND nome = ?
                ''', (boletim['id'], componente)).fetchone()

                if not existe:
                    db.execute('''
                        INSERT INTO componentes (boletin_id, nome, percentual_molar, status_aga, status_cep)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (boletim['id'], componente, 0.0, 'PENDENTE', 'PENDENTE'))

                    # Adicionar ao histórico
                    db.execute('''
                        INSERT INTO historico_componentes (componente, boletin_id, valor, data_coleta)
                        VALUES (?, ?, ?, ?)
                    ''', (componente, boletim['id'], 0.0, boletim['data_coleta']))

            # Atualizar status do boletim
            db.execute('''
                UPDATE boletins SET status = ? WHERE id = ?
            ''', ('PENDENTE', boletim['id']))

            contador += 1

        db.commit()
        flash(f'✅ Processados {contador} boletins existentes. Agora eles aparecem '
              f'na aba Histórico e podem ser revalidados.')

    except Exception as e:
        flash(f'Erro ao processar boletins existentes: {str(e)}', 'error')

    return redirect(url_for('listar_boletins'))


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
