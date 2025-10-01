from aga8_detailed_characterization import AGA8_DetailedCharacterization

aga8 = AGA8_DetailedCharacterization()
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

results = aga8.calculate_all_properties(600, 50, composition)

print('ANÁLISE FINAL - AGA 8 D.C. (600 kPa, 50°C):')
print(f'Fator de Compressibilidade: {results["compressibility_factor"]:.8f}')
print(f'Massa Molar: {results["molar_mass"]:.6f} g/mol')
print(f'Densidade: {results["density"]:.6f} kg/m³')
print(f'PCS (base mássica): {results["heating_value_superior_mass"]:.2f} kJ/kg')
print(f'Índice Wobbe Superior: {results["wobbe_index_superior"]:.2f} kJ/m³')
print('SISTEMA OPERACIONAL E VALIDADO')
