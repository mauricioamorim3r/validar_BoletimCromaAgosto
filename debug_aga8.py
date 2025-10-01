"""
Debug do AGA 8 - Teste simples
"""

from aga8_gerg2008 import AGA8_GERG2008

def debug_test():
    """Teste de debug"""

    composition = {
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

    try:
        print("Iniciando debug...")
        aga8 = AGA8_GERG2008()
        print("Calculador criado com sucesso")

        # Testar validação de composição
        is_valid, message, norm_comp = aga8.validate_composition(composition)
        print(f"Validação: {is_valid}, Mensagem: {message}")

        if is_valid:
            print("Composição normalizada:")
            for comp, fraction in norm_comp.items():
                print(f"  {comp}: {fraction:.6f}")

            # Testar propriedades da mistura
            print("\nTestando propriedades da mistura...")
            mix_props = aga8.calculate_mixture_properties(norm_comp)
            print(f"Massa molar: {mix_props}")

            # Testar cálculo completo
            print("\nCalculando propriedades completas...")
            results = aga8.calculate_gas_properties(558.0, 55.0, composition)

            if 'error' in results:
                print(f"Erro: {results['error']}")
            else:
                print("Cálculo bem-sucedido!")
                print(f"Densidade: {results['density_properties']['density_kg_m3']:.4f} kg/m³")

        else:
            print(f"Composição inválida: {message}")

    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    debug_test()
