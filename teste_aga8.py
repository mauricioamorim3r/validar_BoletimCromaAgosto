"""
Teste do AGA 8 2017 Part 2 - GERG 2008
Script de validação com os dados fornecidos
"""

from aga8_gerg2008 import AGA8_GERG2008

def main():
    """Testar cálculos com dados da imagem"""
    
    # Dados fornecidos na imagem
    test_data = {
        'pressure_kpa': 558.0,
        'temperature_c': 55.0,
        'composition': {
            'Methane': 96.5,
            'Nitrogen': 0.3,
            'Carbon Dioxide': 0.6,
            'Ethane': 1.8,
            'Propane': 0.45,
            'Iso-Butane': 0.1,
            'n-Butane': 0.1,
            'iso-Pentane': 0.05,
            'n-Pentane': 0.03,
            'n-Hexane': 0.07
        }
    }
    
    print("=== VALIDAÇÃO AGA 8 2017 Part 2 - GERG 2008 ===")
    print(f"Dados de entrada:")
    print(f"  Pressão: {test_data['pressure_kpa']} kPa absoluta")
    print(f"  Temperatura: {test_data['temperature_c']}°C")
    print(f"  Composição:")
    
    total_composition = 0
    for component, fraction in test_data['composition'].items():
        print(f"    {component}: {fraction}%")
        total_composition += fraction
    
    print(f"  Soma total: {total_composition}%")
    print()
    
    try:
        # Criar calculador
        aga8 = AGA8_GERG2008()
        
        # Realizar cálculos
        results = aga8.calculate_gas_properties(
            test_data['pressure_kpa'],
            test_data['temperature_c'],
            test_data['composition']
        )
        
        if not results.get('error', False) and results.get('validation', {}).get('valid', False):
            print("OK VALIDAÇÃO APROVADA")
            print()
            print("=== PROPRIEDADES CALCULADAS ===")
            
            # Propriedades básicas
            print(f"Massa molar da mistura: {results['mixture_properties']['molecular_weight']:.4f} g/mol")
            print(f"Temperatura crítica: {results['mixture_properties']['critical_temperature']:.2f} K")
            print(f"Pressão crítica: {results['mixture_properties']['critical_pressure']:.1f} kPa")
            print()
            
            # Propriedades nas condições de operação
            print("=== PROPRIEDADES NAS CONDIÇÕES DE OPERAÇÃO ===")
            print(f"Densidade: {results['density_properties']['density_kg_m3']:.4f} kg/m³")
            print(f"Densidade relativa (ar=1): {results['density_properties']['relative_density']:.6f}")
            print(f"Fator de compressibilidade (Z): {results['density_properties']['compressibility_factor']:.6f}")
            print()
            
            # Poder calorífico
            print("=== PODER CALORÍFICO ===")
            print(f"PCS (base volumétrica): {results['heating_value']['HHV_vol_MJ_m3']:.3f} MJ/m³")
            print(f"PCI (base volumétrica): {results['heating_value']['LHV_vol_MJ_m3']:.3f} MJ/m³")
            print(f"PCS (base mássica): {results['heating_value']['HHV_mass_MJ_kg']:.3f} MJ/kg")
            print(f"PCI (base mássica): {results['heating_value']['LHV_mass_MJ_kg']:.3f} MJ/kg")
            print()
            
            # Propriedades adicionais
            print("=== PROPRIEDADES ADICIONAIS ===")
            print(f"Indice Wobbe (PCS): {results['additional_properties']['wobbe_index_HHV']:.3f} MJ/m³")
            print(f"Indice Wobbe (PCI): {results['additional_properties']['wobbe_index_LHV']:.3f} MJ/m³")
            print(f"Numero de Metano (estimado): {results['additional_properties']['methane_number']:.1f}")
            print()
            
            # Validação ANP
            print("=== VALIDAÇÃO ANP ===")
            composition_norm = results['input_data']['composition_molar']
            
            # Verificar limites ANP
            anp_checks = []
            
            # Metano
            ch4_percent = composition_norm.get('CH4', 0) * 100
            if 70.0 <= ch4_percent <= 99.0:
                anp_checks.append(f"OK Metano: {ch4_percent:.1f}% (limite: 70-99%)")
            else:
                anp_checks.append(f"ERRO Metano: {ch4_percent:.1f}% (limite: 70-99%)")
                
            # Nitrogênio
            n2_percent = composition_norm.get('N2', 0) * 100
            if n2_percent <= 15.0:
                anp_checks.append(f"OK Nitrogênio: {n2_percent:.1f}% (limite: <=15%)")
            else:
                anp_checks.append(f"ERRO Nitrogênio: {n2_percent:.1f}% (limite: <=15%)")
                
            # CO2
            co2_percent = composition_norm.get('CO2', 0) * 100
            if co2_percent <= 10.0:
                anp_checks.append(f"OK CO2: {co2_percent:.1f}% (limite: <=10%)")
            else:
                anp_checks.append(f"ERRO CO2: {co2_percent:.1f}% (limite: <=10%)")
                
            # Etano
            c2h6_percent = composition_norm.get('C2H6', 0) * 100
            if c2h6_percent <= 15.0:
                anp_checks.append(f"OK Etano: {c2h6_percent:.1f}% (limite: <=15%)")
            else:
                anp_checks.append(f"ERRO Etano: {c2h6_percent:.1f}% (limite: <=15%)")
                
            # Propano
            c3h8_percent = composition_norm.get('C3H8', 0) * 100
            if c3h8_percent <= 5.0:
                anp_checks.append(f"OK Propano: {c3h8_percent:.2f}% (limite: <=5%)")
            else:
                anp_checks.append(f"ERRO Propano: {c3h8_percent:.2f}% (limite: <=5%)")
            
            for check in anp_checks:
                print(check)
                
        else:
            print(f"ERRO VALIDAÇÃO REPROVADA: {results.get('error', 'Erro desconhecido')}")
            
    except Exception as e:
        print(f"ERRO ERRO NA EXECUÇÃO: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()