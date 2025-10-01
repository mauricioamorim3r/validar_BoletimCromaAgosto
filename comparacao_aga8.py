# -*- coding: utf-8 -*-
"""
Comparação e Validação dos Métodos AGA 8 2017
Comparação entre GERG 2008 e Detailed Characterization
"""

from aga8_calibrado import AGA8_GERG2008_Calibrated
from aga8_gerg2008 import AGA8_GERG2008
from aga8_detailed_characterization import AGA8_DetailedCharacterization


def compare_aga8_methods():
    """
    Compara os resultados dos diferentes métodos AGA 8 2017
    """

    print("=" * 80)
    print("COMPARAÇÃO MÉTODOS AGA 8 2017")
    print("=" * 80)

    # Instanciar calculadores
    gerg_calibrated = AGA8_GERG2008_Calibrated()
    gerg_standard = AGA8_GERG2008()
    detailed_char = AGA8_DetailedCharacterization()

    # === TESTE 1: Composição GERG 2008 (558 kPa, 55°C) ===
    print("\n1. TESTE GERG 2008 - Composição Calibrada")
    print("-" * 50)
    print("Condições: 558 kPa, 55°C")

    composition_gerg = {
        'methane': 0.965,
        'nitrogen': 0.003,
        'carbon_dioxide': 0.006,
        'ethane': 0.018,
        'propane': 0.0045,
        'n-butane': 0.001,
        'i-butane': 0.001,
        'i-pentane': 0.0005,
        'n-pentane': 0.0003,
        'n-hexane': 0.0007
    }

    results_calibrated = gerg_calibrated.calculate_properties(558, 55, composition_gerg)
    results_standard = gerg_standard.calculate_properties(558, 55, composition_gerg)

    print(f"{'Propriedade':<25} {'Calibrado':<15} {'Padrão':<15} {'Diferença %':<12}")
    print("-" * 70)

    for prop in ['compressibility_factor', 'molar_mass', 'density']:
        if prop in results_calibrated and prop in results_standard:
            cal_val = results_calibrated[prop]
            std_val = results_standard[prop]
            diff_pct = ((cal_val - std_val) / cal_val * 100) if cal_val != 0 else 0
            print(f"{prop:<25} {cal_val:<15.6f} {std_val:<15.6f} {diff_pct:<12.3f}")

    # === TESTE 2: Composição Detailed Characterization (600 kPa, 50°C) ===
    print("\n\n2. TESTE DETAILED CHARACTERIZATION")
    print("-" * 50)
    print("Condições: 600 kPa, 50°C")

    # Composição da imagem
    composition_dc = {
        'methane': 96.5,
        'nitrogen': 0.3,
        'carbon_dioxide': 0.6,
        'ethane': 1.8,
        'propane': 0.45,
        'i_butane': 0.1,
        'n_butane': 0.1,
        'i_pentane': 0.05,
        'n_pentane': 0.03,
        'n_hexane': 0.07
    }

    # Converter para frações molares
    composition_dc_fractions = {k: v / 100.0 for k, v in composition_dc.items()}

    # Calcular com todos os métodos
    results_dc = detailed_char.calculate_all_properties(600, 50, composition_dc_fractions)

    # Para GERG, mapear componentes
    composition_gerg_mapped = {
        'methane': composition_dc_fractions['methane'],
        'nitrogen': composition_dc_fractions['nitrogen'],
        'carbon_dioxide': composition_dc_fractions['carbon_dioxide'],
        'ethane': composition_dc_fractions['ethane'],
        'propane': composition_dc_fractions['propane'],
        'n-butane': composition_dc_fractions['n_butane'],
        'i-butane': composition_dc_fractions['i_butane'],
        'i-pentane': composition_dc_fractions['i_pentane'],
        'n-pentane': composition_dc_fractions['n_pentane'],
        'n-hexane': composition_dc_fractions['n_hexane']
    }

    results_gerg_dc = gerg_standard.calculate_properties(600, 50, composition_gerg_mapped)

    print("\nRESULTADOS DETAILED CHARACTERIZATION:")
    print(f"{'Propriedade':<35} {'Valor':<15} {'Unidade':<10}")
    print("-" * 60)

    properties_display = {
        'compressibility_factor': ('Fator de Compressibilidade', '', 6),
        'molar_mass': ('Massa Molar', 'g/mol', 4),
        'density': ('Densidade', 'kg/m³', 4),
        'heating_value_superior_mass': ('PCS (base mássica)', 'kJ/kg', 1),
        'heating_value_inferior_mass': ('PCI (base mássica)', 'kJ/kg', 1),
        'wobbe_index_superior': ('Índice Wobbe Superior', 'kJ/m³', 1),
        'methane_number': ('Número de Metano', '', 1),
        'specific_gravity': ('Densidade Relativa', '', 4)
    }

    for prop_key, (name, unit, decimals) in properties_display.items():
        if prop_key in results_dc:
            value = results_dc[prop_key]
            print(f"{name:<35} {value:<15.{decimals}f} {unit:<10}")

    # Comparação GERG vs DC para propriedades comuns
    print("\n\nCOMPARAÇÃO GERG vs DETAILED CHARACTERIZATION:")
    print(f"{'Propriedade':<25} {'GERG':<15} {'D.C.':<15} {'Diferença %':<12}")
    print("-" * 70)

    comparison_props = {
        'compressibility_factor': 'compressibility_factor',
        'molar_mass': 'molar_mass',
        'density': 'density'
    }

    for gerg_prop, dc_prop in comparison_props.items():
        if gerg_prop in results_gerg_dc and dc_prop in results_dc:
            gerg_val = results_gerg_dc[gerg_prop]
            dc_val = results_dc[dc_prop]
            diff_pct = ((dc_val - gerg_val) / dc_val * 100) if dc_val != 0 else 0
            print(f"{gerg_prop:<25} {gerg_val:<15.6f} {dc_val:<15.6f} {diff_pct:<12.3f}")

    # === ANÁLISE DE APLICABILIDADE ===
    print("\n\n3. ANÁLISE DE APLICABILIDADE")
    print("-" * 50)

    print("\nGERG 2008 (AGA 8 Part 2):")
    print("• Composições de gás natural com até 21 componentes")
    print("• Pressões: 0-70 MPa")
    print("• Temperaturas: 90-450 K")
    print("• Incerteza: ±0.1% para densidade")
    print("• Ideal para: Medição fiscal, custódia")

    print("\nDetailed Characterization (AGA 8 D.C.):")
    print("• Análise detalhada de hidrocarbonetos pesados")
    print("• Melhor para gases com C6+ significativo")
    print("• Cálculos de propriedades termodinâmicas estendidas")
    print("• Ideal para: Processamento, engenharia")

    # === RECOMENDAÇÕES ===
    print("\n\n4. RECOMENDAÇÕES DE USO")
    print("-" * 50)

    methane_content = composition_dc['methane']
    heavy_content = sum([composition_dc.get(comp, 0) for comp in ['n_hexane', 'n_heptane', 'n_octane']])

    print("Composição analisada:")
    print(f"• Metano: {methane_content:.1f}%")
    print(f"• Pesados (C6+): {heavy_content:.2f}%")

    if methane_content > 85 and heavy_content < 2:
        print("\n🟢 RECOMENDAÇÃO: GERG 2008")
        print("   - Composição típica de gás natural")
        print("   - GERG 2008 oferece precisão adequada")
        print("   - Menor complexidade computacional")
    else:
        print("\n🟡 RECOMENDAÇÃO: Detailed Characterization")
        print("   - Composição com componentes pesados significativos")
        print("   - D.C. fornece melhor precisão para C6+")
        print("   - Análise termodinâmica mais completa")

    print("\n" + "=" * 80)

    return {
        'gerg_calibrated': results_calibrated,
        'gerg_standard': results_standard,
        'detailed_char': results_dc,
        'gerg_dc_conditions': results_gerg_dc
    }


if __name__ == "__main__":
    results = compare_aga8_methods()
