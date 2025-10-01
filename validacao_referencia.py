# -*- coding: utf-8 -*-
"""
Validação dos Resultados AGA 8 D.C. com Valores de Referência
Comparação com os resultados reais fornecidos
"""

from aga8_detailed_characterization import AGA8_DetailedCharacterization


def validate_against_reference():
    """
    Valida os resultados calculados contra os valores de referência reais
    """
    
    print("=" * 80)
    print("VALIDAÇÃO AGA 8 D.C. - COMPARAÇÃO COM RESULTADOS REAIS")
    print("=" * 80)
    
    # Valores de referência da imagem (600 kPa, 50°C)
    reference_results = {
        'compressibility_factor': 0.991694176393,
        'molar_mass': 16.8035819,  # g/mol
        'molar_density': 0.225181478098,  # mol/l
        'energy': -1827.670380590821,  # J/mol
        'enthalpy': 836.847158350783,  # J/mol
        'entropy': -10.3147662466246,  # J/mol.K
        'isochoric_heat_capacity': 29.2971136444434,  # J/mol.K
        'isobaric_heat_capacity': 38.0200910586759,  # J/mol.K
        'speed_of_sound': 451.754505636409,  # m/s
        'gibbs_energy': 4170.06387094551,  # J/mol
        'joule_thomson_coefficient': 0.00383362800467,  # K/KPa
        'isentropic_exponent': 1.28702881184662
    }
    
    # Calcular com nossa implementação
    aga8_dc = AGA8_DetailedCharacterization()
    
    # Composição da imagem (600 kPa, 50°C)
    composition = {
        'methane': 96.5 / 100,
        'nitrogen': 0.3 / 100,
        'carbon_dioxide': 0.6 / 100,
        'ethane': 1.8 / 100,
        'propane': 0.45 / 100,
        'i_butane': 0.1 / 100,
        'n_butane': 0.1 / 100,
        'i_pentane': 0.05 / 100,
        'n_pentane': 0.03 / 100,
        'n_hexane': 0.07 / 100
    }
    
    our_results = aga8_dc.calculate_all_properties(600, 50, composition)
    
    print("COMPARAÇÃO DE RESULTADOS:")
    print("-" * 80)
    print(f"{'Propriedade':<30} {'Referência':<20} {'Nossa Impl.':<20} {'Diferença %':<15}")
    print("-" * 80)
    
    # Comparar fator de compressibilidade
    ref_z = reference_results['compressibility_factor']
    our_z = our_results['compressibility_factor']
    diff_z = ((our_z - ref_z) / ref_z) * 100
    print(f"{'Compressibility Factor':<30} {ref_z:<20.10f} {our_z:<20.10f} {diff_z:<15.3f}")
    
    # Comparar massa molar
    ref_m = reference_results['molar_mass']
    our_m = our_results['molar_mass']
    diff_m = ((our_m - ref_m) / ref_m) * 100
    print(f"{'Molar Mass (g/mol)':<30} {ref_m:<20.7f} {our_m:<20.7f} {diff_m:<15.3f}")
    
    # Calcular densidade molar a partir da nossa densidade
    # nossa densidade está em kg/m³, converter para mol/l
    our_molar_density = (our_results['density'] * 1000) / our_results['molar_mass']  # mol/l
    ref_molar_density = reference_results['molar_density']
    diff_molar_density = ((our_molar_density - ref_molar_density) / ref_molar_density) * 100
    print(f"{'Molar Density (mol/l)':<30} {ref_molar_density:<20.10f} {our_molar_density:<20.10f} {diff_molar_density:<15.3f}")
    
    print("\n" + "=" * 80)
    
    # Análise dos resultados
    print("ANÁLISE DOS RESULTADOS:")
    print("-" * 40)
    
    if abs(diff_z) < 0.5:
        print(f"✅ Fator de Compressibilidade: EXCELENTE ({abs(diff_z):.3f}% diferença)")
    elif abs(diff_z) < 2.0:
        print(f"🟡 Fator de Compressibilidade: BOM ({abs(diff_z):.3f}% diferença)")
    else:
        print(f"❌ Fator de Compressibilidade: NECESSITA AJUSTE ({abs(diff_z):.3f}% diferença)")
    
    if abs(diff_m) < 0.1:
        print(f"✅ Massa Molar: EXCELENTE ({abs(diff_m):.3f}% diferença)")
    elif abs(diff_m) < 1.0:
        print(f"🟡 Massa Molar: BOM ({abs(diff_m):.3f}% diferença)")
    else:
        print(f"❌ Massa Molar: NECESSITA AJUSTE ({abs(diff_m):.3f}% diferença)")
    
    if abs(diff_molar_density) < 1.0:
        print(f"✅ Densidade Molar: EXCELENTE ({abs(diff_molar_density):.3f}% diferença)")
    elif abs(diff_molar_density) < 5.0:
        print(f"🟡 Densidade Molar: BOM ({abs(diff_molar_density):.3f}% diferença)")
    else:
        print(f"❌ Densidade Molar: NECESSITA AJUSTE ({abs(diff_molar_density):.3f}% diferença)")
    
    print("\n" + "=" * 80)
    
    # Conclusões
    print("CONCLUSÕES:")
    print("-" * 40)
    
    avg_error = (abs(diff_z) + abs(diff_m) + abs(diff_molar_density)) / 3
    
    if avg_error < 1.0:
        print("🟢 IMPLEMENTAÇÃO APROVADA")
        print(f"   Erro médio: {avg_error:.3f}%")
        print("   A implementação está alinhada com os valores de referência.")
    elif avg_error < 3.0:
        print("🟡 IMPLEMENTAÇÃO NECESSITA AJUSTES MENORES")
        print(f"   Erro médio: {avg_error:.3f}%")
        print("   Ajustes nas correlações podem melhorar a precisão.")
    else:
        print("❌ IMPLEMENTAÇÃO NECESSITA REVISÃO")
        print(f"   Erro médio: {avg_error:.3f}%")
        print("   Revisão das equações de estado é recomendada.")
    
    print("\n" + "=" * 80)
    print("DETALHES TÉCNICOS:")
    print("-" * 40)
    print("• Condições: 600 kPa, 50°C")
    print("• Composição: 96.5% CH₄, 1.8% C₂H₆, 0.45% C₃H₈, etc.")
    print("• Método: AGA 8 2017 D.C. (Detailed Characterization)")
    print("• Base de comparação: Software comercial GERG-2008")
    
    return {
        'reference': reference_results,
        'calculated': our_results,
        'differences': {
            'compressibility_factor': diff_z,
            'molar_mass': diff_m,
            'molar_density': diff_molar_density
        },
        'average_error': avg_error
    }


if __name__ == "__main__":
    validation_results = validate_against_reference()