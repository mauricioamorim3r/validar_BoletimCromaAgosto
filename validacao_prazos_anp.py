"""
Módulo de Validação de Prazos ANP - Regulamento Técnico 52
Sistema de Validação de Boletins Cromatográficos - BRAVA Energia

Prazos Regulamentários:
- Coleta → Análise → Emissão: 25 dias (Portaria 52 ANP)
- Emissão → Implementação/validação: 1 dia quando não houver validação (Portaria 52 ANP)
- Total (Coleta → Implementação/validação): 28 dias (Portaria 52 ANP)
"""

from datetime import datetime
from typing import Dict


def calcular_dias_uteis(data_inicial: str, data_final: str) -> int:
    """
    Calcula a diferença em dias entre duas datas

    Args:
        data_inicial: Data no formato 'YYYY-MM-DD'
        data_final: Data no formato 'YYYY-MM-DD'

    Returns:
        int: Número de dias de diferença
    """
    try:
        dt_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
        dt_final = datetime.strptime(data_final, '%Y-%m-%d')
        return (dt_final - dt_inicial).days
    except (ValueError, TypeError):
        return 0


def validar_prazo_coleta_emissao(data_coleta: str, data_emissao: str) -> Dict:
    """
    Valida o prazo entre coleta e emissão (máximo 25 dias)

    Args:
        data_coleta: Data de coleta no formato 'YYYY-MM-DD'
        data_emissao: Data de emissão no formato 'YYYY-MM-DD'

    Returns:
        Dict contendo status, dias_decorridos, prazo_limite e mensagem
    """
    if not data_coleta or not data_emissao:
        return {
            'status': 'PENDENTE',
            'dias_decorridos': None,
            'prazo_limite': 25,
            'dias_restantes': None,
            'mensagem': 'Datas não informadas',
            'regulamento': 'Portaria 52 ANP'
        }

    dias_decorridos = calcular_dias_uteis(data_coleta, data_emissao)
    prazo_limite = 25

    if dias_decorridos <= prazo_limite:
        status = 'CONFORME'
        mensagem = f'Dentro do prazo ({dias_decorridos}/{prazo_limite} dias)'
    else:
        status = 'NÃO CONFORME'
        dias_excesso = dias_decorridos - prazo_limite
        mensagem = f'Excedeu o prazo em {dias_excesso} dias ({dias_decorridos}/{prazo_limite})'

    return {
        'status': status,
        'dias_decorridos': dias_decorridos,
        'prazo_limite': prazo_limite,
        'dias_restantes': max(0, prazo_limite - dias_decorridos),
        'mensagem': mensagem,
        'regulamento': 'Portaria 52 ANP'
    }


def validar_prazo_emissao_validacao(data_emissao: str, data_validacao: str = None, metodologia_aprovada: bool = False) -> Dict:
    """
    Valida o prazo entre emissão e validação conforme Portaria 52 ANP
    
    Regras:
    - Máximo 1 dia útil (quando não existir metodologia de validação aprovada)
    - Máximo 3 dias úteis (quando existir metodologia de validação aprovada)

    Args:
        data_emissao: Data de emissão no formato 'YYYY-MM-DD'
        data_validacao: Data de validação no formato 'YYYY-MM-DD' (opcional)
        metodologia_aprovada: Se existe metodologia de validação aprovada (boolean)

    Returns:
        Dict contendo status, dias_decorridos, prazo_limite e mensagem
    """
    if not data_emissao:
        return {
            'status': 'PENDENTE',
            'dias_decorridos': None,
            'prazo_limite': 3 if metodologia_aprovada else 1,
            'dias_restantes': None,
            'mensagem': 'Data de emissão não informada',
            'regulamento': 'Portaria 52 ANP'
        }

    # Se não há data de validação, usar data atual
    if not data_validacao:
        data_validacao = datetime.now().strftime('%Y-%m-%d')

    dias_decorridos = calcular_dias_uteis(data_emissao, data_validacao)
    
    # Definir prazo limite baseado na metodologia
    if metodologia_aprovada:  
        prazo_limite = 3
        tipo_prazo = "3 dias úteis (com metodologia aprovada)"
    else:
        prazo_limite = 1
        tipo_prazo = "1 dia útil (sem metodologia aprovada)"

    if dias_decorridos <= prazo_limite:
        status = 'CONFORME'
        if dias_decorridos == 1:
            mensagem = f'Dentro do prazo ({dias_decorridos} dia de {tipo_prazo})'
        else:
            mensagem = f'Dentro do prazo ({dias_decorridos} dias de {tipo_prazo})'
    else:
        status = 'NÃO CONFORME'
        dias_excesso = dias_decorridos - prazo_limite
        if dias_excesso == 1:
            mensagem = f'Excedeu o prazo em {dias_excesso} dia ({dias_decorridos} dias de {tipo_prazo})'
        else:
            mensagem = f'Excedeu o prazo em {dias_excesso} dias ({dias_decorridos} dias de {tipo_prazo})'

    return {
        'status': status,
        'dias_decorridos': dias_decorridos,
        'prazo_limite': prazo_limite,
        'dias_restantes': max(0, prazo_limite - dias_decorridos),
        'mensagem': mensagem,
        'metodologia_aprovada': metodologia_aprovada,
        'tipo_prazo': tipo_prazo,
        'regulamento': 'Portaria 52 ANP'
    }


def validar_prazo_total(data_coleta: str, data_validacao: str = None) -> Dict:
    """
    Valida o prazo total entre coleta e validação (máximo 28 dias)

    Args:
        data_coleta: Data de coleta no formato 'YYYY-MM-DD'
        data_validacao: Data de validação no formato 'YYYY-MM-DD' (opcional)

    Returns:
        Dict contendo status, dias_decorridos, prazo_limite e mensagem
    """
    if not data_coleta:
        return {
            'status': 'PENDENTE',
            'dias_decorridos': None,
            'prazo_limite': 28,
            'dias_restantes': None,
            'mensagem': 'Data de coleta não informada',
            'regulamento': 'Portaria 52 ANP'
        }

    # Se não há data de validação, usar data atual
    if not data_validacao:
        data_validacao = datetime.now().strftime('%Y-%m-%d')

    dias_decorridos = calcular_dias_uteis(data_coleta, data_validacao)
    prazo_limite = 28

    if dias_decorridos <= prazo_limite:
        status = 'CONFORME'
        mensagem = f'Dentro do prazo total ({dias_decorridos}/{prazo_limite} dias)'
    else:
        status = 'NÃO CONFORME'
        dias_excesso = dias_decorridos - prazo_limite
        mensagem = f'Excedeu o prazo total em {dias_excesso} dias ({dias_decorridos}/{prazo_limite})'

    return {
        'status': status,
        'dias_decorridos': dias_decorridos,
        'prazo_limite': prazo_limite,
        'dias_restantes': max(0, prazo_limite - dias_decorridos),
        'mensagem': mensagem,
        'regulamento': 'Portaria 52 ANP'
    }


def validar_todos_prazos_anp(data_coleta: str, data_analise: str = None,
                             data_emissao: str = None, data_validacao: str = None, 
                             metodologia_aprovada: bool = False) -> Dict:
    """
    Executa todas as validações de prazo ANP para um boletim

    Args:
        data_coleta: Data de coleta no formato 'YYYY-MM-DD'
        data_analise: Data de análise no formato 'YYYY-MM-DD' (opcional)
        data_emissao: Data de emissão no formato 'YYYY-MM-DD' (opcional)
        data_validacao: Data de validação no formato 'YYYY-MM-DD' (opcional)
        metodologia_aprovada: Se existe metodologia de validação aprovada (boolean)

    Returns:
        Dict contendo todas as validações de prazo
    """
    resultado = {
        'prazo_coleta_emissao': {},
        'prazo_emissao_validacao': {},
        'prazo_total': {},
        'status_geral': 'CONFORME',
        'alertas': [],
        'resumo': {},
        'metodologia_aprovada': metodologia_aprovada
    }

    # Validação Coleta → Emissão (25 dias)
    if data_coleta and data_emissao:
        resultado['prazo_coleta_emissao'] = validar_prazo_coleta_emissao(data_coleta, data_emissao)
        if resultado['prazo_coleta_emissao']['status'] == 'NÃO CONFORME':
            resultado['status_geral'] = 'NÃO CONFORME'
            resultado['alertas'].append('Prazo coleta → emissão excedido')

    # Validação Emissão → Validação (1 ou 3 dias úteis conforme metodologia)
    if data_emissao:
        resultado['prazo_emissao_validacao'] = validar_prazo_emissao_validacao(data_emissao, data_validacao, metodologia_aprovada)
        if resultado['prazo_emissao_validacao']['status'] == 'NÃO CONFORME':
            resultado['status_geral'] = 'NÃO CONFORME'
            resultado['alertas'].append('Prazo emissão → validação excedido')

    # Validação Prazo Total (28 dias)
    if data_coleta:
        resultado['prazo_total'] = validar_prazo_total(data_coleta, data_validacao)
        if resultado['prazo_total']['status'] == 'NÃO CONFORME':
            resultado['status_geral'] = 'NÃO CONFORME'
            resultado['alertas'].append('Prazo total excedido')

    # Resumo
    resultado['resumo'] = {
        'total_verificacoes': len([k for k in resultado.keys() if k.startswith('prazo_') and resultado[k]]),
        'conformes': len([k for k in resultado.keys() if k.startswith('prazo_') and resultado[k].get('status') == 'CONFORME']),
        'nao_conformes': len([k for k in resultado.keys() if k.startswith('prazo_') and resultado[k].get('status') == 'NÃO CONFORME']),
        'pendentes': len([k for k in resultado.keys() if k.startswith('prazo_') and resultado[k].get('status') == 'PENDENTE'])
    }

    return resultado


def gerar_classe_css_prazo(status: str) -> str:
    """
    Gera a classe CSS apropriada baseada no status do prazo

    Args:
        status: Status da validação ('CONFORME', 'NÃO CONFORME', 'PENDENTE')

    Returns:
        str: Classe CSS
    """
    classes = {
        'CONFORME': 'text-success',
        'NÃO CONFORME': 'text-danger',
        'PENDENTE': 'text-warning'
    }
    return classes.get(status, 'text-muted')


def gerar_badge_prazo(status: str) -> str:
    """
    Gera o badge HTML apropriado baseado no status do prazo

    Args:
        status: Status da validação ('CONFORME', 'NÃO CONFORME', 'PENDENTE')

    Returns:
        str: HTML do badge
    """
    badges = {
        'CONFORME': '<span class="badge bg-success">✓ CONFORME</span>',
        'NÃO CONFORME': '<span class="badge bg-danger">✗ NÃO CONFORME</span>',
        'PENDENTE': '<span class="badge bg-warning">⏳ PENDENTE</span>'
    }
    return badges.get(status, '<span class="badge bg-secondary">-</span>')


# Função para teste
if __name__ == '__main__':
    # Teste das funções
    print("=== TESTE DE VALIDAÇÃO DE PRAZOS ANP ===")

    # Teste 1: Prazo dentro do limite
    data_coleta = '2025-08-01'
    data_emissao = '2025-08-20'
    data_validacao = '2025-08-21'

    resultado = validar_todos_prazos_anp(data_coleta, None, data_emissao, data_validacao)
    print("\nTeste 1 - Dentro do prazo:")
    print(f"Status Geral: {resultado['status_geral']}")
    print(f"Alertas: {resultado['alertas']}")

    # Teste 2: Prazo excedido
    data_coleta = '2025-07-01'
    data_emissao = '2025-08-10'  # 40 dias depois
    data_validacao = '2025-08-15'

    resultado = validar_todos_prazos_anp(data_coleta, None, data_emissao, data_validacao)
    print("\nTeste 2 - Prazo excedido:")
    print(f"Status Geral: {resultado['status_geral']}")
    print(f"Alertas: {resultado['alertas']}")
