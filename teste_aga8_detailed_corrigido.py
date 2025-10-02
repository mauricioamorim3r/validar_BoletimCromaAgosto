#!/usr/bin/env python3
"""
Teste AGA8 Detailed Characterization - Versão Corrigida
Com mapeamento correto de componentes
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from aga8_detailed_characterization import AGA8_DetailedCharacterization
except ImportError as e:
    print(f"❌ ERRO: Não foi possível importar AGA8 Detailed: {e}")
    sys.exit(1)

def converter_composicao(composicao_entrada):
    """Converte nomes de componentes para formato interno do AGA8 Detailed"""
    
    mapeamento = {
        'CH4': 'methane',
        'N2': 'nitrogen', 
        'CO2': 'carbon_dioxide',
        'C2H6': 'ethane',
        'C3H8': 'propane',
        'H2O': 'water',
        'H2S': 'hydrogen_sulfide',
        'H2': 'hydrogen',
        'CO': 'carbon_monoxide',
        'O2': 'oxygen',
        'iC4H10': 'i_butane',
        'nC4H10': 'n_butane',
        'iC5H12': 'i_pentane',
        'nC5H12': 'n_pentane',
        'nC6H14': 'n_hexane',
        'nC7H16': 'n_heptane',
        'nC8H18': 'n_octane',
        'nC9H20': 'n_nonane',
        'nC10H22': 'n_decane',
        'He': 'helium',
        'Ar': 'argon'
    }
    
    composicao_convertida = {}
    for comp_entrada, valor in composicao_entrada.items():
        if valor > 0 and comp_entrada in mapeamento:
            comp_interno = mapeamento[comp_entrada]
            composicao_convertida[comp_interno] = valor
    
    return composicao_convertida

def teste_aga8_detailed_corrigido():
    """Teste do AGA8 Detailed com mapeamento correto"""
    print("🔬 TESTE AGA8 DETAILED CHARACTERIZATION - CORRIGIDO")
    print("=" * 60)
    
    # Condições do teste
    pressao_kpa = 500.0
    temperatura_c = 55.0
    
    # Composição original
    composicao_original = {
        'CH4': 96.5,          # Metano
        'N2': 0.3,            # Nitrogênio
        'CO2': 0.6,           # Dióxido de carbono
        'C2H6': 1.8,          # Etano
        'C3H8': 0.45,         # Propano
        'H2O': 0.0,           # Água
        'H2S': 0.0,           # H2S
        'H2': 0.0,            # Hidrogênio
        'CO': 0.0,            # CO
        'O2': 0.0,            # Oxigênio
        'iC4H10': 0.1,        # iso-Butano
        'nC4H10': 0.1,        # n-Butano
        'iC5H12': 0.05,       # iso-Pentano
        'nC5H12': 0.03,       # n-Pentano
        'nC6H14': 0.07,       # n-Hexano
        'nC7H16': 0.0,        # n-Heptano
        'nC8H18': 0.0,        # n-Octano
        'nC9H20': 0.0,        # n-Nonano
        'nC10H22': 0.0,       # n-Decano
        'He': 0.0,            # Hélio
        'Ar': 0.0             # Argônio
    }
    
    print(f"📊 CONDIÇÕES:")
    print(f"   Pressão: {pressao_kpa} kPa")
    print(f"   Temperatura: {temperatura_c}°C")
    
    # Converter composição
    composicao_convertida = converter_composicao(composicao_original)
    
    print(f"\n🧪 COMPOSIÇÃO (convertida para AGA8 Detailed):")
    for comp, valor in composicao_convertida.items():
        print(f"   {comp}: {valor}%")
    
    try:
        aga8_detailed = AGA8_DetailedCharacterization()
        
        # Calcular todas as propriedades
        resultado = aga8_detailed.calculate_all_properties(
            pressao_kpa, temperatura_c, composicao_convertida
        )
        
        print(f"\n✅ RESULTADOS AGA8 DETAILED CHARACTERIZATION:")
        print("=" * 60)
        
        # Organizar resultados por categoria
        propriedades_fundamentais = [
            ('compressibility_factor', 'Fator de Compressibilidade (Z)', ''),
            ('molar_mass', 'Massa Molar', 'g/mol'),
            ('density', 'Densidade', 'kg/m³')
        ]
        
        propriedades_energeticas = [
            ('heating_value_superior_mass', 'PCS (massa)', 'kJ/kg'),
            ('heating_value_inferior_mass', 'PCI (massa)', 'kJ/kg'),
            ('heating_value_superior_volume', 'PCS (volume)', 'kJ/m³'),
            ('heating_value_inferior_volume', 'PCI (volume)', 'kJ/m³')
        ]
        
        propriedades_adicionais = [
            ('wobbe_index', 'Índice de Wobbe', ''),
            ('methane_number', 'Número de Metano', ''),
            ('specific_gravity', 'Densidade Relativa', '')
        ]
        
        print(f"🔹 PROPRIEDADES FUNDAMENTAIS:")
        for prop, nome, unidade in propriedades_fundamentais:
            if prop in resultado:
                valor = resultado[prop]
                if prop == 'compressibility_factor':
                    print(f"   {nome}: {valor:.8f} {unidade}")
                elif 'density' in prop or 'mass' in prop:
                    print(f"   {nome}: {valor:.6f} {unidade}")
                else:
                    print(f"   {nome}: {valor:.4f} {unidade}")
        
        print(f"\n🔥 PROPRIEDADES ENERGÉTICAS:")
        for prop, nome, unidade in propriedades_energeticas:
            if prop in resultado:
                valor = resultado[prop]
                print(f"   {nome}: {valor:.4f} {unidade}")
        
        print(f"\n📊 PROPRIEDADES ADICIONAIS:")
        for prop, nome, unidade in propriedades_adicionais:
            if prop in resultado:
                valor = resultado[prop]
                print(f"   {nome}: {valor:.4f} {unidade}")
        
        # Comparar com valores de referência se disponíveis
        print(f"\n🎯 COMPARAÇÃO COM REFERÊNCIA:")
        print("=" * 60)
        
        referencia = {
            'compressibility_factor': 0.993478459795,
            'molar_mass': 16.8035819,
            'density': None  # Será calculada a partir da densidade molar
        }
        
        # Calcular densidade de referência a partir da densidade molar
        densidade_molar_ref = 0.184460117402  # mol/L
        massa_molar_ref = 16.8035819  # g/mol
        densidade_ref = (densidade_molar_ref * massa_molar_ref) / 1000  # kg/m³
        referencia['density'] = densidade_ref
        
        desvios = []
        for prop, nome, unidade in propriedades_fundamentais:
            if prop in resultado and prop in referencia:
                calc = resultado[prop]
                ref = referencia[prop]
                desvio_abs = abs(calc - ref)
                desvio_perc = (desvio_abs / ref) * 100
                desvios.append(desvio_perc)
                
                print(f"{nome}:")
                print(f"   Calculado:  {calc:.8f} {unidade}")
                print(f"   Referência: {ref:.8f} {unidade}")
                print(f"   Desvio:     {desvio_abs:.8f} ({desvio_perc:.4f}%) {unidade}")
                
                if desvio_perc < 0.5:
                    status = "✅ EXCELENTE"
                elif desvio_perc < 1.0:
                    status = "✅ MUITO BOM"
                elif desvio_perc < 5.0:
                    status = "⚠️  ACEITÁVEL"
                else:
                    status = "❌ SIGNIFICATIVO"
                
                print(f"   Status:     {status}\n")
        
        if desvios:
            desvio_medio = sum(desvios) / len(desvios)
            print(f"📈 RESUMO:")
            print(f"   Desvio médio: {desvio_medio:.4f}%")
            if desvio_medio < 1.0:
                print(f"   ✅ AGA8 DETAILED VALIDADO - Precisão excelente!")
            elif desvio_medio < 5.0:
                print(f"   ⚠️  AGA8 DETAILED ACEITÁVEL - Precisão boa")
            else:
                print(f"   ❌ REVISAR AGA8 DETAILED - Desvios significativos")
        
        return resultado
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO TESTE AGA8 DETAILED CORRIGIDO")
    resultado = teste_aga8_detailed_corrigido()
    
    if resultado:
        print(f"\n✅ TESTE CONCLUÍDO COM SUCESSO!")
        print(f"🎉 AGA8 DETAILED CHARACTERIZATION FUNCIONANDO!")
    else:
        print(f"\n❌ TESTE FALHOU - Verificar implementação")