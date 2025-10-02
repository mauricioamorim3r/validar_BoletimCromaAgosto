#!/usr/bin/env python3
"""
Teste AGA8 GERG-2008 - Memorial Oficial
Validação com novos dados: 555 kPa, 50°C
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from aga8_gerg2008 import AGA8_GERG2008
except ImportError as e:
    print(f"❌ ERRO: Não foi possível importar AGA8 GERG-2008: {e}")
    sys.exit(1)

def teste_memorial_gerg2008():
    """Teste com dados do memorial oficial AGA8 GERG-2008"""
    print("🔬 TESTE AGA8 GERG-2008 - MEMORIAL OFICIAL")
    print("=" * 60)
    
    # Condições exatas do memorial GERG-2008
    pressao_kpa = 555.0      # kPa absolute  
    temperatura_c = 50.0     # °C
    
    print(f"📋 MEMORIAL OFICIAL AGA8 2017 Part 2 GERG 2008:")
    print(f"   Data: 02/10/25")
    print(f"   Hora: 18:49:04")
    print(f"   Método: GERG 2008")
    print(f"   Pressão: {pressao_kpa} kPa absolute")
    print(f"   Temperatura: {temperatura_c} °C")
    
    # Composição exata do memorial
    composicao_memorial = {
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
        'iC5H12': 0.05,  # iso-Pentane
        'nC5H12': 0.03,  # n-Pentane
        'nC6H14': 0.07,  # n-Hexane
        'nC7H16': 0.0,   # n-Heptane
        'nC8H18': 0.0,   # n-Octane
        'nC9H20': 0.0,   # n-Nonane
        'nC10H22': 0.0,  # n-Decano
        'He': 0.0,       # Helium
        'Ar': 0.0        # Argon
    }
    
    # Verificar composição
    soma_comp = sum(v for v in composicao_memorial.values() if v > 0)
    print(f"\n🧪 COMPOSIÇÃO:")
    print(f"   Soma total: {soma_comp}%")
    print(f"   Componentes ativos:")
    for comp, valor in composicao_memorial.items():
        if valor > 0:
            print(f"     {comp}: {valor}%")
    
    print(f"\n🔬 EXECUTANDO AGA8 GERG-2008:")
    print("-" * 60)
    
    try:
        aga8_gerg = AGA8_GERG2008()
        resultado = aga8_gerg.calculate_gas_properties(
            pressure_kpa=pressao_kpa,
            temperature_c=temperatura_c,
            composition=composicao_memorial
        )
        
        print(f"✅ CÁLCULO EXECUTADO COM SUCESSO!")
        
        # Exibir resultados organizados
        print(f"\n📊 RESULTADOS AGA8 GERG-2008:")
        print("=" * 60)
        
        # Propriedades da mistura
        if 'mixture_properties' in resultado:
            mix_props = resultado['mixture_properties']
            print(f"\n🔹 PROPRIEDADES DA MISTURA:")
            if 'molecular_weight' in mix_props:
                print(f"   Massa Molar: {mix_props['molecular_weight']:.6f} g/mol")
            if 'critical_temperature' in mix_props:
                print(f"   Temperatura Crítica: {mix_props['critical_temperature']:.3f} K")
            if 'critical_pressure' in mix_props:
                print(f"   Pressão Crítica: {mix_props['critical_pressure']:.3f} kPa")
        
        # Propriedades de densidade
        if 'density_properties' in resultado:
            dens_props = resultado['density_properties']
            print(f"\n🔹 PROPRIEDADES DE DENSIDADE:")
            if 'compressibility_factor' in dens_props:
                z_factor = dens_props['compressibility_factor']
                print(f"   Fator de Compressibilidade (Z): {z_factor:.8f}")
            if 'density_kg_m3' in dens_props:
                densidade = dens_props['density_kg_m3']
                print(f"   Densidade: {densidade:.6f} kg/m³")
            if 'relative_density' in dens_props:
                dens_rel = dens_props['relative_density']
                print(f"   Densidade Relativa: {dens_rel:.6f}")
            
            # Calcular densidade molar
            if 'molecular_weight' in resultado.get('mixture_properties', {}) and densidade:
                mm = resultado['mixture_properties']['molecular_weight']
                densidade_molar = (densidade * 1000) / mm  # mol/L
                print(f"   Densidade Molar: {densidade_molar:.6f} mol/L")
        
        # Propriedades energéticas
        if 'heating_value' in resultado:
            heating = resultado['heating_value']
            print(f"\n🔥 PROPRIEDADES ENERGÉTICAS:")
            if 'HHV_vol_MJ_m3' in heating:
                print(f"   Poder Calorífico Superior: {heating['HHV_vol_MJ_m3']:.6f} MJ/m³")
            if 'LHV_vol_MJ_m3' in heating:
                print(f"   Poder Calorífico Inferior: {heating['LHV_vol_MJ_m3']:.6f} MJ/m³")
            if 'HHV_mass_MJ_kg' in heating:
                print(f"   PCS (base mássica): {heating['HHV_mass_MJ_kg']:.6f} MJ/kg")
            if 'LHV_mass_MJ_kg' in heating:
                print(f"   PCI (base mássica): {heating['LHV_mass_MJ_kg']:.6f} MJ/kg")
        
        # Propriedades adicionais
        if 'additional_properties' in resultado:
            add_props = resultado['additional_properties']
            print(f"\n📊 PROPRIEDADES ADICIONAIS:")
            if 'wobbe_index_HHV' in add_props:
                print(f"   Índice de Wobbe (PCS): {add_props['wobbe_index_HHV']:.6f}")
            if 'wobbe_index_LHV' in add_props:
                print(f"   Índice de Wobbe (PCI): {add_props['wobbe_index_LHV']:.6f}")
            if 'methane_number' in add_props:
                print(f"   Número de Metano: {add_props['methane_number']:.3f}")
        
        print(f"\n🎯 VALORES PRINCIPAIS PARA COMPARAÇÃO:")
        print("-" * 60)
        
        # Extrair valores principais para comparação futura
        valores_principais = {}
        
        if 'density_properties' in resultado:
            dp = resultado['density_properties']
            valores_principais['z_factor'] = dp.get('compressibility_factor')
            valores_principais['densidade'] = dp.get('density_kg_m3')
            valores_principais['densidade_relativa'] = dp.get('relative_density')
        
        if 'mixture_properties' in resultado:
            mp = resultado['mixture_properties']
            valores_principais['massa_molar'] = mp.get('molecular_weight')
            
            # Calcular densidade molar
            if valores_principais.get('densidade') and valores_principais.get('massa_molar'):
                valores_principais['densidade_molar'] = (valores_principais['densidade'] * 1000) / valores_principais['massa_molar']
        
        if 'heating_value' in resultado:
            hv = resultado['heating_value']
            valores_principais['pcs_vol'] = hv.get('HHV_vol_MJ_m3')
            valores_principais['pci_vol'] = hv.get('LHV_vol_MJ_m3')
        
        # Exibir valores principais
        for prop, valor in valores_principais.items():
            if valor is not None:
                if 'factor' in prop or 'z_' in prop:
                    print(f"   {prop}: {valor:.8f}")
                elif 'densidade' in prop or 'massa' in prop:
                    print(f"   {prop}: {valor:.6f}")
                else:
                    print(f"   {prop}: {valor:.4f}")
        
        print(f"\n🔄 AGUARDANDO DADOS DE REFERÊNCIA PARA COMPARAÇÃO...")
        return valores_principais, resultado
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def comparar_com_teste_anterior():
    """Compara com o teste anterior (500 kPa, 55°C)"""
    print(f"\n📈 COMPARAÇÃO COM TESTE ANTERIOR:")
    print("-" * 60)
    print(f"Teste Anterior (500 kPa, 55°C):")
    print(f"   Z-factor: 0.99086112")
    print(f"   Massa Molar: 16.803583 g/mol")
    print(f"   Densidade: 0.003108 kg/m³")
    
    print(f"\nTeste Atual (555 kPa, 50°C):")
    print(f"   Condições mais severas: maior pressão, menor temperatura")
    print(f"   Esperado: maior densidade, menor Z-factor")

if __name__ == "__main__":
    print("🚀 INICIANDO TESTE AGA8 GERG-2008 - MEMORIAL OFICIAL")
    valores, resultado_completo = teste_memorial_gerg2008()
    
    if valores:
        comparar_com_teste_anterior()
        print(f"\n✅ TESTE CONCLUÍDO - Pronto para comparação com memorial!")
    else:
        print(f"\n❌ TESTE FALHOU - Verificar implementação")