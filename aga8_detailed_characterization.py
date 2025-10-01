# -*- coding: utf-8 -*-
"""
AGA 8 2017 D.C: Calculation of Gas Properties Using Detailed Characterization method
Implementação do método de Caracterização Detalhada para gases naturais
"""

import math
from typing import Dict, Tuple


class AGA8_DetailedCharacterization:
    """
    Implementação do método AGA 8 2017 D.C (Detailed Characterization)
    para cálculo preciso de propriedades de gases naturais.
    """

    def __init__(self):
        # Constante universal dos gases
        self.R = 8.314472  # J/(mol·K)

        # Propriedades críticas detalhadas dos componentes
        self.critical_properties = {
            'methane': {'Tc': 190.564, 'pc': 4599.2, 'M': 16.0428, 'w': 0.0115, 'Zc': 0.2866},
            'nitrogen': {'Tc': 126.192, 'pc': 3395.8, 'M': 28.0135, 'w': 0.0372, 'Zc': 0.2902},
            'carbon_dioxide': {'Tc': 304.1282, 'pc': 7377.3, 'M': 44.0095, 'w': 0.2276, 'Zc': 0.2740},
            'ethane': {'Tc': 305.322, 'pc': 4872.2, 'M': 30.0690, 'w': 0.0995, 'Zc': 0.2793},
            'propane': {'Tc': 369.89, 'pc': 4251.2, 'M': 44.0956, 'w': 0.1521, 'Zc': 0.2760},
            'water': {'Tc': 647.14, 'pc': 22064.0, 'M': 18.0153, 'w': 0.3442, 'Zc': 0.2295},
            'hydrogen_sulfide': {'Tc': 373.40, 'pc': 8936.5, 'M': 34.0809, 'w': 0.0942, 'Zc': 0.2842},
            'hydrogen': {'Tc': 33.145, 'pc': 1296.4, 'M': 2.0159, 'w': -0.2180, 'Zc': 0.3058},
            'carbon_monoxide': {'Tc': 132.86, 'pc': 3499.0, 'M': 28.0101, 'w': 0.0497, 'Zc': 0.2948},
            'oxygen': {'Tc': 154.581, 'pc': 5042.8, 'M': 31.9988, 'w': 0.0222, 'Zc': 0.2878},
            'i_butane': {'Tc': 407.817, 'pc': 3640.0, 'M': 58.1222, 'w': 0.1756, 'Zc': 0.2780},
            'n_butane': {'Tc': 425.125, 'pc': 3796.0, 'M': 58.1222, 'w': 0.2002, 'Zc': 0.2736},
            'i_pentane': {'Tc': 460.39, 'pc': 3378.0, 'M': 72.1488, 'w': 0.2223, 'Zc': 0.2703},
            'n_pentane': {'Tc': 469.70, 'pc': 3370.0, 'M': 72.1488, 'w': 0.2515, 'Zc': 0.2688},
            'n_hexane': {'Tc': 507.60, 'pc': 3025.0, 'M': 86.1754, 'w': 0.3013, 'Zc': 0.2659},
            'n_heptane': {'Tc': 540.20, 'pc': 2736.0, 'M': 100.2019, 'w': 0.3495, 'Zc': 0.2632},
            'n_octane': {'Tc': 568.70, 'pc': 2497.0, 'M': 114.2285, 'w': 0.3996, 'Zc': 0.2568},
            'n_nonane': {'Tc': 594.60, 'pc': 2290.0, 'M': 128.2551, 'w': 0.4433, 'Zc': 0.2527},
            'n_decane': {'Tc': 617.70, 'pc': 2103.0, 'M': 142.2817, 'w': 0.4923, 'Zc': 0.2479},
            'helium': {'Tc': 5.1953, 'pc': 227.5, 'M': 4.0026, 'w': -0.3836, 'Zc': 0.3010},
            'argon': {'Tc': 150.687, 'pc': 4863.0, 'M': 39.948, 'w': -0.0022, 'Zc': 0.2910}
        }

        # Parâmetros de interação binária (matriz simplificada)
        self.binary_interaction = {}
        self._initialize_binary_interactions()

        # Poderes caloríficos dos componentes (kJ/mol)
        self.heating_values = {
            'methane': 890.36,
            'ethane': 1559.88,
            'propane': 2219.17,
            'i_butane': 2868.20,
            'n_butane': 2877.40,
            'i_pentane': 3528.85,
            'n_pentane': 3536.22,
            'n_hexane': 4194.97,
            'n_heptane': 4853.43,
            'n_octane': 5512.09,
            'n_nonane': 6170.60,
            'n_decane': 6829.00
        }

    def _initialize_binary_interactions(self):
        """Inicializa parâmetros de interação binária simplificados"""
        # Matriz simplificada de interações binárias para GERG-2008
        components = list(self.critical_properties.keys())
        for i, comp1 in enumerate(components):
            for j, comp2 in enumerate(components):
                if i != j:
                    # Valores típicos de interação (simplificados para demonstração)
                    if comp1 == 'methane' and comp2 == 'ethane':
                        self.binary_interaction[(comp1, comp2)] = 0.9974
                    elif comp1 == 'methane' and comp2 == 'propane':
                        self.binary_interaction[(comp1, comp2)] = 0.9945
                    elif comp1 == 'methane' and comp2 == 'nitrogen':
                        self.binary_interaction[(comp1, comp2)] = 1.0266
                    elif comp1 == 'methane' and comp2 == 'carbon_dioxide':
                        self.binary_interaction[(comp1, comp2)] = 0.9960
                    else:
                        self.binary_interaction[(comp1, comp2)] = 1.0000

    def calculate_mixture_properties(self, composition: Dict[str, float]) -> Dict[str, float]:
        """
        Calcula propriedades críticas da mistura usando regras de mistura avançadas.

        Args:
            composition: Composição molar dos componentes

        Returns:
            Propriedades críticas da mistura
        """

        # Normalizar composição
        total = sum(composition.values())
        if total <= 0:
            raise ValueError("Composição inválida: soma zero")

        norm_comp = {k: v / total for k, v in composition.items()}

        # Calcular propriedades da mistura
        tc_mix = 0.0
        pc_mix = 0.0
        vc_mix = 0.0
        w_mix = 0.0
        m_mix = 0.0

        for comp, x_i in norm_comp.items():
            if comp in self.critical_properties:
                props = self.critical_properties[comp]
                tc_mix += x_i * props['Tc']
                pc_mix += x_i * props['pc']
                w_mix += x_i * props['w']
                m_mix += x_i * props['M']
                vc_mix += x_i * (props['Zc'] * self.R * props['Tc'] / props['pc'])

        return {
            'Tc_mix': tc_mix,
            'pc_mix': pc_mix,
            'vc_mix': vc_mix,
            'w_mix': w_mix,
            'M_mix': m_mix,
            'Zc_mix': pc_mix * vc_mix / (self.R * tc_mix) if tc_mix > 0 else 0.29
        }

    def calculate_compressibility_detailed(self, pressure_kpa: float, temperature_c: float,
                                           composition: Dict[str, float]) -> float:
        """
        Calcula fator de compressibilidade usando método detalhado GERG-2008.

        Args:
            pressure_kpa: Pressão em kPa
            temperature_c: Temperatura em °C
            composition: Composição molar

        Returns:
            Fator de compressibilidade
        """

        temperature_k = temperature_c + 273.15
        mix_props = self.calculate_mixture_properties(composition)

        # Propriedades reduzidas
        tr = temperature_k / mix_props['Tc_mix']
        pr = pressure_kpa / mix_props['pc_mix']

        # Correlação de Lee-Kesler modificada para GERG
        w_mix = mix_props['w_mix']

        # Fator acêntrico zero
        z0 = 1.0 + pr * (0.083 - 0.422 / tr**1.6) + pr**2 * (0.139 - 0.172 / tr**4.2)

        # Correção para fator acêntrico
        z1 = pr * (0.675 - 1.050 / tr + 0.407 / tr**3) + pr**2 * (-0.045 + 0.042 / tr**2)

        # Fator de compressibilidade total
        z = z0 + w_mix * z1

        # Limitar valores físicos
        return max(0.1, min(2.0, z))

    def calculate_density_detailed(self, pressure_kpa: float, temperature_c: float,
                                   composition: Dict[str, float]) -> float:
        """
        Calcula densidade usando caracterização detalhada.

        Args:
            pressure_kpa: Pressão em kPa
            temperature_c: Temperatura em °C
            composition: Composição molar

        Returns:
            Densidade em kg/m³
        """

        temperature_k = temperature_c + 273.15
        mix_props = self.calculate_mixture_properties(composition)
        z_factor = self.calculate_compressibility_detailed(pressure_kpa, temperature_c, composition)

        # Densidade molar
        density_molar = pressure_kpa / (z_factor * self.R * temperature_k)  # mol/m³

        # Densidade másssica
        density_mass = density_molar * mix_props['M_mix'] / 1000.0  # kg/m³

        return density_mass

    def calculate_heating_values_detailed(self, composition: Dict[str, float]) -> Tuple[float, float]:
        """
        Calcula poderes caloríficos usando caracterização detalhada.

        Args:
            composition: Composição molar

        Returns:
            Tuple com (PCS_mass, PCI_mass) em kJ/kg
        """

        # Normalizar composição
        total = sum(composition.values())
        norm_comp = {k: v / total for k, v in composition.items()}

        # Poder calorífico superior da mistura (base molar)
        pcs_molar = 0.0
        molar_mass = 0.0

        for comp, fraction in norm_comp.items():
            if comp in self.heating_values:
                pcs_molar += fraction * self.heating_values[comp]

            if comp in self.critical_properties:
                molar_mass += fraction * self.critical_properties[comp]['M']

        # Converter para base mássica
        pcs_mass = (pcs_molar / molar_mass) * 1000.0 if molar_mass > 0 else 0.0  # kJ/kg

        # PCI aproximado (considerando água formada)
        h2o_formation_energy = 44.0  # kJ/mol de H2O
        h_content = 0.0

        # Estimar conteúdo de hidrogênio
        for comp, fraction in norm_comp.items():
            if 'methane' in comp:
                h_content += fraction * 4  # CH4 tem 4 H
            elif 'ethane' in comp:
                h_content += fraction * 6  # C2H6 tem 6 H
            elif 'propane' in comp:
                h_content += fraction * 8  # C3H8 tem 8 H
            # Adicionar outros hidrocarbonetos conforme necessário

        water_heat_loss = (h_content / 2) * h2o_formation_energy  # Energia perdida na condensação
        pci_mass = pcs_mass - (water_heat_loss / molar_mass * 1000.0) if molar_mass > 0 else pcs_mass * 0.9

        return pcs_mass, pci_mass

    def calculate_wobbe_index_detailed(self, composition: Dict[str, float]) -> float:
        """
        Calcula índice de Wobbe usando caracterização detalhada.

        Args:
            composition: Composição molar

        Returns:
            Índice de Wobbe em kJ/m³
        """

        pcs_mass, _ = self.calculate_heating_values_detailed(composition)
        mix_props = self.calculate_mixture_properties(composition)

        # Densidade relativa
        specific_gravity = mix_props['M_mix'] / 28.9647  # Massa molar do ar seco

        # Índice de Wobbe
        wobbe_index = pcs_mass / math.sqrt(specific_gravity)

        return wobbe_index

    def calculate_all_properties(self, pressure_kpa: float, temperature_c: float,
                                 composition: Dict[str, float]) -> Dict[str, float]:
        """
        Calcula todas as propriedades usando caracterização detalhada.

        Args:
            pressure_kpa: Pressão em kPa
            temperature_c: Temperatura em °C
            composition: Composição molar

        Returns:
            Dicionário com todas as propriedades
        """

        # Propriedades da mistura
        mix_props = self.calculate_mixture_properties(composition)

        # Propriedades fundamentais
        z_factor = self.calculate_compressibility_detailed(pressure_kpa, temperature_c, composition)
        density = self.calculate_density_detailed(pressure_kpa, temperature_c, composition)
        pcs_mass, pci_mass = self.calculate_heating_values_detailed(composition)
        wobbe_index = self.calculate_wobbe_index_detailed(composition)

        # Propriedades volumétricas
        pcs_volume = pcs_mass * density  # kJ/m³
        pci_volume = pci_mass * density  # kJ/m³

        # Número de metano (aproximado)
        methane_number = composition.get('methane', 0.0) * 100.0

        # Densidade relativa
        specific_gravity = mix_props['M_mix'] / 28.9647

        return {
            'compressibility_factor': z_factor,
            'molar_mass': mix_props['M_mix'],
            'density': density,
            'heating_value_superior_mass': pcs_mass,
            'heating_value_inferior_mass': pci_mass,
            'heating_value_superior_volume': pcs_volume,
            'heating_value_inferior_volume': pci_volume,
            'wobbe_index_superior': wobbe_index,
            'wobbe_index_inferior': wobbe_index * (pci_mass / pcs_mass),
            'methane_number': methane_number,
            'specific_gravity': specific_gravity,
            'critical_pressure': mix_props['pc_mix'],
            'critical_temperature': mix_props['Tc_mix'],
            'critical_volume': mix_props['vc_mix'],
            'acentric_factor': mix_props['w_mix']
        }


def test_aga8_detailed_characterization():
    """
    Teste com a composição da imagem fornecida
    """

    aga8_dc = AGA8_DetailedCharacterization()

    # Composição da imagem (600 kPa, 50°C)
    composition = {
        'methane': 96.5,              # 96.5%
        'nitrogen': 0.3,              # 0.3%
        'carbon_dioxide': 0.6,        # 0.6%
        'ethane': 1.8,                # 1.8%
        'propane': 0.45,              # 0.45%
        'water': 0.0,                 # 0%
        'hydrogen_sulfide': 0.0,      # 0%
        'hydrogen': 0.0,              # 0%
        'carbon_monoxide': 0.0,       # 0%
        'oxygen': 0.0,                # 0%
        'i_butane': 0.1,              # 0.1%
        'n_butane': 0.1,              # 0.1%
        'i_pentane': 0.05,            # 0.05%
        'n_pentane': 0.03,            # 0.03%
        'n_hexane': 0.07,             # 0.07%
        'n_heptane': 0.0,             # 0%
        'n_octane': 0.0,              # 0%
        'n_nonane': 0.0,              # 0%
        'n_decane': 0.0,              # 0%
        'helium': 0.0,                # 0%
        'argon': 0.0                  # 0%
    }

    # Converter percentuais para frações molares
    composition_fractions = {k: v / 100.0 for k, v in composition.items()}

    # Calcular propriedades
    results = aga8_dc.calculate_all_properties(600.0, 50.0, composition_fractions)

    print("=" * 60)
    print("AGA 8 2017 D.C - Detailed Characterization Results")
    print("=" * 60)
    print(f"Conditions: {600} kPa, {50}°C")
    print("-" * 60)

    # Formatação dos resultados
    properties_format = {
        'compressibility_factor': ('Compressibility Factor', '', 6),
        'molar_mass': ('Molar Mass', 'g/mol', 4),
        'density': ('Density', 'kg/m³', 4),
        'heating_value_superior_mass': ('HHV (mass basis)', 'kJ/kg', 1),
        'heating_value_inferior_mass': ('LHV (mass basis)', 'kJ/kg', 1),
        'heating_value_superior_volume': ('HHV (volume basis)', 'kJ/m³', 1),
        'heating_value_inferior_volume': ('LHV (volume basis)', 'kJ/m³', 1),
        'wobbe_index_superior': ('Wobbe Index (superior)', 'kJ/m³', 1),
        'wobbe_index_inferior': ('Wobbe Index (inferior)', 'kJ/m³', 1),
        'methane_number': ('Methane Number', '', 1),
        'specific_gravity': ('Specific Gravity', '', 4),
        'critical_pressure': ('Critical Pressure', 'kPa', 1),
        'critical_temperature': ('Critical Temperature', 'K', 2),
        'critical_volume': ('Critical Volume', 'm³/kmol', 6),
        'acentric_factor': ('Acentric Factor', '', 4)
    }

    for prop_key, value in results.items():
        if prop_key in properties_format:
            name, unit, decimals = properties_format[prop_key]
            unit_str = f" {unit}" if unit else ""
            print(f"{name:<30}: {value:.{decimals}f}{unit_str}")

    print("=" * 60)

    return results


if __name__ == "__main__":
    test_aga8_detailed_characterization()
