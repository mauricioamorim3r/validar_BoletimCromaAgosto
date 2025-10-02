#!/usr/bin/env python3
"""
Teste Simplificado AGA8 - Verificação Básica
Teste com composição mais simples primeiro
"""

import os
import sys

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from aga8_detailed_characterization import AGA8_DetailedCharacterization
    from aga8_gerg2008 import AGA8_GERG2008
except ImportError as e:
    print(f"❌ ERRO: Não foi possível importar os módulos AGA8: {e}")
    sys.exit(1)

def teste_aga8_simples():
    """Teste com composição simplificada"""
    print("🔬 TESTE AGA8 SIMPLIFICADO")
    print("=" * 40)
    
    # Condições da imagem
    pressao_kpa = 550.0  # kPa
    temperatura_c = 220.0 - 273.15  # Converter K para C = -53.15°C
    
    print(f"Condições:")
    print(f"  Pressão: {pressao_kpa} kPa")
    print(f"  Temperatura: {temperatura_c:.2f}°C ({temperatura_c + 273.15:.2f} K)")
    
    # Composição simplificada baseada na imagem (apenas componentes principais)
    composicao = {
        'CH4': 76.6,    # Metano - componente principal
        'N2': 2.0,      # Nitrogênio
        'CO2': 1.0,     # Dióxido de carbono
        'C2H6': 1.0,    # Etano
        'C3H8': 1.0,    # Propano
        'O2': 2.0,      # Oxigênio
        'He': 1.0,      # Hélio
        # Total: 84.6% - vamos normalizar
    }
    
    # Normalizar para 100%
    total = sum(composicao.values())
    for comp in composicao:
        composicao[comp] = (composicao[comp] / total) * 100
    
    print(f"\nComposição normalizada:")
    for comp, valor in composicao.items():
        print(f"  {comp}: {valor:.3f}%")
    print(f"  Total: {sum(composicao.values()):.3f}%")
    
    # Teste AGA8 Detailed Characterization
    try:
        print(f"\n📊 TESTE AGA8 DETAILED CHARACTERIZATION:")
        aga8 = AGA8_DetailedCharacterization()
        
        # Calcular propriedades
        resultado = aga8.calculate_all_properties(
            pressure_kpa=pressao_kpa,
            temperature_c=temperatura_c,
            composition=composicao
        )
        
        print(f"✅ RESULTADOS AGA8 Detailed:")
        for key, value in resultado.items():
            if isinstance(value, (int, float)):
                print(f"   {key}: {value:.6f}")
            else:
                print(f"   {key}: {value}")
                
    except Exception as e:
        print(f"❌ ERRO AGA8 Detailed: {e}")
        import traceback
        traceback.print_exc()
    
    # Teste AGA8 GERG-2008
    try:
        print(f"\n📊 TESTE AGA8 GERG-2008:")
        aga8_gerg = AGA8_GERG2008()
        
        # Calcular propriedades
        resultado_gerg = aga8_gerg.calculate_gas_properties(
            pressure_kpa=pressao_kpa,
            temperature_c=temperatura_c,
            composition=composicao
        )
        
        print(f"✅ RESULTADOS AGA8 GERG:")
        for key, value in resultado_gerg.items():
            if isinstance(value, (int, float)):
                print(f"   {key}: {value:.6f}")
            else:
                print(f"   {key}: {value}")
                
    except Exception as e:
        print(f"❌ ERRO AGA8 GERG: {e}")
        import traceback
        traceback.print_exc()

def teste_aga8_completo():
    """Teste com a composição completa da imagem"""
    print(f"\n🔬 TESTE AGA8 COMPOSIÇÃO COMPLETA")
    print("=" * 40)
    
    # Condições da imagem
    pressao_kpa = 550.0
    temperatura_c = -53.15  # 220K em Celsius
    
    # Composição completa da imagem
    composicao_completa = {
        'CH4': 76.6,     # Metano
        'N2': 2.0,       # Nitrogênio  
        'CO2': 1.0,      # CO2
        'C2H6': 1.0,     # Etano
        'C3H8': 1.0,     # Propano
        'iC4H10': 1.0,   # iso-Butano
        'nC4H10': 1.0,   # n-Butano
        'iC5H12': 1.0,   # iso-Pentano
        'nC5H12': 1.0,   # n-Pentano
        'nC6H14': 1.0,   # n-Hexano
        'nC7H16': 1.0,   # n-Heptano
        'nC8H18': 1.0,   # n-Octano
        'nC9H20': 1.0,   # n-Nonano
        'nC10H22': 1.0,  # n-Decano
        'O2': 2.0,       # Oxigênio
        'CO': 1.0,       # CO
        'H2O': 1.0,      # Água
        'H2S': 1.0,      # H2S
        'He': 1.0,       # Hélio
        # Argônio seria o restante para completar 99.6%
    }
    
    # Calcular total atual
    total_atual = sum(composicao_completa.values())
    faltante = 99.6 - total_atual
    composicao_completa['Ar'] = faltante if faltante > 0 else 0
    
    print(f"Composição completa (total: {sum(composicao_completa.values()):.1f}%):")
    for comp, valor in composicao_completa.items():
        if valor > 0:
            print(f"  {comp}: {valor:.1f}%")
    
    try:
        aga8 = AGA8_DetailedCharacterization()
        resultado = aga8.calculate_all_properties(
            pressure_kpa=pressao_kpa,
            temperature_c=temperatura_c,
            composition=composicao_completa
        )
        
        print(f"\n✅ RESULTADOS COMPOSIÇÃO COMPLETA:")
        print(f"   Fator Z: {resultado.get('compressibility_factor', 'N/A')}")
        print(f"   Densidade: {resultado.get('density_kg_m3', 'N/A')} kg/m³")
        print(f"   PCS: {resultado.get('higher_heating_value', 'N/A')} MJ/m³")
        
    except Exception as e:
        print(f"❌ ERRO composição completa: {e}")

if __name__ == "__main__":
    teste_aga8_simples()
    teste_aga8_completo()