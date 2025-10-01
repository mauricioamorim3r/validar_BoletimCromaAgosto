# -*- coding: utf-8 -*-
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_file
)
import sqlite3
from datetime import datetime
import os
import io
import sys
import logging
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle
)
from reportlab.lib.enums import TA_CENTER
from config import DEBUG, HOST, PORT
from excel_import import (
    processar_excel_boletins,
    criar_template_excel,
    allowed_file
)
from validacao_prazos_anp import (
    validar_todos_prazos_anp,
    gerar_classe_css_prazo,
    gerar_badge_prazo
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Starting Flask application - Sistema de Validação de Boletins")

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    os.system('chcp 65001 > nul')

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_flask'


# Filtros personalizados para formatação
def date_format(date_string):
    """Formata data de YYYY-MM-DD para DD/MM/AA"""
    if not date_string:
        return ''
    try:
        # Se a string já estiver no formato DD/MM/YY, retorna como está
        if '/' in date_string and len(date_string.split('/')[2]) == 2:
            return date_string

        # Converte de YYYY-MM-DD para DD/MM/AA
        if isinstance(date_string, str) and len(date_string) >= 10:
            date_obj = datetime.strptime(date_string[:10], '%Y-%m-%d')
            return date_obj.strftime('%d/%m/%y')
        return date_string
    except (ValueError, AttributeError):
        return date_string


def number_format(value, decimals=2):
    """
    Formata números com vírgula como separador de milhares e ponto para
    decimais
    """
    if value is None or value == '':
        return ''
    try:
        # Converte para float se necessário
        if isinstance(value, str):
            # Remove possíveis caracteres não numéricos exceto ponto e vírgula
            value = value.replace(',', '.').strip()
            if not value or value == '-':
                return value
            value = float(value)
        elif not isinstance(value, (int, float)):
            return str(value)

        # Formata com o número de casas decimais especificado
        formatted = f"{value:,.{decimals}f}"

        # Substitui ponto por vírgula para separador decimal (padrão brasileiro)
        # e vírgula por ponto para separador de milhares
        parts = formatted.split('.')
        if len(parts) == 2:
            integer_part = parts[0].replace(',', '.')  # Separador de milhares
            decimal_part = parts[1]
            # Separador decimal brasileiro
            return f"{integer_part},{decimal_part}"
        else:
            return parts[0].replace(',', '.')  # Apenas separador de milhares
    except (ValueError, TypeError, AttributeError):
        return str(value)


def register_template_filters():
    """Registra filtros personalizados para os templates"""
    app.jinja_env.filters['gerar_classe_css_prazo'] = gerar_classe_css_prazo
    app.jinja_env.filters['gerar_badge_prazo'] = gerar_badge_prazo

    # Registrar outros filtros personalizados
    app.jinja_env.filters['date_format'] = date_format
    app.jinja_env.filters['number_format'] = number_format


# Registrar filtros
register_template_filters()


# Função auxiliar para formatação de datas no Python
def format_date_br(date_string):
    """Formata data de YYYY-MM-DD para DD/MM/AA - versão Python"""
    if not date_string:
        return ''
    try:
        # Se a string já estiver no formato DD/MM/YY, retorna como está
        if '/' in date_string and len(date_string.split('/')[2]) == 2:
            return date_string

        # Converte de YYYY-MM-DD para DD/MM/AA
        if isinstance(date_string, str) and len(date_string) >= 10:
            date_obj = datetime.strptime(date_string[:10], '%Y-%m-%d')
            return date_obj.strftime('%d/%m/%y')
        return date_string
    except (ValueError, AttributeError):
        return date_string

# Funções do banco de dados


def get_db():
    """Obtém conexão com o banco de dados"""
    db = sqlite3.connect('boletins.db')
    db.row_factory = sqlite3.Row
    return db


def ensure_column(db, table, column, definition):
    """Garantir coluna opcional no banco sem recriar tabela"""
    existing = {row['name'] for row in db.execute(f'PRAGMA table_info({table})')}
    if column not in existing:
        db.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
        db.commit()


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
        limite_inferior_aga REAL,
        limite_superior_aga REAL,
        observacoes TEXT,
        FOREIGN KEY (boletin_id) REFERENCES boletins (id) ON DELETE CASCADE
    )
    ''')
    ensure_column(db, 'componentes', 'limite_inferior_aga', 'REAL')
    ensure_column(db, 'componentes', 'limite_superior_aga', 'REAL')
    ensure_column(db, 'componentes', 'observacoes', 'TEXT')

    # Criar tabela de propriedades
    db.execute('''
    CREATE TABLE IF NOT EXISTS propriedades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        boletin_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        valor REAL NOT NULL,
        status_aga TEXT,
        status_cep TEXT,
        observacoes TEXT,
        FOREIGN KEY (boletin_id) REFERENCES boletins (id) ON DELETE CASCADE
    )
    ''')
    ensure_column(db, 'propriedades', 'observacoes', 'TEXT')

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
    from config import LIMITES_AGA8

    if componente in LIMITES_AGA8:
        minimo = LIMITES_AGA8[componente]['min']
        maximo = LIMITES_AGA8[componente]['max']
        return minimo <= valor <= maximo
    return True


def valida_cep(componente, novo_valor, historico):
    """Valida componente usando Controle Estatístico de Processo"""
    from config import CEP_AMOSTRAS_MIN, CEP_D2_CONSTANT, CEP_SIGMA_LIMIT

    ultimas_amostras = historico[-CEP_AMOSTRAS_MIN:]

    if len(ultimas_amostras) < 2:
        return True

    media = sum(ultimas_amostras) / len(ultimas_amostras)

    amplitudes = [abs(ultimas_amostras[i] - ultimas_amostras[i - 1])
                  for i in range(1, len(ultimas_amostras))]

    media_amplitudes = sum(amplitudes) / len(amplitudes)

    lcs = media + CEP_SIGMA_LIMIT * media_amplitudes / CEP_D2_CONSTANT
    lci = media - CEP_SIGMA_LIMIT * media_amplitudes / CEP_D2_CONSTANT

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
    from config import MASSAS_MOLARES

    propriedades = {}

    # Cálculo da Massa Molecular
    massa_molecular = 0.0
    total_percentual = 0.0

    for comp_nome, percentual in componentes_data.items():
        if comp_nome in MASSAS_MOLARES:
            massa_molecular += (percentual / 100.0) * MASSAS_MOLARES[comp_nome]
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

    massa_especifica = (
        P * massa_molecular /
        (propriedades['Fator de Compressibilidade'] * R * T)
    )

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
    from config import CEP_AMOSTRAS_MIN, CEP_D2_CONSTANT, CEP_SIGMA_LIMIT

    historico = get_historico_propriedade(propriedade_nome)

    if len(historico) < 2:
        return True  # Aceita se não há histórico suficiente

    # Usar apenas as últimas N amostras para CEP (configurável)
    ultimas_amostras = historico[-CEP_AMOSTRAS_MIN:] if len(historico) >= CEP_AMOSTRAS_MIN else historico

    if len(ultimas_amostras) < 2:
        return True

    media = sum(ultimas_amostras) / len(ultimas_amostras)

    # Cálculo dos limites de controle usando amplitude móvel
    amplitudes = [abs(ultimas_amostras[i] - ultimas_amostras[i - 1])
                  for i in range(1, len(ultimas_amostras))]

    if not amplitudes:
        return True

    media_amplitudes = sum(amplitudes) / len(amplitudes)

    # Limites de controle (configurável)
    lcs = media + CEP_SIGMA_LIMIT * media_amplitudes / CEP_D2_CONSTANT
    lci = media - CEP_SIGMA_LIMIT * media_amplitudes / CEP_D2_CONSTANT

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
        "Descrição das características do processo do ponto de "
        "amostragem do fluido"
        " (pressão e temperatura)",
        "Identificação do responsável pela amostragem",
        "Indicação dos incertezas de medição, com descrição do nível "
        "de confiança"
        " e fator de abrangência",
        "Identificação dos responsáveis técnicos pela realização da análise",
        "Identificação dos responsáveis pela elaboração e aprovação do boletim"
    ]

    db = get_db()
    for i, descricao in enumerate(itens_checklist, 1):
        db.execute(
            'INSERT INTO checklist_itens (boletin_id, item_numero, '
            'descricao, situacao) '
            'VALUES (?, ?, ?, ?)',
            (boletin_id, i, descricao, 'OK')
        )
    db.commit()


def gerar_pdf_relatorio(boletim_id):
    """Gera PDF completo do relatório com TODOS os campos do banco de dados"""
    db = get_db()

    # Buscar TODOS os dados do boletim
    boletim = db.execute('SELECT * FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
    if not boletim:
        return None

    componentes = db.execute(
        'SELECT * FROM componentes WHERE boletin_id = ? ORDER BY nome',
        (boletim_id,)
    ).fetchall()

    propriedades = db.execute(
        'SELECT * FROM propriedades WHERE boletin_id = ? ORDER BY nome',
        (boletim_id,)
    ).fetchall()

    checklist = db.execute(
        'SELECT * FROM checklist_itens WHERE boletin_id = ? ORDER BY item_numero',
        (boletim_id,)
    ).fetchall()

    # Criar PDF em memória
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    # Estilos aprimorados
    styles = getSampleStyleSheet()

    # Estilo do título principal
    titulo_principal_style = ParagraphStyle(
        'TituloPrincipal',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#fbbf24'),
        fontName='Helvetica-Bold'
    )

    subtitulo_style = ParagraphStyle(
        'Subtitulo',
        parent=styles['Title'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1e40af'),
        fontName='Helvetica-Bold'
    )

    secao_style = ParagraphStyle(
        'Secao',
        parent=styles['Heading2'],
        fontSize=11,
        spaceAfter=8,
        spaceBefore=15,
        textColor=colors.HexColor('#1e40af'),
        fontName='Helvetica-Bold'
    )

    normal_style = styles['Normal']
    normal_style.fontSize = 9

    # ===== CONTEÚDO DO PDF =====
    story = []

    # ===== CABEÇALHO =====
    story.append(Paragraph("BRAVA ENERGIA", titulo_principal_style))
    story.append(Paragraph("RELATÓRIO DE VALIDAÇÃO DE BOLETIM DE ANÁLISES QUÍMICAS", subtitulo_style))

    # Linha separadora
    from reportlab.platypus import HRFlowable
    story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor('#1e40af')))
    story.append(Spacer(1, 15))

    # ===== 1. INFORMAÇÕES COMPLETAS DO BOLETIM =====
    story.append(Paragraph("1. INFORMAÇÕES DO BOLETIM", secao_style))

    # Tabela com TODAS as informações do boletim (2 colunas para economia de espaço)
    info_completa = [
        # Linha 1
        [
            'Número do Boletim:', str(boletim['numero_boletim'] or ''),
            'Número do Documento:', str(boletim['numero_documento'] or '')
        ],
        # Linha 2
        [
            'Data de Coleta:', format_date_br(boletim['data_coleta']),
            'Data de Recebimento:', format_date_br(boletim['data_recebimento'])
        ],
        # Linha 3
        [
            'Data de Análise:', format_date_br(boletim['data_analise']),
            'Data de Emissão:', format_date_br(boletim['data_emissao'])
        ],
        # Linha 4
        [
            'Data de Validação:', format_date_br(boletim['data_validacao']),
            'Status Geral:', str(boletim['status'] or 'PENDENTE')
        ],
        # Linha 5 - Instalação e processo
        [
            'Instalação:', str(boletim['identificacao_instalacao'] or ''),
            'Plataforma:', str(boletim['plataforma'] or '')
        ],
        # Linha 6
        [
            'Sistema de Medição:', str(boletim['sistema_medicao'] or ''),
            'Classificação:', str(boletim['classificacao'] or '')
        ],
        # Linha 7
        [
            'Ponto de Coleta:', str(boletim['ponto_coleta'] or ''),
            'Agente Regulado:', str(boletim['agente_regulado'] or '')
        ],
        # Linha 8 - Condições do processo
        [
            'Pressão:', f"{boletim['pressao']} atm" if boletim['pressao'] else '',
            'Temperatura:', f"{boletim['temperatura']} °C" if boletim['temperatura'] else ''
        ],
        # Linha 9 - Responsável amostragem
        [
            'Responsável Amostragem:', str(boletim['responsavel_amostragem'] or ''),
            '', ''
        ]
    ]

    info_table = Table(info_completa, colWidths=[90, 140, 90, 140])
    info_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f8f9fa')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)

    # ===== VALIDAÇÃO DE PRAZOS ANP - RTM 52 =====
    story.append(Spacer(1, 15))
    story.append(Paragraph("VALIDAÇÃO DE PRAZOS ANP - REGULAMENTO TÉCNICO 52", secao_style))

    # Calcular prazos para exibir no PDF
    try:
        from validacao_prazos_anp import validar_todos_prazos_anp
        prazos_info = validar_todos_prazos_anp(
            boletim['data_coleta'],
            boletim['data_analise'],
            boletim['data_emissao'],
            boletim['data_validacao']
        )

        coleta_emissao = prazos_info.get('prazo_coleta_emissao', {}) or {}
        emissao_validacao = prazos_info.get('prazo_emissao_validacao', {}) or {}
        prazo_total = prazos_info.get('prazo_total', {}) or {}

        def _format_dias(entry):
            valor = entry.get('dias_decorridos')
            return f"{valor} dias" if valor is not None else 'N/A'

        def _format_status(entry):
            status = entry.get('status')
            if not status:
                return '-'
            if status == 'CONFORME':
                return 'V OK'
            if status == 'PENDENTE':
                return '! PENDENTE'
            return '? EXCEDIDO'

        prazos_data = [
            ['Validação', 'Prazo Calculado', 'Limite Regulamentar', 'Status'],
            ['Coleta -> Emissao', _format_dias(coleta_emissao), '25 dias (Portaria 52 ANP)', _format_status(coleta_emissao)],
            ['Emissao -> Validacao', _format_dias(emissao_validacao), '1 dia (Portaria 52 ANP)', _format_status(emissao_validacao)],
            ['Prazo Total (Coleta -> Validacao)', _format_dias(prazo_total), '28 dias (Portaria 52 ANP)', _format_status(prazo_total)]
        ]
    except Exception:
        prazos_data = [
            ['Validação', 'Status'],
            ['Validação de Prazos RTM 52', 'Dados insuficientes para validação']
        ]

    prazos_table = Table(prazos_data, colWidths=[120, 80, 120, 80])
    prazos_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(prazos_table)

    # ===== 2. CONDIÇÕES DO PROCESSO =====
    story.append(Spacer(1, 15))
    story.append(Paragraph("2. CONDIÇÕES DO PROCESSO", secao_style))

    condicoes_data = [
        ['Parâmetro', 'Valor', 'Unidade'],
        ['Pressão', str(boletim['pressao']) if boletim['pressao'] else '-', 'atm'],
        ['Temperatura', str(boletim['temperatura']) if boletim['temperatura'] else '-', '°C']
    ]

    condicoes_table = Table(condicoes_data, colWidths=[150, 100, 80])
    condicoes_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(condicoes_table)

    # ===== 3. COMPONENTES GASOSOS COMPLETOS =====
    story.append(Spacer(1, 15))
    story.append(Paragraph("3. COMPONENTES GASOSOS (%)", secao_style))

    if componentes:
        comp_data = [
            ['Componente', 'Unidade', '% Molar', 'Status A.G.A #8', 'Status CEP', 'Min A.G.A', 'Max A.G.A']
        ]

        # Definir limites A.G.A #8 por componente
        limites_aga = {
            'Metano': {'min': 0, 'max': 100},
            'Etano': {'min': 0, 'max': 100},
            'Propano': {'min': 0, 'max': 12},
            'i-Butano': {'min': 0, 'max': 6},
            'n-Butano': {'min': 0, 'max': 6},
            'i-Pentano': {'min': 0, 'max': 4},
            'n-Pentano': {'min': 0, 'max': 4},
            'Hexano': {'min': 0, 'max': 100},
            'Heptano': {'min': 0, 'max': 100},
            'Octano': {'min': 0, 'max': 100},
            'Nonano': {'min': 0, 'max': 100},
            'Decano': {'min': 0, 'max': 100},
            'Oxigênio': {'min': 0, 'max': 21},
            'Nitrogênio': {'min': 0, 'max': 100},
            'CO2': {'min': 0, 'max': 100}
        }

        for comp in componentes:
            nome_simples = comp['nome'].split(',')[0]  # Pegar parte antes da vírgula
            limites = limites_aga.get(nome_simples, {'min': 0, 'max': 100})

            comp_data.append([
                comp['nome'],
                '% mol',
                f"{comp['percentual_molar']:.3f}%",
                comp['status_aga'] or 'PENDENTE',
                comp['status_cep'] or 'PENDENTE',
                f"{limites['min']}%",
                f"{limites['max']}%"
            ])

        comp_table = Table(comp_data, colWidths=[70, 30, 50, 60, 60, 40, 40])
        comp_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),  # % Molar alinhado à direita
            ('ALIGN', (3, 0), (-1, -1), 'CENTER'),  # Status centralizados
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(comp_table)
    else:
        story.append(Paragraph("Nenhum componente cadastrado para este boletim.", normal_style))

    # ===== 4. PROPRIEDADES DO FLUIDO COMPLETAS =====
    story.append(Spacer(1, 15))
    story.append(Paragraph("4. PROPRIEDADES DO FLUIDO", secao_style))

    if propriedades:
        prop_data = [
            ['Propriedade', 'Unidade', 'Valor', 'Status CEP', 'Limite Inf.', 'Limite Sup.']
        ]

        # Limites para propriedades do fluido
        limites_propriedades = {
            'Fator de compressibilidade': {'min': 0.9, 'max': 1.1, 'unidade': 'adimensional'},
            'Massa Específica': {'min': 0.65, 'max': 0.9, 'unidade': 'kg/m³'},
            'Massa Molecular': {'min': 16, 'max': 22, 'unidade': 'g/mol'}
        }

        for prop in propriedades:
            limite_info = None
            for key, val in limites_propriedades.items():
                if key in prop['nome']:
                    limite_info = val
                    break

            if limite_info:
                prop_data.append([
                    prop['nome'][:40] + '...' if len(prop['nome']) > 40 else prop['nome'],
                    limite_info['unidade'],
                    f"{prop['valor']:.4f}",
                    prop['status_cep'] or 'PENDENTE',
                    str(limite_info['min']),
                    str(limite_info['max'])
                ])
            else:
                prop_data.append([
                    prop['nome'][:40] + '...' if len(prop['nome']) > 40 else prop['nome'],
                    '-',
                    f"{prop['valor']:.4f}",
                    prop['status_cep'] or 'PENDENTE',
                    '-',
                    '-'
                ])

        prop_table = Table(prop_data, colWidths=[120, 50, 60, 60, 50, 50])
        prop_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),  # Valores alinhados à direita
            ('ALIGN', (3, 0), (-1, -1), 'CENTER'),  # Status centralizados
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(prop_table)
    else:
        story.append(Paragraph("Nenhuma propriedade cadastrada para este boletim.", normal_style))

    # ===== 5. CHECK LIST NBR ISO/IEC 17025 COMPLETO =====
    story.append(Spacer(1, 15))
    story.append(Paragraph("5. CHECK LIST NBR ISO/IEC 17025", secao_style))

    if checklist:
        checklist_data = [['Item', 'Descrição', 'Situação', 'N/A', 'Observações']]

        for item_row in checklist:
            item = dict(item_row)
            descricao = item['descricao'][:60] + '...' if len(item['descricao']) > 60 else item['descricao']
            observacao = (item.get('observacao') or '')
            observacao = observacao[:30] + '...' if len(observacao) > 30 else observacao
            nao_aplicavel = item.get('nao_aplicavel', 'Não') or 'Não'

            checklist_data.append([
                str(item['item_numero']),
                descricao,
                item['situacao'] or 'Pendente',
                nao_aplicavel,
                observacao
            ])

        checklist_table = Table(checklist_data, colWidths=[25, 180, 60, 35, 90])
        checklist_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Item centralizado
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),  # Status centralizados
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(checklist_table)
    else:
        story.append(Paragraph("Checklist não preenchido para este boletim.", normal_style))

    # ===== 6. RESULTADO FINAL DA VALIDAÇÃO =====
    story.append(Spacer(1, 20))
    story.append(Paragraph("6. RESULTADO FINAL DA VALIDAÇÃO", secao_style))

    resultado_data = [
        ['Validação', 'Status'],
        ['A.G.A #8', boletim['status_aga8'] or 'PENDENTE'],
        ['CEP (Controle Estatístico)', boletim['status_cep'] or 'PENDENTE'],
        ['Checklist ISO/IEC 17025', boletim['status_checklist'] or 'PENDENTE'],
        ['STATUS GERAL DO BOLETIM', boletim['status'] or 'PENDENTE']
    ]

    resultado_table = Table(resultado_data, colWidths=[200, 150])
    resultado_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Linha do status geral
        ('GRID', (0, 0), (-1, -1), 2, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f3f4f6')),  # Destacar status geral
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(resultado_table)

    # ===== 7. OBSERVAÇÕES =====
    if boletim['observacoes']:
        story.append(Spacer(1, 15))
        story.append(Paragraph("7. OBSERVAÇÕES", secao_style))
        story.append(Paragraph(str(boletim['observacoes']), normal_style))

    # ===== 8. RESPONSÁVEIS PELA VALIDAÇÃO =====
    story.append(Spacer(1, 20))
    story.append(Paragraph("8. RESPONSÁVEIS PELA VALIDAÇÃO", secao_style))

    resp_data = [
        ['Responsável Técnico', 'Responsável Elaboração', 'Responsável Aprovação'],
        [
            boletim['responsavel_tecnico'] or '',
            boletim['responsavel_elaboracao'] or '',
            boletim['responsavel_aprovacao'] or ''
        ],
        ['_' * 25, '_' * 25, '_' * 25],
        ['Assinatura', 'Assinatura', 'Assinatura']
    ]

    resp_table = Table(resp_data, colWidths=[130, 130, 130])
    resp_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, 1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 2), (-1, 2), 1, colors.black),
    ]))
    story.append(resp_table)

    # ===== RODAPÉ =====
    story.append(Spacer(1, 20))
    rodape = Paragraph(
        f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')} | "
        f"BRAVA ENERGIA - Sistema de Validação de Boletins Cromatográficos",
        ParagraphStyle('Rodape', parent=normal_style, fontSize=7, alignment=TA_CENTER, textColor=colors.grey)
    )
    story.append(rodape)

    # ===== GERAR PDF =====
    doc.build(story)
    buffer.seek(0)
    return buffer

# Rotas da aplicação


@app.route('/favicon.ico')
def favicon():
    """Serve a simple favicon"""
    # Create a minimal ICO response to prevent 404 errors
    ico_header = (
        b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00\x08'
        b'\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00'
    )
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
        where_conditions.append(
            "DATE(b.data_coleta) >= DATE('now', '-' || ? || ' days')")
        params.append(days)

    if status_filter:
        where_conditions.append("b.status = ?")
        params.append(status_filter)

    where_clause = "WHERE " + \
        " AND ".join(where_conditions) if where_conditions else ""

    # Estatísticas gerais (com filtros aplicados)
    stats = {}
    base_query = f"SELECT COUNT(*) FROM boletins b {where_clause}"
    stats['total_boletins'] = db.execute(base_query, params).fetchone()[0]

    # Estatísticas de validação (com filtros)
    if where_clause:
        stats['boletins_validados'] = db.execute(
            f"SELECT COUNT(*) FROM boletins b {where_clause} AND b.status = ?",
            params + ['VALIDADO']
        ).fetchone()[0]
        stats['boletins_invalidados'] = db.execute(
            f"SELECT COUNT(*) FROM boletins b {where_clause} AND b.status = ?",
            params + ['INVALIDADO']
        ).fetchone()[0]
        stats['aga8_aprovados'] = db.execute(
            f"SELECT COUNT(*) FROM boletins b {where_clause} AND b.status_aga8 = ?",
            params + ['VALIDADO']
        ).fetchone()[0]
        stats['cep_aprovados'] = db.execute(
            f"SELECT COUNT(*) FROM boletins b {where_clause} AND b.status_cep = ?",
            params + ['VALIDADO']
        ).fetchone()[0]
        stats['checklist_aprovados'] = db.execute(
            f"SELECT COUNT(*) FROM boletins b {where_clause} AND b.status_checklist = ?",
            params + ['VALIDADO']
        ).fetchone()[0]
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
        stats['boletins_validados'] * 100 /
        stats['total_boletins']
    ) if stats['total_boletins'] > 0 else 0

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
        comp_where.append(
            "DATE(b.data_coleta) >= DATE('now', '-' || ? || ' days')")
        comp_params.append(int(periodo))

    comp_where_clause = "WHERE " + \
        " AND ".join(comp_where) if comp_where else ""

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
    componentes_problemas = db.execute(
        componentes_query, comp_params).fetchall()

    # Histórico recente para gráfico (com filtros aplicados)
    if componente_filter:
        hist_where = ["hc.componente = ?"]
        hist_params = [componente_filter]
    else:
        hist_where = ["hc.componente IN ('Metano', 'Etano', 'Propano', 'Nitrogênio', 'CO2')"]
        hist_params = []

    if periodo:
        hist_where.append("DATE(hc.data_coleta) >= DATE('now', '-' || ? || ' days')")
        hist_params.append(int(periodo))

    hist_where_clause = " AND ".join(hist_where)
    hist_query = f'''
        SELECT hc.componente, b.numero_boletim, hc.data_coleta, hc.valor, c.status_aga, c.status_cep
        FROM historico_componentes hc
        JOIN boletins b ON hc.boletin_id = b.id
        JOIN componentes c ON hc.componente = c.nome AND hc.boletin_id = c.boletin_id
        WHERE {hist_where_clause}
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
        SELECT b.id, b.numero_boletim, b.identificacao_instalacao,
               b.data_coleta, b.data_emissao, b.data_validacao, b.status
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
            'responsavel_amostragem': request.form['responsavel_amostragem'],
            'pressao': float(request.form['pressao']),
            'temperatura': float(request.form['temperatura']),
            'observacoes': request.form['observacoes'],
            'responsavel_tecnico': request.form['responsavel_tecnico'],
            'responsavel_elaboracao': request.form['responsavel_elaboracao'],
            'responsavel_aprovacao': request.form['responsavel_aprovacao']
        }

        # Validar sequência de datas conforme RTM 52
        errors = []
        data_coleta = datetime.strptime(dados_boletim['data_coleta'], '%Y-%m-%d').date()
        data_emissao = datetime.strptime(dados_boletim['data_emissao'], '%Y-%m-%d').date()
        data_validacao = request.form.get('data_validacao')

        # Validação 1: Data de emissão não pode ser anterior à data de coleta
        if data_emissao < data_coleta:
            errors.append(f"Data de emissão ({data_emissao.strftime('%d/%m/%Y')}) não pode ser anterior à data de coleta ({data_coleta.strftime('%d/%m/%Y')})")

        # Validação 2: Verificar prazo Coleta → Emissão (máximo 25 dias)
        dias_coleta_emissao = (data_emissao - data_coleta).days
        if dias_coleta_emissao > 25:
            errors.append(f"Prazo entre coleta e emissão excede 25 dias (RTM 52): {dias_coleta_emissao} dias")

        # Validação 3: Data de validação, se informada
        if data_validacao and data_validacao.strip():
            data_validacao_dt = datetime.strptime(data_validacao, '%Y-%m-%d').date()

            if data_validacao_dt < data_emissao:
                errors.append(f"Data de validação ({data_validacao_dt.strftime('%d/%m/%Y')}) não pode ser anterior à data de emissão ({data_emissao.strftime('%d/%m/%Y')})")

            if data_validacao_dt < data_coleta:
                errors.append(f"Data de validação ({data_validacao_dt.strftime('%d/%m/%Y')}) não pode ser anterior à data de coleta ({data_coleta.strftime('%d/%m/%Y')})")

            # Validação do prazo total (máximo 28 dias)
            dias_total = (data_validacao_dt - data_coleta).days
            if dias_total > 28:
                errors.append(f"Prazo total entre coleta e validação excede 28 dias (RTM 52): {dias_total} dias")

        # Se há erros de validação, retornar para o formulário com mensagens de erro
        if errors:
            flash('Erros de validação encontrados:', 'danger')
            for error in errors:
                flash(f"• {error}", 'danger')
            return render_template('cadastrar.html', form_data=request.form)

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
                ponto_coleta, agente_regulado, responsavel_amostragem,
                pressao, temperatura, observacoes, responsavel_tecnico, responsavel_elaboracao,
                responsavel_aprovacao, data_validacao, status, status_cep, status_aga8, status_checklist
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dados_boletim['numero_boletim'], dados_boletim['numero_documento'],
            dados_boletim['data_coleta'], dados_boletim['data_recebimento'],
            dados_boletim['data_analise'], dados_boletim['data_emissao'],
            dados_boletim['identificacao_instalacao'], dados_boletim['plataforma'],
            dados_boletim['sistema_medicao'], dados_boletim['classificacao'],
            dados_boletim['ponto_coleta'],
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
            status_aga = "VALIDADO" if valida_aga8(
                comp, valor) else "INVALIDADO"
            historico = get_historico_componente(comp)
            status_cep = "VALIDADO" if valida_cep(
                comp, valor, historico) else "INVALIDADO"

            db.execute('''
                INSERT INTO componentes (boletin_id, nome, percentual_molar, status_aga, status_cep)
                VALUES (?, ?, ?, ?, ?)
            ''', (boletim_id, comp, valor, status_aga, status_cep))

            db.execute('''
                INSERT INTO historico_componentes (componente, boletin_id, valor, data_coleta)
                VALUES (?, ?, ?, ?)
            ''', (comp, boletim_id, valor, dados_boletim['data_coleta']))

        # Calcular propriedades automaticamente (removido - agora é entrada manual)
        # propriedades_calculadas = calcular_propriedades_fluido(componentes_data)

        # Processar propriedades inseridas manualmente
        propriedades_manuais = []

        # Verificar se as propriedades foram enviadas no formulário
        if 'fator_compressibilidade' in request.form:
            fator_comp = request.form.get('fator_compressibilidade')
            if fator_comp and fator_comp.strip():
                propriedades_manuais.append(('Fator de compressibilidade', float(fator_comp)))

        if 'massa_especifica' in request.form:
            massa_esp = request.form.get('massa_especifica')
            if massa_esp and massa_esp.strip():
                propriedades_manuais.append(('Massa Específica', float(massa_esp)))

        if 'massa_molecular' in request.form:
            massa_mol = request.form.get('massa_molecular')
            if massa_mol and massa_mol.strip():
                propriedades_manuais.append(('Massa Molecular', float(massa_mol)))

        # Inserir propriedades manuais
        for nome_prop, valor_manual in propriedades_manuais:
            # Validação CEP para propriedades
            status_cep_prop = "VALIDADO" if valida_cep_propriedade(nome_prop, valor_manual) else "INVALIDADO"

            db.execute('''
                INSERT INTO propriedades (boletin_id, nome, valor, status_aga, status_cep)
                VALUES (?, ?, ?, ?, ?)
            ''', (boletim_id, nome_prop, valor_manual, "N/A", status_cep_prop))

            # Salvar no histórico de propriedades
            db.execute('''
                INSERT INTO historico_propriedades (propriedade, boletin_id, valor, data_coleta)
                VALUES (?, ?, ?, ?)
            ''', (nome_prop, boletim_id, valor_manual, dados_boletim['data_coleta']))

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
        status = "INVALIDADO" if (
            status_aga8 == "INVALIDADO" or status_cep == "INVALIDADO") else "VALIDADO"
        data_validacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db.execute('''
            UPDATE boletins SET status = ?, status_cep = ?, status_aga8 = ?,
                               status_checklist = ?, data_validacao = ? WHERE id = ?
        ''', (status, status_cep, status_aga8, status_checklist, data_validacao, boletim_id))
        db.commit()

        flash('Boletim cadastrado com sucesso!')
        return redirect(url_for('relatorio', boletim_id=boletim_id))

    return render_template('cadastrar.html')


@app.route('/editar/<int:boletim_id>', methods=['GET', 'POST'])
def editar_boletim(boletim_id):
    """Página para editar um boletim existente"""
    db = get_db()

    # Buscar dados do boletim
    boletim = db.execute(
        'SELECT * FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
    if not boletim:
        flash('Boletim não encontrado.')
        return redirect(url_for('listar_boletins'))

    if request.method == 'POST':
        # Capturar dados do formulário
        try:
            # Atualizar dados do boletim
            db.execute('''
                UPDATE boletins SET
                    numero_boletim = ?, numero_documento = ?, data_coleta = ?,
                    data_recebimento = ?, data_analise = ?, data_emissao = ?,
                    data_validacao = ?, identificacao_instalacao = ?,
                    plataforma = ?, sistema_medicao = ?, classificacao = ?,
                    ponto_coleta = ?, agente_regulado = ?,
                    responsavel_amostragem = ?, pressao = ?, temperatura = ?,
                    responsavel_tecnico = ?, responsavel_elaboracao = ?,
                    responsavel_aprovacao = ?, observacoes = ?
                WHERE id = ?
            ''', (
                request.form['numero_boletim'],
                request.form['numero_documento'] or None,
                request.form['data_coleta'],
                request.form['data_recebimento'] or None,
                request.form['data_analise'] or None,
                request.form['data_emissao'],
                request.form['data_validacao'] or None,
                request.form['identificacao_instalacao'],
                request.form['plataforma'],
                request.form['sistema_medicao'],
                request.form['classificacao'],
                request.form['ponto_coleta'],
                request.form['agente_regulado'],
                request.form['responsavel_amostragem'],
                float(request.form['pressao']),
                float(request.form['temperatura']),
                request.form['responsavel_tecnico'] or None,
                request.form['responsavel_elaboracao'] or None,
                request.form['responsavel_aprovacao'] or None,
                request.form['observacoes'] or None,
                boletim_id
            ))
            db.commit()
            flash(
                f'Boletim {request.form["numero_boletim"]} atualizado com sucesso!')
            return redirect(url_for('listar_boletins'))

        except Exception as e:
            flash(f'Erro ao atualizar boletim: {str(e)}')

    # Buscar componentes do boletim para exibir
    componentes = db.execute('''
        SELECT nome, percentual_molar, status_aga, status_cep
        FROM componentes
        WHERE boletin_id = ?
        ORDER BY nome
    ''', (boletim_id,)).fetchall()

    return render_template('editar_boletim.html', boletim=boletim, componentes=componentes)


@app.route('/excluir/<int:boletim_id>', methods=['POST'])
def excluir_boletim(boletim_id):
    """Excluir um boletim e todos os dados associados"""
    db = get_db()

    # Buscar dados do boletim para mostrar mensagem
    boletim = db.execute(
        'SELECT numero_boletim FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
    if not boletim:
        flash('Boletim não encontrado.')
        return redirect(url_for('listar_boletins'))

    try:
        # Excluir em ordem (devido às chaves estrangeiras)
        # 1. Excluir histórico de componentes
        db.execute(
            'DELETE FROM historico_componentes WHERE boletin_id = ?', (boletim_id,))

        # 2. Excluir componentes
        db.execute('DELETE FROM componentes WHERE boletin_id = ?', (boletim_id,))

        # 3. Excluir boletim
        db.execute('DELETE FROM boletins WHERE id = ?', (boletim_id,))

        db.commit()
        flash(f'Boletim {boletim["numero_boletim"]} excluído com sucesso!')

    except Exception as e:
        db.rollback()
        flash(f'Erro ao excluir boletim: {str(e)}')

    return redirect(url_for('listar_boletins'))


@app.route('/relatorio/<int:boletim_id>', methods=['GET', 'POST'])
@app.route('/relatorio/<int:boletim_id>/<edit_mode>', methods=['GET', 'POST'])
def relatorio(boletim_id, edit_mode=None):
    """Exibe o relatório detalhado de um boletim específico, com modo de edição opcional"""
    logger.debug(f"Relatório acessado - Method: {request.method}, Edit Mode: {edit_mode}, ID: {boletim_id}")
    db = get_db()

    # Verificar se é uma requisição POST para salvar edições
    if request.method == 'POST' and edit_mode == 'edit':
        logger.debug(f"POST request received for boletim {boletim_id}")
        logger.debug(f"Form keys: {list(request.form.keys())[:5]}...")  # Log only first 5 keys
        logger.debug(f"Form data length: {len(request.form)}")

        try:
            # Validar campos numéricos
            pressao = request.form.get('pressao', '').strip()
            temperatura = request.form.get('temperatura', '').strip()

            # Converter para float ou usar None se vazio
            pressao_val = float(pressao) if pressao else None
            temperatura_val = float(temperatura) if temperatura else None

            # Atualizar dados do boletim
            logger.debug(f"Updating boletim {boletim_id} - Classificacao: {request.form.get('classificacao', 'N/A')}")

            cursor = db.execute('''
                UPDATE boletins SET
                    numero_boletim = ?, numero_documento = ?, data_coleta = ?,
                    data_recebimento = ?, data_analise = ?, data_emissao = ?,
                    data_validacao = ?, identificacao_instalacao = ?,
                    plataforma = ?, sistema_medicao = ?, classificacao = ?,
                    ponto_coleta = ?, agente_regulado = ?,
                    responsavel_amostragem = ?, pressao = ?, temperatura = ?
                WHERE id = ?
            ''', (
                request.form['numero_boletim'],
                request.form['numero_documento'] or None,
                request.form['data_coleta'],
                request.form['data_recebimento'] or None,
                request.form['data_analise'] or None,
                request.form['data_emissao'],
                request.form['data_validacao'] or None,
                request.form['identificacao_instalacao'],
                request.form['plataforma'],
                request.form['sistema_medicao'],
                request.form['classificacao'],
                request.form['ponto_coleta'],
                request.form['agente_regulado'],
                request.form['responsavel_amostragem'],
                pressao_val,
                temperatura_val,
                boletim_id
            ))

            logger.debug(f"Update completed - rowcount: {cursor.rowcount}")

            # Verificar dados antes do commit
            verificacao = db.execute(
                'SELECT classificacao FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
            logger.debug(f"Data verification before commit - Classificacao: {verificacao['classificacao'] if verificacao else 'None'}")

            # Atualizar dados do checklist
            checklist_items = db.execute(
                'SELECT item_numero FROM checklist_itens WHERE boletin_id = ?', (boletim_id,)).fetchall()
            for item in checklist_items:
                item_num = item['item_numero']
                situacao_key = f'checklist_{item_num}_situacao'
                nao_aplicavel_key = f'checklist_{item_num}_nao_aplicavel'
                observacao_key = f'checklist_{item_num}_observacao'

                if situacao_key in request.form:
                    db.execute('''
                        UPDATE checklist_itens SET
                            situacao = ?,
                            nao_aplicavel = ?,
                            observacao = ?
                        WHERE boletin_id = ? AND item_numero = ?
                    ''', (
                        request.form[situacao_key],
                        int(request.form.get(nao_aplicavel_key, 0)),
                        request.form.get(observacao_key, '') or None,
                        boletim_id,
                        item_num
                    ))

            # Atualizar dados dos componentes - mapeamento completo
            mapeamento_componentes = {
                'metano_ch4': 'Metano',
                'etano_c2h6': 'Etano',
                'propano_c3h8': 'Propano',
                'i_butano_ic4h10': 'i-Butano',
                'n_butano_nc4h10': 'n-Butano',
                'i_pentano_ic5h12': 'i-Pentano',
                'n_pentano_nc5h12': 'n-Pentano',
                'c6_mais': 'Hexano',  # C₆+ maps to Hexano in database
                'heptano_c7h16': 'Heptano',
                'octano_c8h18': 'Octano',
                'nonano_c9h20': 'Nonano',
                'decano_c10h22': 'Decano',
                'oxigenio_o2': 'Oxigênio',
                'nitrogenio_n2': 'Nitrogênio',
                'dioxido_carbono_co2': 'CO2'
            }

            for form_name, db_name in mapeamento_componentes.items():
                if form_name in request.form:
                    percentual_str = request.form[form_name].strip()
                    if percentual_str:  # Se não estiver vazio
                        try:
                            percentual = float(percentual_str)
                            # Verificar se o componente já existe
                            existing = db.execute('''
                                SELECT id FROM componentes
                                WHERE boletin_id = ? AND nome = ?
                            ''', (boletim_id, db_name)).fetchone()

                            if existing:
                                # Atualizar componente existente
                                db.execute('''
                                    UPDATE componentes SET percentual_molar = ?
                                    WHERE id = ?
                                ''', (percentual, existing['id']))
                            else:
                                # Inserir novo componente
                                db.execute('''
                                    INSERT INTO componentes (boletin_id, nome, percentual_molar, status_aga, status_cep)
                                    VALUES (?, ?, ?, ?, ?)
                                ''', (boletim_id, db_name, percentual, 'VALIDADO', 'VALIDADO'))
                        except ValueError:
                            # Ignorar valores inválidos
                            continue

            db.commit()
            logger.debug("Database changes committed successfully")

            # Verificar dados após commit
            verificacao_final = db.execute(
                'SELECT classificacao FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
            logger.debug(f"Data verification after commit - Classificacao: {verificacao_final['classificacao'] if verificacao_final else 'None'}")

            db.close()
            flash(f'Boletim {request.form["numero_boletim"]} atualizado com sucesso!')
            return redirect(url_for('relatorio', boletim_id=boletim_id))

        except ValueError as e:
            db.rollback()
            db.close()
            flash(f'Erro nos dados fornecidos: {str(e)}')
            return redirect(url_for('relatorio', boletim_id=boletim_id, edit_mode='edit'))

        except sqlite3.Error as e:
            db.rollback()
            db.close()
            flash(f'Erro no banco de dados: {str(e)}')
            return redirect(url_for('relatorio', boletim_id=boletim_id, edit_mode='edit'))

        except Exception as e:
            db.rollback()
            db.close()
            flash(f'Erro ao atualizar boletim: {str(e)}')
            return redirect(url_for('relatorio', boletim_id=boletim_id, edit_mode='edit'))

    boletim = db.execute(
        'SELECT * FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
    if boletim is None:
        flash('Boletim não encontrado!')
        return redirect(url_for('listar_boletins'))

    componentes = db.execute('''
        SELECT * FROM componentes WHERE boletin_id = ?
    ''', (boletim_id,)).fetchall()

    # Criar dicionário de componentes para facilitar acesso no template
    componentes_dict = {}
    mapeamento_nomes = {
        'Metano': 'metano_ch4',
        'Etano': 'etano_c2h6',
        'Propano': 'propano_c3h8',
        'i-Butano': 'i_butano_ic4h10',
        'n-Butano': 'n_butano_nc4h10',
        'i-Pentano': 'i_pentano_ic5h12',
        'n-Pentano': 'n_pentano_nc5h12',
        'Hexano': 'c6_mais',  # Database Hexano maps to template c6_mais (shown as C₆+)
        'Heptano': 'heptano_c7h16',
        'Octano': 'octano_c8h18',
        'Nonano': 'nonano_c9h20',
        'Decano': 'decano_c10h22',
        'Oxigênio': 'oxigenio_o2',
        'Nitrogênio': 'nitrogenio_n2',
        'CO2': 'dioxido_carbono_co2'
    }

    for comp in componentes:
        nome_template = mapeamento_nomes.get(comp['nome'])
        if nome_template:
            componentes_dict[nome_template] = comp['percentual_molar']

    propriedades = db.execute('''
        SELECT * FROM propriedades WHERE boletin_id = ?
    ''', (boletim_id,)).fetchall()

    checklist = db.execute('''
        SELECT * FROM checklist_itens WHERE boletin_id = ? ORDER BY item_numero
    ''', (boletim_id,)).fetchall()

    # Calculate CEP limits for each component
    def calculate_cep_limits(componente_nome):
        from config import CEP_AMOSTRAS_MIN, CEP_D2_CONSTANT, CEP_SIGMA_LIMIT

        historico = get_historico_componente(componente_nome)
        ultimas_amostras = historico[-CEP_AMOSTRAS_MIN:]
        if len(ultimas_amostras) < 2:
            return None, None
        media = sum(ultimas_amostras) / len(ultimas_amostras)
        amplitudes = [abs(ultimas_amostras[i] - ultimas_amostras[i - 1])
                      for i in range(1, len(ultimas_amostras))]
        media_amplitudes = sum(amplitudes) / len(amplitudes)
        lcs = media + CEP_SIGMA_LIMIT * media_amplitudes / CEP_D2_CONSTANT
        lci = media - CEP_SIGMA_LIMIT * media_amplitudes / CEP_D2_CONSTANT
        return lci, lcs

    componentes_with_limits = []
    for comp in componentes:
        lci, lcs = calculate_cep_limits(comp['nome'])
        comp_dict = dict(comp)
        comp_dict['cep_lci'] = lci
        comp_dict['cep_lcs'] = lcs
        componentes_with_limits.append(comp_dict)

    # Definir se está em modo de edição
    is_edit_mode = edit_mode == 'edit'

    # Validar prazos ANP
    validacao_prazos = validar_todos_prazos_anp(
        boletim['data_coleta'],
        boletim['data_analise'],
        boletim['data_emissao'],
        boletim['data_validacao']
    )

    # Fechar conexão
    db.close()

    return render_template(
        'relatorio_excel.html',
        boletim=boletim,
        componentes=componentes_with_limits,
        propriedades=propriedades,
        checklist=checklist,
        componentes_dict=componentes_dict,
        edit_mode=is_edit_mode,
        validacao_prazos=validacao_prazos
    )


@app.route('/revalidar/<int:boletim_id>', methods=['POST'])
def revalidar_boletim(boletim_id):
    """Revalida um boletim existente aplicando as regras A.G.A #8 e CEP"""
    db = get_db()

    # Verificar se o boletim existe
    boletim = db.execute(
        'SELECT * FROM boletins WHERE id = ?', (boletim_id,)).fetchone()
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
        status_aga = "VALIDADO" if valida_aga8(
            componente['nome'], componente['percentual_molar']) else "INVALIDADO"

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
    status = "INVALIDADO" if (
        status_aga8 == "INVALIDADO" or status_cep == "INVALIDADO") else "VALIDADO"
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
            status_aga = "VALIDADO" if valida_aga8(
                componente['nome'], componente['percentual_molar']) else "INVALIDADO"

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
        status = "INVALIDADO" if (
            status_aga8 == "INVALIDADO" or status_cep == "INVALIDADO") else "VALIDADO"
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
                flash(f'OK: Importação concluída: {resultado["success"]} boletins '
                      f'processados com sucesso!')

                for boletim in resultado['boletins_processados']:
                    flash(f'RELATORIO: Boletim {boletim["numero_boletim"]}: {boletim["status"]} '
                          f'({boletim["componentes_processados"]} componentes)')

            if resultado['errors']:
                for erro in resultado['errors']:
                    flash(f'ERRO: {erro}', 'error')

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
        flash(f'OK: Processados {contador} boletins existentes. Agora eles aparecem '
              f'na aba Histórico e podem ser revalidados.')

    except Exception as e:
        flash(f'Erro ao processar boletins existentes: {str(e)}', 'error')

    return redirect(url_for('listar_boletins'))


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)