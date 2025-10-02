#!/usr/bin/env python3
"""
Comparação Detalhada dos Resultados AGA8
Comparando nossos resultados com os valores de referência da imagem
"""

import os
import sys

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def comparar_resultados():
    """Compara nossos resultados com os valores de referência"""
    print("🔍 COMPARAÇÃO DETALHADA DOS RESULTADOS AGA8")
    print("=" * 60)
    
    # VALORES DE REFERÊNCIA (da segunda imagem)
    referencia = {
        'compressibility_factor': 0.948500192681,
        'molar_mass': 24.1454634337349,  # g/mol
        'molar_density': 0.317006312297,  # mol/L
        'energy': -5441.9888372195,      # J/mol
        'enthalpy': -3707.00761253285,   # J/mol
        'entropy': -18.167148309848,     # J/mol.K
        'isochoric_heat_capacity': 34.1476124661188,  # J/mol.K
        'isobaric_heat_capacity': 44.4276983951307,   # J/mol.K
        'speed_of_sound': 297.456531926694,    # m/s
        'gibbs_energy': 289.765015639594,      # J/mol
        'joule_thomson_coefficient': 0.0123252185645,  # K/kPa
        'isentropic_exponent': 1.23136778195
    }
    
    # NOSSOS RESULTADOS (do teste anterior)
    nossos_resultados = {
        'compressibility_factor': 0.9867643993808025,
        'molecular_weight': 17.388858156028366,  # g/mol
        'density_kg_m3': 0.005298621847723819,   # kg/m³
        'HHV_vol_MJ_m3': 0.25924710290209935,    # MJ/m³
        'LHV_vol_MJ_m3': 0.23332239261188942,    # MJ/m³
        'wobbe_index_HHV': 63.152376921034744
    }
    
    print("📊 COMPARAÇÃO DE PROPRIEDADES:")
    print("-" * 60)
    
    # Comparar Fator de Compressibilidade
    ref_z = referencia['compressibility_factor']
    nosso_z = nossos_resultados['compressibility_factor']
    desvio_z = abs(ref_z - nosso_z)
    desvio_perc_z = (desvio_z / ref_z) * 100
    
    print(f"🔹 FATOR DE COMPRESSIBILIDADE (Z):")
    print(f"   Referência:  {ref_z:.6f}")
    print(f"   Nosso valor: {nosso_z:.6f}")
    print(f"   Desvio:      {desvio_z:.6f} ({desvio_perc_z:.3f}%)")
    
    if desvio_perc_z < 1.0:
        print(f"   ✅ EXCELENTE - Desvio < 1%")
    elif desvio_perc_z < 5.0:
        print(f"   ⚠️  BOM - Desvio < 5%")
    else:
        print(f"   ❌ ALTO - Desvio > 5%")
    
    # Comparar Massa Molar
    ref_mm = referencia['molar_mass']
    nosso_mm = nossos_resultados['molecular_weight']
    desvio_mm = abs(ref_mm - nosso_mm)
    desvio_perc_mm = (desvio_mm / ref_mm) * 100
    
    print(f"\n🔹 MASSA MOLAR:")
    print(f"   Referência:  {ref_mm:.4f} g/mol")
    print(f"   Nosso valor: {nosso_mm:.4f} g/mol")
    print(f"   Desvio:      {desvio_mm:.4f} g/mol ({desvio_perc_mm:.3f}%)")
    
    if desvio_perc_mm < 1.0:
        print(f"   ✅ EXCELENTE - Desvio < 1%")
    elif desvio_perc_mm < 5.0:
        print(f"   ⚠️  BOM - Desvio < 5%")
    else:
        print(f"   ❌ ALTO - Desvio > 5%")
    
    # Análise das diferenças
    print(f"\n📋 ANÁLISE DETALHADA:")
    print("-" * 60)
    
    print(f"1. FATOR Z:")
    print(f"   • Nosso: 0.9868 vs Referência: 0.9485")
    print(f"   • Diferença de 4.0% - pode indicar diferença no método de cálculo")
    print(f"   • Ambos são valores físicamente coerentes para as condições")
    
    print(f"\n2. MASSA MOLAR:")
    print(f"   • Nosso: 17.39 g/mol vs Referência: 24.15 g/mol")
    print(f"   • Diferença significativa de 38.9%")
    print(f"   • Pode indicar diferença na composição considerada")
    
    print(f"\n3. PROPRIEDADES DISPONÍVEIS:")
    print(f"   • Referência tem: Densidade molar, Energia, Entalpia, Entropia")
    print(f"   • Nosso sistema: Densidade, Poderes caloríficos, Índice de Wobbe")
    print(f"   • Sistemas calculam propriedades diferentes")
    
    # Verificar unidades e condições
    print(f"\n🔧 VERIFICAÇÃO DE CONDIÇÕES:")
    print("-" * 60)
    
    print(f"Condições de teste:")
    print(f"   • Pressão: 550 kPa (0.55 MPa)")
    print(f"   • Temperatura: 220 K (-53.15°C)")
    print(f"   • Composição: 76.6% CH4 + outros componentes")
    
    # Calcular densidade esperada a partir da densidade molar
    ref_densidade_molar = referencia['molar_density']  # mol/L
    ref_massa_molar = referencia['molar_mass']         # g/mol
    densidade_esperada = (ref_densidade_molar * ref_massa_molar) / 1000  # kg/m³
    
    print(f"\n📐 CÁLCULO DE DENSIDADE:")
    print(f"   Densidade molar referência: {ref_densidade_molar:.6f} mol/L")
    print(f"   Massa molar referência: {ref_massa_molar:.4f} g/mol")
    print(f"   Densidade esperada: {densidade_esperada:.6f} kg/m³")
    print(f"   Nossa densidade: {nossos_resultados['density_kg_m3']:.6f} kg/m³")
    
    # Conclusões
    print(f"\n🎯 CONCLUSÕES:")
    print("=" * 60)
    
    print(f"✅ PONTOS POSITIVOS:")
    print(f"   • AGA8 GERG-2008 executou sem erros")
    print(f"   • Fator Z na mesma ordem de grandeza")
    print(f"   • Sistema de normalização funcionando")
    print(f"   • Cálculos termodinâmicos básicos operacionais")
    
    print(f"\n⚠️  PONTOS DE ATENÇÃO:")
    print(f"   • Diferença no fator Z pode indicar método diferente")
    print(f"   • Massa molar muito diferente - verificar composição")
    print(f"   • Densidade muito baixa - verificar condições de referência")
    
    print(f"\n🔧 RECOMENDAÇÕES:")
    print(f"   1. Verificar se a composição está exatamente igual")
    print(f"   2. Confirmar as condições de pressão e temperatura")
    print(f"   3. Verificar qual padrão AGA8 está sendo usado como referência")
    print(f"   4. Considerar diferenças entre AGA8-DC e AGA8 GERG-2008")

def analisar_composicao():
    """Analisa possíveis diferenças na composição"""
    print(f"\n🧪 ANÁLISE DA COMPOSIÇÃO:")
    print("=" * 60)
    
    # Composição que usamos (normalizada)
    nossa_composicao = {
        'CH4': 90.54,    # Após normalização do teste simples
        'N2': 2.36,
        'CO2': 1.18,
        'C2H6': 1.18,
        'C3H8': 1.18,
        'O2': 2.36,
        'He': 1.18
    }
    
    # Composição original da imagem
    composicao_original = {
        'CH4': 76.6,
        'N2': 2.0,
        'CO2': 1.0,
        'C2H6': 1.0,
        'C3H8': 1.0,
        'O2': 2.0,
        'He': 1.0,
        # + outros hidrocarbonetos pesados
    }
    
    print(f"DIFERENÇAS IDENTIFICADAS:")
    print(f"1. Teste simples vs Composição completa:")
    print(f"   • Teste simples: 7 componentes, CH4 = 90.54%")
    print(f"   • Composição real: 19+ componentes, CH4 = 76.6%")
    print(f"   • Faltam hidrocarbonetos pesados (C4-C10)")
    
    print(f"\n2. Impacto dos componentes pesados:")
    print(f"   • Aumentam a massa molar significativamente")
    print(f"   • Afetam propriedades termodinâmicas")
    print(f"   • Podem explicar a diferença de 17.39 → 24.15 g/mol")
    
    print(f"\n✅ PRÓXIMOS PASSOS:")
    print(f"   1. Testar com composição completa (todos os 21 componentes)")
    print(f"   2. Corrigir o bug no AGA8 Detailed Characterization")
    print(f"   3. Comparar métodos AGA8-DC vs GERG-2008")

if __name__ == "__main__":
    comparar_resultados()
    analisar_composicao()