#!/usr/bin/env python3
"""
Teste Comparativo - AGA8 Gross vs Nossos Métodos
Condições: 550 kPa, 50°C
Aguardando resultados do método Gross para comparação
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from aga8_gerg2008 import AGA8_GERG2008
    from teste_aga8_detailed_corrigido import converter_composicao
    from aga8_detailed_characterization import AGA8_DetailedCharacterization
except ImportError as e:
    print(f"❌ ERRO: Não foi possível importar módulos AGA8: {e}")
    sys.exit(1)

def teste_preparatorio_gross():
    """Teste preparatório com nossos métodos para comparação com AGA8 Gross"""
    print("🔬 TESTE PREPARATÓRIO - AGA8 GROSS vs NOSSOS MÉTODOS")
    print("=" * 70)
    
    # Condições do memorial AGA8 Gross
    pressao_kpa = 550.0      # kPa absolute
    temperatura_c = 50.0     # °C
    base_pressure_bar = 1.01325    # bar
    base_temperature_c = 15.0      # °C
    
    print(f"📋 MEMORIAL AGA8 2017 Gross:")
    print(f"   Data: 02/10/25")
    print(f"   Hora: 18:50:40")
    print(f"   Site: hsw")
    print(f"   Método: AGA8 2017 Gross")
    print(f"   Pressão: {pressao_kpa} kPa absolute")
    print(f"   Temperatura: {temperatura_c}°C")
    print(f"   Base Conditions: {base_pressure_bar} bar/{base_temperature_c}°C")
    
    # Composição
    composicao_gross = {
        'CH4': 96.5,     # Methane
        'N2': 0.3,       # Nitrogen  
        'CO2': 0.6,      # Carbon Dioxide
        'C2H6': 1.8,     # Ethane
        'C3H8': 0.45,    # Propane
        'H2O': 0.0,      # Water
        'H2S': 0.0,      # Hydrogen Sulfide
        'H2': 0.0,       # Hydrogen
        'CO': 0.0,       # Carbon Monoxide
        'O2': 0.0,       # Oxygen
        'iC4H10': 0.1,   # iso-Butane
        'nC4H10': 0.1,   # n-Butane
        'iC5H12': 0.05,  # iso-Pentano
        'nC5H12': 0.03,  # n-Pentano
        'nC6H14': 0.07,  # n-Hexano
        'nC7H16': 0.0,   # n-Heptano
        'nC8H18': 0.0,   # n-Octano
        'nC9H20': 0.0,   # n-Nonano
        'nC10H22': 0.0,  # n-Decano
        'He': 0.0,       # Helium
        'Ar': 0.0        # Argon
    }
    
    soma_comp = sum(v for v in composicao_gross.values() if v > 0)
    print(f"\n🧪 COMPOSIÇÃO: {soma_comp}% total")
    
    # Executar com nossos métodos disponíveis
    print(f"\n🔬 EXECUTANDO NOSSOS MÉTODOS PARA COMPARAÇÃO:")
    print("=" * 70)
    
    resultados = {}
    
    # 1. AGA8 GERG-2008
    print(f"\n1️⃣ AGA8 GERG-2008:")
    print("-" * 30)
    try:
        aga8_gerg = AGA8_GERG2008()
        resultado_gerg = aga8_gerg.calculate_gas_properties(
            pressure_kpa=pressao_kpa,
            temperature_c=temperatura_c,
            composition=composicao_gross
        )
        
        # Extrair valores principais
        gerg_valores = {}
        if 'density_properties' in resultado_gerg:
            dp = resultado_gerg['density_properties']
            gerg_valores['z_factor'] = dp.get('compressibility_factor')
            gerg_valores['densidade'] = dp.get('density_kg_m3')
            gerg_valores['densidade_relativa'] = dp.get('relative_density')
        
        if 'mixture_properties' in resultado_gerg:
            mp = resultado_gerg['mixture_properties']
            gerg_valores['massa_molar'] = mp.get('molecular_weight')
            
            # Densidade molar
            if gerg_valores.get('densidade') and gerg_valores.get('massa_molar'):
                gerg_valores['densidade_molar'] = (gerg_valores['densidade'] * 1000) / gerg_valores['massa_molar']
        
        # Exibir resultados
        for prop, valor in gerg_valores.items():
            if valor is not None:
                if 'factor' in prop or 'z_' in prop:
                    print(f"   {prop}: {valor:.8f}")
                elif 'densidade' in prop or 'massa' in prop:
                    print(f"   {prop}: {valor:.6f}")
                else:
                    print(f"   {prop}: {valor:.4f}")
        
        resultados['gerg'] = gerg_valores
        print(f"   Status: ✅ Sucesso")
        
    except Exception as e:
        print(f"   Status: ❌ Erro: {e}")
        resultados['gerg'] = None
    
    # 2. AGA8 Detailed Characterization
    print(f"\n2️⃣ AGA8 Detailed Characterization:")
    print("-" * 40)
    try:
        aga8_detailed = AGA8_DetailedCharacterization()
        composicao_convertida = converter_composicao(composicao_gross)
        
        resultado_detailed = aga8_detailed.calculate_all_properties(
            pressao_kpa, temperatura_c, composicao_convertida
        )
        
        # Extrair valores principais
        detailed_valores = {
            'z_factor': resultado_detailed.get('compressibility_factor'),
            'massa_molar': resultado_detailed.get('molar_mass'),
            'densidade': resultado_detailed.get('density')
        }
        
        # Calcular densidade molar e relativa
        if detailed_valores.get('densidade') and detailed_valores.get('massa_molar'):
            detailed_valores['densidade_molar'] = (detailed_valores['densidade'] * 1000) / detailed_valores['massa_molar']
            detailed_valores['densidade_relativa'] = detailed_valores['massa_molar'] / 28.9647
        
        # Exibir resultados
        for prop, valor in detailed_valores.items():
            if valor is not None:
                if 'factor' in prop or 'z_' in prop:
                    print(f"   {prop}: {valor:.8f}")
                elif 'densidade' in prop or 'massa' in prop:
                    print(f"   {prop}: {valor:.6f}")
                else:
                    print(f"   {prop}: {valor:.4f}")
        
        resultados['detailed'] = detailed_valores
        print(f"   Status: ✅ Sucesso")
        
    except Exception as e:
        print(f"   Status: ❌ Erro: {e}")
        resultados['detailed'] = None
    
    # Comparação entre nossos métodos
    if resultados.get('gerg') and resultados.get('detailed'):
        print(f"\n🔍 COMPARAÇÃO ENTRE NOSSOS MÉTODOS:")
        print("-" * 50)
        
        gerg_vals = resultados['gerg']
        detailed_vals = resultados['detailed']
        
        propriedades_comparaveis = ['z_factor', 'massa_molar', 'densidade', 'densidade_molar']
        
        for prop in propriedades_comparaveis:
            if prop in gerg_vals and prop in detailed_vals:
                val_gerg = gerg_vals[prop]
                val_detailed = detailed_vals[prop]
                
                if val_gerg and val_detailed:
                    desvio = abs(val_gerg - val_detailed)
                    desvio_perc = (desvio / val_gerg) * 100
                    
                    print(f"{prop}:")
                    print(f"   GERG-2008:  {val_gerg:.8f}")
                    print(f"   Detailed:   {val_detailed:.8f}")
                    print(f"   Diferença:  {desvio:.8f} ({desvio_perc:.4f}%)")
                    
                    if desvio_perc < 0.1:
                        print(f"   Status:     ✅ EXCELENTE concordância")
                    elif desvio_perc < 1.0:
                        print(f"   Status:     ⚠️  BOA concordância")
                    else:
                        print(f"   Status:     ❌ Diferença significativa")
                    print()
    
    # Posicionamento para comparação com Gross
    print(f"\n📊 RESUMO PARA COMPARAÇÃO COM AGA8 GROSS:")
    print("=" * 70)
    print(f"Condições: 550 kPa, 50°C")
    print(f"Composição: 96.5% CH4 + outros")
    print(f"Base Conditions: 1.01325 bar/15°C")
    
    if resultados.get('gerg'):
        print(f"\nNosso GERG-2008:")
        for prop, valor in resultados['gerg'].items():
            if valor is not None:
                if 'factor' in prop:
                    print(f"   {prop}: {valor:.8f}")
                elif 'densidade' in prop or 'massa' in prop:
                    print(f"   {prop}: {valor:.6f}")
    
    if resultados.get('detailed'):
        print(f"\nNosso Detailed:")
        for prop, valor in resultados['detailed'].items():
            if valor is not None:
                if 'factor' in prop:
                    print(f"   {prop}: {valor:.8f}")
                elif 'densidade' in prop or 'massa' in prop:
                    print(f"   {prop}: {valor:.6f}")
    
    print(f"\n🔄 AGUARDANDO RESULTADOS DO AGA8 GROSS PARA COMPARAÇÃO...")
    
    return resultados

def analise_condicoes():
    """Análise das condições do teste"""
    print(f"\n🌡️  ANÁLISE DAS CONDIÇÕES:")
    print("-" * 50)
    print(f"Teste Atual (550 kPa, 50°C) vs Anteriores:")
    print(f"   vs Teste 555 kPa, 50°C: Pressão ligeiramente menor")
    print(f"   vs Teste 500 kPa, 55°C: Pressão maior, temperatura menor")
    print(f"   Esperado: Propriedades intermediárias")
    
    print(f"\n🎯 DIFERENCIAL DO MÉTODO GROSS:")
    print(f"   • Método otimizado para cálculos rápidos")
    print(f"   • Menor complexidade computacional")
    print(f"   • Precisão adequada para aplicações industriais")
    print(f"   • Base conditions definidas explicitamente")

if __name__ == "__main__":
    print("🚀 INICIANDO TESTE PREPARATÓRIO PARA COMPARAÇÃO COM AGA8 GROSS")
    resultados = teste_preparatorio_gross()
    analise_condicoes()
    
    if any(resultados.values()):
        print(f"\n✅ TESTE PREPARATÓRIO CONCLUÍDO!")
        print(f"📋 Resultados prontos para comparação com AGA8 Gross")
    else:
        print(f"\n❌ TESTE PREPARATÓRIO FALHOU")