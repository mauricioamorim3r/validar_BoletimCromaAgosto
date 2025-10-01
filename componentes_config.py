# -*- coding: utf-8 -*-
"""
Configuração oficial dos componentes cromatográficos
Baseado na tabela de referência fornecida
"""

# Lista oficial dos 15 componentes com nomenclatura padronizada
COMPONENTES_OFICIAIS = [
    {
        'id': 'metano_ch4',
        'nome_backend': 'Metano',
        'nome_display': 'Metano, CH₄',
        'formula': 'CH₄',
        'nome_ingles': 'Methane'
    },
    {
        'id': 'etano_c2h6',
        'nome_backend': 'Etano',
        'nome_display': 'Etano, C₂H₆',
        'formula': 'C₂H₆',
        'nome_ingles': 'Ethane'
    },
    {
        'id': 'propano_c3h8',
        'nome_backend': 'Propano',
        'nome_display': 'Propano, C₃H₈',
        'formula': 'C₃H₈',
        'nome_ingles': 'Propane'
    },
    {
        'id': 'i_butano_ic4h10',
        'nome_backend': 'i-Butano',
        'nome_display': 'Isobutano, i-C₄H₁₀',
        'formula': 'i-C₄H₁₀',
        'nome_ingles': 'Isobutane'
    },
    {
        'id': 'n_butano_nc4h10',
        'nome_backend': 'n-Butano',
        'nome_display': 'n-Butano, n-C₄H₁₀',
        'formula': 'n-C₄H₁₀',
        'nome_ingles': 'n-Butane'
    },
    {
        'id': 'i_pentano_ic5h12',
        'nome_backend': 'i-Pentano',
        'nome_display': 'Isopentano, i-C₅H₁₂',
        'formula': 'i-C₅H₁₂',
        'nome_ingles': 'Isopentane'
    },
    {
        'id': 'n_pentano_nc5h12',
        'nome_backend': 'n-Pentano',
        'nome_display': 'n-Pentano, n-C₅H₁₂',
        'formula': 'n-C₅H₁₂',
        'nome_ingles': 'n-Pentane'
    },
    {
        'id': 'n_hexano_nc6h14',
        'nome_backend': 'Hexano',
        'nome_display': 'n-Hexano, n-C₆H₁₄',
        'formula': 'n-C₆H₁₄',
        'nome_ingles': 'n-Hexane'
    },
    {
        'id': 'n_heptano_nc7h16',
        'nome_backend': 'Heptano',
        'nome_display': 'n-Heptano, n-C₇H₁₆',
        'formula': 'n-C₇H₁₆',
        'nome_ingles': 'n-Heptane'
    },
    {
        'id': 'n_octano_nc8h18',
        'nome_backend': 'Octano',
        'nome_display': 'n-Octano, n-C₈H₁₈',
        'formula': 'n-C₈H₁₈',
        'nome_ingles': 'n-Octane'
    },
    {
        'id': 'n_nonano_nc9h20',
        'nome_backend': 'Nonano',
        'nome_display': 'n-Nonano, n-C₉H₂₀',
        'formula': 'n-C₉H₂₀',
        'nome_ingles': 'n-Nonane'
    },
    {
        'id': 'n_decano_nc10h22',
        'nome_backend': 'Decano',
        'nome_display': 'n-Decano, n-C₁₀H₂₂',
        'formula': 'n-C₁₀H₂₂',
        'nome_ingles': 'n-Decane'
    },
    {
        'id': 'nitrogenio_n2',
        'nome_backend': 'Nitrogênio',
        'nome_display': 'Nitrogênio, N₂',
        'formula': 'N₂',
        'nome_ingles': 'Nitrogen'
    },
    {
        'id': 'oxigenio_o2',
        'nome_backend': 'Oxigênio',
        'nome_display': 'Oxigênio, O₂',
        'formula': 'O₂',
        'nome_ingles': 'Oxygen'
    },
    {
        'id': 'dioxido_carbono_co2',
        'nome_backend': 'CO2',
        'nome_display': 'Dióxido de Carbono, CO₂',
        'formula': 'CO₂',
        'nome_ingles': 'Carbon dioxide'
    }
]

# Lista de nomes para o backend (manter compatibilidade)
COMPONENTES_BACKEND = [comp['nome_backend'] for comp in COMPONENTES_OFICIAIS]

# Lista de nomes para display nas telas
COMPONENTES_DISPLAY = [comp['nome_display'] for comp in COMPONENTES_OFICIAIS]

# Mapeamento ID -> Backend
MAPA_ID_BACKEND = {comp['id']: comp['nome_backend'] for comp in COMPONENTES_OFICIAIS}

# Mapeamento Backend -> Display
MAPA_BACKEND_DISPLAY = {comp['nome_backend']: comp['nome_display'] for comp in COMPONENTES_OFICIAIS}

# Mapeamento Backend -> Fórmula
MAPA_BACKEND_FORMULA = {comp['nome_backend']: comp['formula'] for comp in COMPONENTES_OFICIAIS}


def get_componente_info(nome_backend):
    """Retorna informações completas de um componente pelo nome do backend"""
    for comp in COMPONENTES_OFICIAIS:
        if comp['nome_backend'] == nome_backend:
            return comp
    return None


def get_nome_display(nome_backend):
    """Retorna o nome para display a partir do nome do backend"""
    return MAPA_BACKEND_DISPLAY.get(nome_backend, nome_backend)


def get_formula(nome_backend):
    """Retorna a fórmula a partir do nome do backend"""
    return MAPA_BACKEND_FORMULA.get(nome_backend, '')
