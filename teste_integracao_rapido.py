#!/usr/bin/env python3
"""
Teste rápido de integração dos módulos AGA8
"""

from aga8_dc_calibrado import AGA8_DetailedCharacterization_Calibrated


def teste_integracao():
    """Teste básico de integração"""
    print("=== TESTE DE INTEGRAÇÃO AGA8 ===")
    
    # Inicializar solver
    solver = AGA8_DetailedCharacterization_Calibrated()
    print("✓ Solver inicializado")
    
    # Composição de teste
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
        # Teste de cálculo
        resultado = solver.calculate_all_properties_calibrated(
            pressure_kpa=558.0,
            temperature_c=50.0,
            composition=composicao
        )
        print("✓ Cálculo executado com sucesso")
        
        # Verificar resultados básicos
        densidade = resultado.get('density_kg_m3')
        fator_z = resultado.get('compressibility_factor')
        
        if densidade and fator_z:
            print(f"✓ Densidade: {densidade:.3f} kg/m³")
            print(f"✓ Fator Z: {fator_z:.6f}")
            print("✓ TESTE DE INTEGRAÇÃO: SUCESSO")
            return True
        else:
            print("✗ Resultados incompletos")
            return False
            
    except Exception as e:
        print(f"✗ Erro no cálculo: {e}")
        return False


if __name__ == "__main__":
    sucesso = teste_integracao()
    exit(0 if sucesso else 1)