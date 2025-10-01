#!/usr/bin/env python3
"""
Teste básico do AGA8 GERG2008
"""

from aga8_gerg2008 import AGA8_GERG2008


def teste_basico():
    """Teste básico do sistema AGA8"""
    print("=== TESTE BÁSICO AGA8 GERG2008 ===")
    
    solver = AGA8_GERG2008()
    print("✓ Solver inicializado")
    
    # Composição de teste (dados da imagem)
    composicao = {
        'Metano': 85.123,
        'Etano': 7.456,
        'Propano': 3.789,
        'i-Butano': 1.234,
        'n-Butano': 1.567,
        'i-Pentano': 0.345,
        'n-Pentano': 0.234,
        'Hexano': 0.156,
        'Nitrogênio': 0.096
    }
    
    try:
        # Validar composição
        valid, msg, normalized = solver.validate_composition(composicao)
        print(f"✓ Validação: {valid}")
        print(f"✓ Total normalizado: {sum(normalized.values()):.3f}%")
        
        if valid:
            # Calcular propriedades
            result = solver.calculate_properties(558.0, 50.0, normalized)
            densidade = result.get('density', 'N/A')
            print(f"✓ Densidade calculada: {densidade} kg/m³")
            print("✓ TESTE BÁSICO: SUCESSO")
            return True
        else:
            print(f"✗ Composição inválida: {msg}")
            return False
            
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = teste_basico()
    exit(0 if sucesso else 1)