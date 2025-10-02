#!/usr/bin/env python3
"""
Teste AGA8 - Novos Dados de Entrada
Condições: 500 kPa, 55°C
Composição rica em metano (96.5%)
"""

import os
import sys

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from aga8_gerg2008 import AGA8_GERG2008
    from aga8_detailed_characterization import AGA8_DetailedCharacterization
except ImportError as e:
    print(f"❌ ERRO: Não foi possível importar AGA8: {e}")
    sys.exit(1)

def teste_novos_dados():
    """Teste com os novos dados fornecidos na imagem"""
    print("🎯 TESTE AGA8 - NOVOS DADOS DE ENTRADA")
    print("=" * 50)
    
    # Condições conforme nova imagem
    pressao_kpa = 500.0      # kPa absoluta
    temperatura_c = 55.0     # °C
    temperatura_k = temperatura_c + 273.15  # 328.15 K
    
    print(f"📊 CONDIÇÕES DE TESTE:")
    print(f"   Pressão: {pressao_kpa} kPa (absoluta)")
    print(f"   Temperatura: {temperatura_c}°C ({temperatura_k} K)")
    
    # Composição conforme nova imagem (% molar)
    composicao_nova = {
        'CH4': 96.5,          # Metano - componente dominante
        'N2': 0.3,            # Nitrogênio
        'CO2': 0.6,           # Dióxido de carbono
        'C2H6': 1.8,          # Etano
        'C3H8': 0.45,         # Propano
        'H2O': 0.0,           # Água (0%)
        'H2S': 0.0,           # H2S (0%)
        'H2': 0.0,            # Hidrogênio (0%)
        'CO': 0.0,            # CO (0%)
        'O2': 0.0,            # Oxigênio (0%)
        'iC4H10': 0.1,        # iso-Butano
        'nC4H10': 0.1,        # n-Butano
        'iC5H12': 0.05,       # iso-Pentano
        'nC5H12': 0.03,       # n-Pentano
        'nC6H14': 0.07,       # n-Hexano
        'nC7H16': 0.0,        # n-Heptano (0%)
        'nC8H18': 0.0,        # n-Octano (0%)
        'nC9H20': 0.0,        # n-Nonano (0%)
        'nC10H22': 0.0,       # n-Decano (0%)
        'He': 0.0,            # Hélio (0%)
        'Ar': 0.0             # Argônio (0%)
    }
    
    # Verificar soma (deve ser 100%)
    soma_composicao = sum(composicao_nova.values())
    print(f"\n🧪 COMPOSIÇÃO DETALHADA:")
    print(f"   Soma total: {soma_composicao}%")
    
    # Exibir apenas componentes presentes
    print(f"   Componentes presentes:")
    for comp, valor in composicao_nova.items():
        if valor > 0:
            print(f"     {comp}: {valor}%")
    
    # Normalizar se necessário
    if abs(soma_composicao - 100.0) > 0.01:
        print(f"   ⚠️  Normalizando para 100%...")
        fator_normalizacao = 100.0 / soma_composicao
        for comp in composicao_nova:
            composicao_nova[comp] *= fator_normalizacao
        nova_soma = sum(composicao_nova.values())
        print(f"   Nova soma: {nova_soma:.3f}%")
    
    # Executar teste com AGA8 GERG-2008
    resultado_gerg = testar_aga8_gerg(pressao_kpa, temperatura_c, composicao_nova)
    
    # Tentar executar teste com AGA8 Detailed (se funcionar)
    resultado_detailed = testar_aga8_detailed(pressao_kpa, temperatura_c, composicao_nova)
    
    # Comparar resultados se ambos funcionarem
    if resultado_gerg and resultado_detailed:
        comparar_metodos(resultado_gerg, resultado_detailed)
    
    return resultado_gerg, resultado_detailed

def testar_aga8_gerg(pressao_kpa, temperatura_c, composicao):
    """Testa AGA8 GERG-2008"""
    print(f"\n🔬 TESTE AGA8 GERG-2008:")
    print("=" * 40)
    
    try:
        aga8_gerg = AGA8_GERG2008()
        resultado = aga8_gerg.calculate_gas_properties(
            pressure_kpa=pressao_kpa,
            temperature_c=temperatura_c,
            composition=composicao
        )
        
        print(f"✅ RESULTADOS AGA8 GERG-2008:")
        
        # Propriedades da mistura
        if 'mixture_properties' in resultado:
            mix_props = resultado['mixture_properties']
            print(f"\n📋 PROPRIEDADES DA MISTURA:")
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
        
        return resultado
        
    except Exception as e:
        print(f"❌ ERRO AGA8 GERG-2008: {e}")
        import traceback
        traceback.print_exc()
        return None

def testar_aga8_detailed(pressao_kpa, temperatura_c, composicao):
    """Testa AGA8 Detailed Characterization"""
    print(f"\n🔬 TESTE AGA8 DETAILED CHARACTERIZATION:")
    print("=" * 40)
    
    try:
        aga8_detailed = AGA8_DetailedCharacterization()
        resultado = aga8_detailed.calculate_all_properties(
            pressure_kpa=pressao_kpa,
            temperature_c=temperatura_c,
            composition=composicao
        )
        
        print(f"✅ RESULTADOS AGA8 DETAILED:")
        
        # Exibir propriedades calculadas
        for key, value in resultado.items():
            if isinstance(value, (int, float)):
                if 'factor' in key.lower() or 'compressibility' in key.lower():
                    print(f"   {key}: {value:.8f}")
                elif 'density' in key.lower():
                    print(f"   {key}: {value:.6f}")
                else:
                    print(f"   {key}: {value:.4f}")
            else:
                print(f"   {key}: {value}")
        
        return resultado
        
    except Exception as e:
        print(f"❌ ERRO AGA8 Detailed: {e}")
        return None

def comparar_metodos(resultado_gerg, resultado_detailed):
    """Compara os resultados dos dois métodos"""
    print(f"\n🔍 COMPARAÇÃO ENTRE MÉTODOS:")
    print("=" * 40)
    
    # Comparar fator Z se disponível em ambos
    z_gerg = None
    z_detailed = None
    
    if 'density_properties' in resultado_gerg:
        z_gerg = resultado_gerg['density_properties'].get('compressibility_factor')
    
    if 'compressibility_factor' in resultado_detailed:
        z_detailed = resultado_detailed['compressibility_factor']
    
    if z_gerg and z_detailed:
        desvio_z = abs(z_gerg - z_detailed)
        desvio_perc = (desvio_z / z_gerg) * 100
        print(f"Fator de Compressibilidade (Z):")
        print(f"   GERG-2008:  {z_gerg:.8f}")
        print(f"   Detailed:   {z_detailed:.8f}")
        print(f"   Desvio:     {desvio_z:.8f} ({desvio_perc:.4f}%)")
        
        if desvio_perc < 0.1:
            print(f"   ✅ EXCELENTE concordância")
        elif desvio_perc < 1.0:
            print(f"   ⚠️  BOA concordância")
        else:
            print(f"   ❌ Diferença significativa")

def preparar_resultado_para_comparacao(resultado_gerg):
    """Prepara um resumo dos resultados para comparação futura"""
    if not resultado_gerg:
        return None
    
    print(f"\n📋 RESUMO PARA COMPARAÇÃO:")
    print("=" * 40)
    
    resumo = {}
    
    # Extrair propriedades principais
    if 'density_properties' in resultado_gerg:
        dens_props = resultado_gerg['density_properties']
        resumo['fator_compressibilidade'] = dens_props.get('compressibility_factor')
        resumo['densidade_kg_m3'] = dens_props.get('density_kg_m3')
        resumo['densidade_relativa'] = dens_props.get('relative_density')
    
    if 'mixture_properties' in resultado_gerg:
        mix_props = resultado_gerg['mixture_properties']
        resumo['massa_molar'] = mix_props.get('molecular_weight')
    
    if 'heating_value' in resultado_gerg:
        heating = resultado_gerg['heating_value']
        resumo['pcs_vol'] = heating.get('HHV_vol_MJ_m3')
        resumo['pci_vol'] = heating.get('LHV_vol_MJ_m3')
    
    # Calcular densidade molar se possível
    if resumo.get('densidade_kg_m3') and resumo.get('massa_molar'):
        resumo['densidade_molar'] = (resumo['densidade_kg_m3'] * 1000) / resumo['massa_molar']
    
    print(f"Propriedades calculadas:")
    for prop, valor in resumo.items():
        if valor is not None:
            if 'fator' in prop:
                print(f"   {prop}: {valor:.8f}")
            elif 'densidade' in prop:
                print(f"   {prop}: {valor:.6f}")
            else:
                print(f"   {prop}: {valor:.4f}")
    
    print(f"\n🔄 Aguardando dados de referência para comparação...")
    return resumo

if __name__ == "__main__":
    print("🚀 INICIANDO TESTE COM NOVOS DADOS")
    resultado_gerg, resultado_detailed = teste_novos_dados()
    
    # Preparar resumo para comparação
    resumo = preparar_resultado_para_comparacao(resultado_gerg)
    
    print(f"\n✅ TESTE CONCLUÍDO - Aguardando dados de referência!")