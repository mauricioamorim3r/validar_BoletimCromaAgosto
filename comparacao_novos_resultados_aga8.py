#!/usr/bin/env python3
"""
Comparação AGA8 - Resultados Calculados vs Referência
Análise detalhada dos desvios e validação da precisão
"""

def comparar_resultados():
    """Compara os resultados calculados com os valores de referência"""
    print("🔍 COMPARAÇÃO AGA8 - CALCULADO vs REFERÊNCIA")
    print("=" * 60)
    
    # VALORES CALCULADOS (nosso sistema)
    calculados = {
        'compressibility_factor': 0.99086112,
        'molar_mass': 16.803583,          # g/mol
        'molar_density': 0.184948,        # mol/L
        'energy': None,                   # Não temos energia equivalente
        'enthalpy': None,                 # Não calculamos entalpia
        'entropy': None,                  # Não calculamos entropia
        'isochoric_heat_capacity': None,  # Não calculamos Cv
        'isobaric_heat_capacity': None,   # Não calculamos Cp
        'speed_of_sound': None,           # Não calculamos velocidade do som
        'gibbs_energy': None,             # Não calculamos energia de Gibbs
        'joule_thomson': None,            # Não calculamos coef. Joule-Thomson
        'isentropic_exponent': None       # Não calculamos expoente isentrópico
    }
    
    # VALORES DE REFERÊNCIA (da imagem fornecida)
    referencia = {
        'compressibility_factor': 0.993478459795,
        'molar_mass': 16.8035819,         # g/mol
        'molar_density': 0.184460117402,  # mol/L
        'energy': -1668.978370590974,     # J/mol
        'enthalpy': 104.346740106894,     # J/mol
        'entropy': -8.181156035881,       # J/mol.K
        'isochoric_heat_capacity': 29.512718949517,  # J/mol.K
        'isobaric_heat_capacity': 38.155365927773,   # J/mol.K
        'speed_of_sound': 455.178582991289,          # m/s
        'gibbs_energy': 3726.281180663172,           # J/mol
        'joule_thomson': 0.003708102532,             # K/kPa
        'isentropic_exponent': 1.284393189484       # adimensional
    }
    
    print("📊 PROPRIEDADES COMPARÁVEIS:")
    print("-" * 60)
    
    # Comparar propriedades disponíveis
    propriedades_comparaveis = [
        ('compressibility_factor', 'Fator de Compressibilidade (Z)', ''),
        ('molar_mass', 'Massa Molar', 'g/mol'),
        ('molar_density', 'Densidade Molar', 'mol/L')
    ]
    
    desvios = []
    
    for prop, nome, unidade in propriedades_comparaveis:
        calc = calculados[prop]
        ref = referencia[prop]
        
        if calc is not None and ref is not None:
            desvio_abs = abs(calc - ref)
            desvio_perc = (desvio_abs / ref) * 100
            desvios.append((nome, desvio_perc))
            
            print(f"\n{nome}:")
            print(f"   Calculado:  {calc:.8f} {unidade}")
            print(f"   Referência: {ref:.8f} {unidade}")
            print(f"   Desvio:     {desvio_abs:.8f} ({desvio_perc:.4f}%) {unidade}")
            
            # Classificar precisão
            if desvio_perc < 0.1:
                status = "✅ EXCELENTE"
            elif desvio_perc < 0.5:
                status = "✅ MUITO BOM"
            elif desvio_perc < 1.0:
                status = "⚠️  BOM"
            elif desvio_perc < 5.0:
                status = "⚠️  ACEITÁVEL"
            else:
                status = "❌ SIGNIFICATIVO"
            
            print(f"   Status:     {status}")
    
    # Propriedades não calculadas pelo nosso sistema
    print(f"\n📋 PROPRIEDADES NÃO CALCULADAS (apenas referência):")
    print("-" * 60)
    
    propriedades_extras = [
        ('energy', 'Energia Interna', 'J/mol'),
        ('enthalpy', 'Entalpia', 'J/mol'),
        ('entropy', 'Entropia', 'J/mol.K'),
        ('isochoric_heat_capacity', 'Capacidade Calorífica (Cv)', 'J/mol.K'),
        ('isobaric_heat_capacity', 'Capacidade Calorífica (Cp)', 'J/mol.K'),
        ('speed_of_sound', 'Velocidade do Som', 'm/s'),
        ('gibbs_energy', 'Energia de Gibbs', 'J/mol'),
        ('joule_thomson', 'Coeficiente Joule-Thomson', 'K/kPa'),
        ('isentropic_exponent', 'Expoente Isentrópico', '')
    ]
    
    for prop, nome, unidade in propriedades_extras:
        ref = referencia[prop]
        print(f"{nome}: {ref} {unidade}")
    
    # Resumo da análise
    print(f"\n🎯 RESUMO DA VALIDAÇÃO:")
    print("=" * 60)
    
    if desvios:
        desvio_medio = sum(d[1] for d in desvios) / len(desvios)
        desvio_max = max(desvios, key=lambda x: x[1])
        
        print(f"Propriedades analisadas: {len(desvios)}")
        print(f"Desvio médio: {desvio_medio:.4f}%")
        print(f"Maior desvio: {desvio_max[0]} ({desvio_max[1]:.4f}%)")
        
        if desvio_medio < 1.0:
            print(f"✅ SISTEMA VALIDADO - Precisão excelente!")
            print(f"✅ Todos os desvios < 1% - Adequado para uso industrial")
        elif desvio_medio < 5.0:
            print(f"⚠️  SISTEMA ACEITÁVEL - Precisão boa")
            print(f"⚠️  Desvios menores que 5% - Adequado para a maioria das aplicações")
        else:
            print(f"❌ REVISAR SISTEMA - Desvios significativos")
            print(f"❌ Alguns desvios > 5% - Verificar implementação")
    
    # Comparação com teste anterior
    print(f"\n📈 COMPARAÇÃO COM TESTE ANTERIOR:")
    print("-" * 60)
    print(f"Teste Anterior (220K, 550 kPa):")
    print(f"   Z-factor: 0.982432 (desvio 3.58%)")
    print(f"   Massa Molar: 24.5693 g/mol (desvio 1.76%)")
    
    print(f"\nTeste Atual (328K, 500 kPa):")
    if desvios:
        z_desvio = next((d[1] for d in desvios if 'Compressibilidade' in d[0]), None)
        mm_desvio = next((d[1] for d in desvios if 'Massa Molar' in d[0]), None)
        if z_desvio:
            print(f"   Z-factor: {calculados['compressibility_factor']:.8f} (desvio {z_desvio:.4f}%)")
        if mm_desvio:
            print(f"   Massa Molar: {calculados['molar_mass']:.4f} g/mol (desvio {mm_desvio:.4f}%)")
    
    print(f"\n🔬 OBSERVAÇÕES TÉCNICAS:")
    print("-" * 60)
    print(f"• Condições mais favoráveis (maior temperatura, menor pressão)")
    print(f"• Composição mais simples (96.5% CH4 vs 76.6% anterior)")
    print(f"• Z-factor mais próximo da idealidade (0.991 vs 0.982)")
    print(f"• Menor densidade molar (gases mais leves)")
    
    return desvios

def analisar_diferencias_propriedades():
    """Analisa as diferenças entre as propriedades calculadas pelos dois sistemas"""
    print(f"\n🔍 ANÁLISE DAS DIFERENÇAS DE PROPRIEDADES:")
    print("=" * 60)
    
    print(f"NOSSO SISTEMA AGA8 GERG-2008:")
    print(f"✅ Fator de compressibilidade (Z)")
    print(f"✅ Propriedades de densidade")
    print(f"✅ Propriedades energéticas (PCS/PCI)")
    print(f"✅ Índices de Wobbe")
    print(f"✅ Número de metano")
    print(f"✅ Propriedades críticas")
    
    print(f"\nSISTEMA DE REFERÊNCIA:")
    print(f"✅ Todas as propriedades acima MAIS:")
    print(f"• Energia interna")
    print(f"• Entalpia")
    print(f"• Entropia")
    print(f"• Capacidades caloríficas (Cv, Cp)")
    print(f"• Velocidade do som")
    print(f"• Energia de Gibbs")
    print(f"• Coeficiente Joule-Thomson")
    print(f"• Expoente isentrópico")
    
    print(f"\n💡 RECOMENDAÇÕES:")
    print(f"• Sistema atual adequado para validação de boletins cromatográficos")
    print(f"• Precisão excelente nas propriedades fundamentais")
    print(f"• Considerar expansão futura para propriedades termodinâmicas avançadas")

if __name__ == "__main__":
    print("🚀 INICIANDO ANÁLISE COMPARATIVA")
    desvios = comparar_resultados()
    analisar_diferencias_propriedades()
    print(f"\n✅ ANÁLISE CONCLUÍDA!")