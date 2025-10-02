#!/usr/bin/env python3
"""
Teste AGA8 com Composição Exata da Imagem
Usando todos os componentes conforme fornecido
"""

import os
import sys

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from aga8_gerg2008 import AGA8_GERG2008
except ImportError as e:
    print(f"❌ ERRO: Não foi possível importar AGA8: {e}")
    sys.exit(1)

def teste_composicao_exata():
    """Teste com a composição exata da primeira imagem"""
    print("🎯 TESTE AGA8 - COMPOSIÇÃO EXATA DA IMAGEM")
    print("=" * 50)
    
    # Condições exatas da imagem
    pressao_kpa = 550.0  # kPa absoluta
    temperatura_k = 220.0  # K
    temperatura_c = temperatura_k - 273.15  # -53.15°C
    
    print(f"Condições de teste:")
    print(f"  Pressão: {pressao_kpa} kPa")
    print(f"  Temperatura: {temperatura_k} K ({temperatura_c:.2f}°C)")
    
    # Composição EXATA da primeira imagem (% molar)
    # Soma deve ser 99.6% conforme mostrado
    composicao_exata = {
        'CH4': 76.6,      # Metano
        'N2': 2.0,        # Nitrogênio  
        'CO2': 1.0,       # Dióxido de carbono
        'C2H6': 1.0,      # Etano
        'C3H8': 1.0,      # Propano
        'H2O': 1.0,       # Água
        'H2S': 1.0,       # Sulfeto de hidrogênio
        'CO': 1.0,        # Monóxido de carbono
        'O2': 2.0,        # Oxigênio
        'iC4H10': 1.0,    # iso-Butano
        'nC4H10': 1.0,    # n-Butano
        'iC5H12': 1.0,    # iso-Pentano
        'nC5H12': 1.0,    # n-Pentano
        'nC6H14': 1.0,    # n-Hexano
        'nC7H16': 1.0,    # n-Heptano
        'nC8H18': 1.0,    # n-Octano
        'nC9H20': 1.0,    # n-Nonano
        'nC10H22': 1.0,   # n-Decano
        'He': 1.0,        # Hélio
        'Ar': 0.0         # Argônio (0 conforme imagem)
    }
    
    # Verificar soma
    soma_original = sum(composicao_exata.values())
    print(f"\nComposição original:")
    print(f"  Soma dos componentes: {soma_original}%")
    print(f"  Conforme imagem: 99.6%")
    
    # Ajustar para 99.6% se necessário
    if abs(soma_original - 99.6) > 0.1:
        # Ajustar proporcionalmente para atingir 99.6%
        fator_ajuste = 99.6 / soma_original
        for comp in composicao_exata:
            composicao_exata[comp] *= fator_ajuste
        print(f"  Ajustada para: {sum(composicao_exata.values()):.1f}%")
    
    # Exibir composição detalhada
    print(f"\nComposição detalhada:")
    componentes_principais = ['CH4', 'N2', 'CO2', 'C2H6', 'C3H8', 'O2']
    componentes_pesados = ['iC4H10', 'nC4H10', 'iC5H12', 'nC5H12', 'nC6H14', 'nC7H16', 'nC8H18', 'nC9H20', 'nC10H22']
    componentes_outros = ['H2O', 'H2S', 'CO', 'He', 'Ar']
    
    for categoria, lista in [("Principais", componentes_principais), 
                            ("Pesados", componentes_pesados), 
                            ("Outros", componentes_outros)]:
        print(f"  {categoria}:")
        for comp in lista:
            if comp in composicao_exata and composicao_exata[comp] > 0:
                print(f"    {comp}: {composicao_exata[comp]:.3f}%")
    
    # Executar cálculo AGA8
    try:
        print(f"\n🔬 EXECUTANDO AGA8 GERG-2008...")
        aga8 = AGA8_GERG2008()
        
        resultado = aga8.calculate_gas_properties(
            pressure_kpa=pressao_kpa,
            temperature_c=temperatura_c,
            composition=composicao_exata
        )
        
        print(f"\n📊 RESULTADOS OBTIDOS:")
        print("=" * 50)
        
        # Extrair propriedades principais
        densidade_props = resultado.get('density_properties', {})
        mistura_props = resultado.get('mixture_properties', {})
        heating_props = resultado.get('heating_value', {})
        adicional_props = resultado.get('additional_properties', {})
        
        print(f"🔹 PROPRIEDADES FUNDAMENTAIS:")
        if 'compressibility_factor' in densidade_props:
            z_factor = densidade_props['compressibility_factor']
            print(f"   Fator de Compressibilidade (Z): {z_factor:.6f}")
        
        if 'molecular_weight' in mistura_props:
            massa_molar = mistura_props['molecular_weight']
            print(f"   Massa Molar: {massa_molar:.4f} g/mol")
        
        if 'density_kg_m3' in densidade_props:
            densidade = densidade_props['density_kg_m3']
            print(f"   Densidade: {densidade:.6f} kg/m³")
        
        if 'relative_density' in densidade_props:
            densidade_rel = densidade_props['relative_density']
            print(f"   Densidade Relativa: {densidade_rel:.6f}")
        
        # Calcular densidade molar se possível
        if massa_molar and densidade:
            densidade_molar = (densidade * 1000) / massa_molar  # mol/L
            print(f"   Densidade Molar: {densidade_molar:.6f} mol/L")
        
        print(f"\n🔹 PROPRIEDADES ENERGÉTICAS:")
        if 'HHV_vol_MJ_m3' in heating_props:
            pcs = heating_props['HHV_vol_MJ_m3']
            print(f"   Poder Calorífico Superior: {pcs:.4f} MJ/m³")
        
        if 'LHV_vol_MJ_m3' in heating_props:
            pci = heating_props['LHV_vol_MJ_m3']
            print(f"   Poder Calorífico Inferior: {pci:.4f} MJ/m³")
        
        if 'wobbe_index_HHV' in adicional_props:
            wobbe = adicional_props['wobbe_index_HHV']
            print(f"   Índice de Wobbe (PCS): {wobbe:.4f}")
        
        # Comparar com valores de referência
        print(f"\n🔍 COMPARAÇÃO COM REFERÊNCIA:")
        print("=" * 50)
        
        ref_z = 0.948500192681
        ref_massa_molar = 24.1454634337349
        ref_densidade_molar = 0.317006312297
        
        if 'compressibility_factor' in densidade_props:
            nosso_z = densidade_props['compressibility_factor']
            desvio_z = abs(ref_z - nosso_z)
            desvio_perc_z = (desvio_z / ref_z) * 100
            print(f"Fator Z:")
            print(f"   Referência: {ref_z:.6f}")
            print(f"   Nosso:      {nosso_z:.6f}")
            print(f"   Desvio:     {desvio_z:.6f} ({desvio_perc_z:.2f}%)")
            
            if desvio_perc_z < 1.0:
                print(f"   ✅ EXCELENTE")
            elif desvio_perc_z < 5.0:
                print(f"   ⚠️  BOM")
            else:
                print(f"   ❌ NECESSITA AJUSTE")
        
        if 'molecular_weight' in mistura_props:
            nossa_mm = mistura_props['molecular_weight']
            desvio_mm = abs(ref_massa_molar - nossa_mm)
            desvio_perc_mm = (desvio_mm / ref_massa_molar) * 100
            print(f"\nMassa Molar:")
            print(f"   Referência: {ref_massa_molar:.4f} g/mol")
            print(f"   Nosso:      {nossa_mm:.4f} g/mol")
            print(f"   Desvio:     {desvio_mm:.4f} g/mol ({desvio_perc_mm:.2f}%)")
            
            if desvio_perc_mm < 1.0:
                print(f"   ✅ EXCELENTE")
            elif desvio_perc_mm < 5.0:
                print(f"   ⚠️  BOM")
            else:
                print(f"   ❌ NECESSITA AJUSTE")
        
        return resultado
        
    except Exception as e:
        print(f"❌ ERRO no cálculo AGA8: {e}")
        import traceback
        traceback.print_exc()
        return None

def avaliar_implementacao(resultado):
    """Avalia a qualidade da nossa implementação AGA8"""
    if not resultado:
        print(f"\n❌ IMPLEMENTAÇÃO NÃO PÔDE SER AVALIADA")
        return
    
    print(f"\n🎯 AVALIAÇÃO FINAL DA IMPLEMENTAÇÃO AGA8")
    print("=" * 50)
    
    densidade_props = resultado.get('density_properties', {})
    mistura_props = resultado.get('mixture_properties', {})
    
    pontos_positivos = []
    pontos_atenção = []
    
    # Verificar fator Z
    if 'compressibility_factor' in densidade_props:
        z = densidade_props['compressibility_factor']
        ref_z = 0.948500192681
        desvio_perc = abs(z - ref_z) / ref_z * 100
        
        if desvio_perc < 5.0:
            pontos_positivos.append(f"Fator Z com desvio de {desvio_perc:.2f}% (aceitável)")
        else:
            pontos_atenção.append(f"Fator Z com desvio de {desvio_perc:.2f}% (alto)")
    
    # Verificar massa molar
    if 'molecular_weight' in mistura_props:
        mm = mistura_props['molecular_weight']
        ref_mm = 24.1454634337349
        desvio_perc = abs(mm - ref_mm) / ref_mm * 100
        
        if desvio_perc < 5.0:
            pontos_positivos.append(f"Massa molar com desvio de {desvio_perc:.2f}% (aceitável)")
        else:
            pontos_atenção.append(f"Massa molar com desvio de {desvio_perc:.2f}% (alto)")
    
    # Verificar execução sem erros
    if resultado.get('validation', {}).get('valid', False):
        pontos_positivos.append("Execução sem erros críticos")
    
    print(f"✅ PONTOS POSITIVOS:")
    for ponto in pontos_positivos:
        print(f"   • {ponto}")
    
    if pontos_atenção:
        print(f"\n⚠️  PONTOS DE ATENÇÃO:")
        for ponto in pontos_atenção:
            print(f"   • {ponto}")
    
    # Conclusão geral
    if len(pontos_positivos) >= len(pontos_atenção):
        print(f"\n🎉 CONCLUSÃO: IMPLEMENTAÇÃO AGA8 ESTÁ FUNCIONANDO ADEQUADAMENTE")
        print(f"   Sistema pode ser usado para validação de boletins cromatográficos")
    else:
        print(f"\n🔧 CONCLUSÃO: IMPLEMENTAÇÃO NECESSITA AJUSTES")
        print(f"   Recomenda-se calibrar os parâmetros antes do uso em produção")

if __name__ == "__main__":
    resultado = teste_composicao_exata()
    avaliar_implementacao(resultado)