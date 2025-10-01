
# -*- coding: utf-8 -*-
"""AGA 8 2017 Part 2 - GERG 2008: Calculo de propriedades de gases naturais.
"""

from __future__ import annotations

import math
import unicodedata
from typing import Dict, Tuple

# Mapeamento de nomes alternativos de componentes para os identificadores canônicos
_COMPONENT_ALIAS_MAP = {
    'methane': 'methane',
    'metano': 'methane',
    'ch4': 'methane',
    'c1': 'methane',
    'nitrogen': 'nitrogen',
    'nitrogenio': 'nitrogen',
    'nitrogeno': 'nitrogen',
    'n2': 'nitrogen',
    'carbondioxide': 'carbon_dioxide',
    'dioxidocarbono': 'carbon_dioxide',
    'co2': 'carbon_dioxide',
    'ethane': 'ethane',
    'etano': 'ethane',
    'c2h6': 'ethane',
    'propane': 'propane',
    'propano': 'propane',
    'c3h8': 'propane',
    'isobutane': 'i-butane',
    'isobutano': 'i-butane',
    'ibutano': 'i-butane',
    'ic4h10': 'i-butane',
    'isobutene': 'i-butane',
    'isobutanoch4': 'i-butane',
    'isopentane': 'i-pentane',
    'isopentano': 'i-pentane',
    'ipentano': 'i-pentane',
    'ic5h12': 'i-pentane',
    'nbutane': 'n-butane',
    'n-butane': 'n-butane',
    'nbutano': 'n-butane',
    'n-butano': 'n-butane',
    'nc4h10': 'n-butane',
    'npentane': 'n-pentane',
    'n-pentane': 'n-pentane',
    'npentano': 'n-pentane',
    'nc5h12': 'n-pentane',
    'nhexane': 'n-hexane',
    'hexane': 'n-hexane',
    'hexano': 'n-hexane',
    'nc6h14': 'n-hexane',
    'nheptane': 'n-heptane',
    'heptane': 'n-heptane',
    'heptano': 'n-heptane',
    'nc7h16': 'n-heptane',
    'noctane': 'n-octane',
    'octane': 'n-octane',
    'octano': 'n-octane',
    'nc8h18': 'n-octane',
    'nnonane': 'n-nonane',
    'nonane': 'n-nonane',
    'nonano': 'n-nonane',
    'nc9h20': 'n-nonane',
    'ndecane': 'n-decane',
    'decane': 'n-decane',
    'decano': 'n-decane',
    'nc10h22': 'n-decane',
    'oxygen': 'oxygen',
    'oxigenio': 'oxygen',
    'oxigeno': 'oxygen',
    'o2': 'oxygen',
    'hydrogen': 'hydrogen',
    'hidrogenio': 'hydrogen',
    'h2': 'hydrogen',
    'carbonmonoxide': 'carbon_monoxide',
    'monoxido': 'carbon_monoxide',
    'co': 'carbon_monoxide',
    'water': 'water',
    'agua': 'water',
    'h2o': 'water',
    'helium': 'helium',
    'helio': 'helium',
    'he': 'helium',
    'argon': 'argon',
    'argao': 'argon',
    'ar': 'argon',
}

# Fórmulas simplificadas para relatório
_FORMULA_MAP = {
    'methane': 'CH4',
    'nitrogen': 'N2',
    'carbon_dioxide': 'CO2',
    'ethane': 'C2H6',
    'propane': 'C3H8',
    'i-butane': 'iC4H10',
    'n-butane': 'nC4H10',
    'i-pentane': 'iC5H12',
    'n-pentane': 'nC5H12',
    'n-hexane': 'nC6H14',
    'n-heptane': 'nC7H16',
    'n-octane': 'nC8H18',
    'n-nonane': 'nC9H20',
    'n-decane': 'nC10H22',
    'oxygen': 'O2',
    'carbon_monoxide': 'CO',
    'hydrogen': 'H2',
    'water': 'H2O',
    'helium': 'He',
    'argon': 'Ar',
}


class AGA8_GERG2008:
    """Implementação simplificada do método GERG 2008."""

    def __init__(self) -> None:
        self.R = 8.314472  # J/(mol·K)
        self.critical_properties = {
            'methane': {'Tc': 190.564, 'pc': 4599.2, 'M': 16.043},
            'nitrogen': {'Tc': 126.192, 'pc': 3395.8, 'M': 28.014},
            'carbon_dioxide': {'Tc': 304.1282, 'pc': 7377.3, 'M': 44.01},
            'ethane': {'Tc': 305.322, 'pc': 4872.2, 'M': 30.07},
            'propane': {'Tc': 369.89, 'pc': 4251.2, 'M': 44.097},
            'i-butane': {'Tc': 407.817, 'pc': 3640.0, 'M': 58.123},
            'n-butane': {'Tc': 425.125, 'pc': 3796.0, 'M': 58.123},
            'i-pentane': {'Tc': 460.39, 'pc': 3378.0, 'M': 72.15},
            'n-pentane': {'Tc': 469.7, 'pc': 3370.0, 'M': 72.15},
            'n-hexane': {'Tc': 507.6, 'pc': 3025.0, 'M': 86.177},
            'n-heptane': {'Tc': 540.2, 'pc': 2736.0, 'M': 100.204},
            'n-octane': {'Tc': 569.4, 'pc': 2480.0, 'M': 114.232},
            'n-nonane': {'Tc': 594.6, 'pc': 2290.0, 'M': 128.259},
            'n-decane': {'Tc': 617.7, 'pc': 2110.0, 'M': 142.286},
            'oxygen': {'Tc': 154.58, 'pc': 5043.0, 'M': 31.998},
            'hydrogen': {'Tc': 33.19, 'pc': 1296.0, 'M': 2.0158},
            'carbon_monoxide': {'Tc': 132.86, 'pc': 3494.0, 'M': 28.01},
            'water': {'Tc': 647.096, 'pc': 22055.0, 'M': 18.015},
            'helium': {'Tc': 5.1953, 'pc': 227.5, 'M': 4.0026},
            'argon': {'Tc': 150.86, 'pc': 4863.0, 'M': 39.948},
        }

    @staticmethod
    def _canonical_component(name: str) -> str | None:
        if not name:
            return None
        normalized = unicodedata.normalize('NFKD', str(name))
        normalized = normalized.encode('ascii', 'ignore').decode('ascii')
        normalized = normalized.lower().replace(' ', '').replace('-', '').replace('_', '')
        return _COMPONENT_ALIAS_MAP.get(normalized)

    @staticmethod
    def _component_formula(name: str) -> str:
        return _FORMULA_MAP.get(name, name)

    def normalize_composition(self, composition: Dict[str, float]) -> Tuple[bool, str, Dict[str, float]]:
        normalized: Dict[str, float] = {}
        total_raw = 0.0

        for component, value in composition.items():
            canonical = self._canonical_component(component)
            if canonical is None:
                continue
            try:
                fraction = float(value)
            except (TypeError, ValueError):
                continue
            if fraction < 0:
                fraction = 0.0
            normalized[canonical] = normalized.get(canonical, 0.0) + fraction
            total_raw += fraction

        if not normalized:
            return False, 'Nenhum componente reconhecido para o cálculo.', {}

        if total_raw <= 0:
            return False, 'Soma da composição igual a zero.', {}

        normalized = {k: v / total_raw for k, v in normalized.items()}

        missing = [comp for comp in ('methane', 'ethane', 'propane') if normalized.get(comp, 0.0) <= 0]
        if missing:
            faltantes = ', '.join(missing)
            return False, f'Componentes obrigatórios não encontrados: {faltantes}.', {}

        is_percent = total_raw > 1.5
        expected_total = 100.0 if is_percent else 1.0
        deviation = abs(total_raw - expected_total)
        tolerance = 5.0 if is_percent else 0.05

        if deviation > tolerance:
            unidade = '%' if is_percent else ''
            message = f'Composição normalizada; soma original {total_raw:.2f}{unidade}.'
        else:
            message = 'Composição normalizada com sucesso.'

        return True, message, normalized

    def validate_composition(self, composition: Dict[str, float]) -> Tuple[bool, str, Dict[str, float]]:
        return self.normalize_composition(composition)

    def calculate_molar_mass(self, composition: Dict[str, float]) -> float:
        return sum(
            fraction * self.critical_properties[component]['M']
            for component, fraction in composition.items()
            if component in self.critical_properties
        )

    def calculate_compressibility_factor(self, pressure_kpa: float, temperature_c: float,
                                         composition: Dict[str, float]) -> float:
        temperature_k = temperature_c + 273.15
        pr_mix = 0.0
        tr_mix = 0.0
        total_fraction = 0.0

        for component, fraction in composition.items():
            props = self.critical_properties.get(component)
            if not props:
                continue
            pr_mix += fraction * (pressure_kpa / props['pc'])
            tr_mix += fraction * (temperature_k / props['Tc'])
            total_fraction += fraction

        if total_fraction > 0:
            pr_mix /= total_fraction
            tr_mix /= total_fraction

        z = 1.0 + pr_mix * (0.083 - 0.422 / (tr_mix ** 1.6)) +             pr_mix ** 2 * (0.139 - 0.172 / (tr_mix ** 4.2))

        return max(0.1, min(1.5, z))

    def calculate_density(self, pressure_kpa: float, temperature_c: float,
                          composition: Dict[str, float]) -> float:
        molar_mass = self.calculate_molar_mass(composition)
        z_factor = self.calculate_compressibility_factor(pressure_kpa, temperature_c, composition)
        temperature_k = temperature_c + 273.15
        density = (pressure_kpa * molar_mass) / (z_factor * self.R * temperature_k)
        return density / 1000.0  # kg/m³

    def calculate_heating_values(self, composition: Dict[str, float]) -> Tuple[float, float]:
        heating_values = {
            'methane': 890.3,
            'ethane': 1559.9,
            'propane': 2219.9,
            'n-butane': 2877.4,
            'i-butane': 2868.8,
            'n-pentane': 3536.2,
            'i-pentane': 3528.8,
            'n-hexane': 4194.8,
            'n-heptane': 4850.0,
            'n-octane': 5505.0,
            'n-nonane': 6160.0,
            'n-decane': 6815.0,
        }

        total_hv = 0.0
        molar_mass = self.calculate_molar_mass(composition)
        for component, fraction in composition.items():
            if component in heating_values:
                total_hv += fraction * heating_values[component]

        pcs_mass = (total_hv / molar_mass) * 1000.0  # kJ/kg
        pci_mass = pcs_mass * 0.9
        return pcs_mass, pci_mass

    def calculate_wobbe_index(self, composition: Dict[str, float]) -> float:
        pcs_mass, _ = self.calculate_heating_values(composition)
        specific_gravity = self.calculate_specific_gravity(composition)
        return pcs_mass / math.sqrt(specific_gravity)

    def calculate_specific_gravity(self, composition: Dict[str, float]) -> float:
        molar_mass = self.calculate_molar_mass(composition)
        return molar_mass / 28.97

    def calculate_mixture_properties(self, composition: Dict[str, float]) -> Dict[str, float]:
        molar_mass = self.calculate_molar_mass(composition)
        critical_pressure = sum(
            composition.get(comp, 0.0) * props['pc']
            for comp, props in self.critical_properties.items()
        )
        critical_temperature = sum(
            composition.get(comp, 0.0) * props['Tc']
            for comp, props in self.critical_properties.items()
        )
        return {
            'molecular_weight': molar_mass,
            'critical_pressure': critical_pressure,
            'critical_temperature': critical_temperature,
        }

    def calculate_properties(self, pressure_kpa: float, temperature_c: float,
                              composition: Dict[str, float]) -> Dict[str, float]:
        valid, message, normalized = self.validate_composition(composition)
        if not valid:
            raise ValueError(message)

        pcs_mass, pci_mass = self.calculate_heating_values(normalized)
        z_factor = self.calculate_compressibility_factor(pressure_kpa, temperature_c, normalized)
        density = self.calculate_density(pressure_kpa, temperature_c, normalized)
        wobbe_index = self.calculate_wobbe_index(normalized)
        specific_gravity = self.calculate_specific_gravity(normalized)

        mix_props = self.calculate_mixture_properties(normalized)
        critical_pressure = mix_props['critical_pressure']
        critical_temperature = mix_props['critical_temperature']

        return {
            'compressibility_factor': z_factor,
            'molar_mass': mix_props['molecular_weight'],
            'density': density,
            'heating_value_mass': pcs_mass,
            'heating_value_mass_hhv': pcs_mass,
            'heating_value_mass_lhv': pci_mass,
            'heating_value_volume': pcs_mass * density,
            'heating_value_volume_hhv': pcs_mass * density,
            'heating_value_volume_lhv': pci_mass * density,
            'wobbe_index': wobbe_index,
            'methane_number': normalized.get('methane', 0.0) * 100.0,
            'specific_gravity': specific_gravity,
            'critical_pressure': critical_pressure,
            'critical_temperature': critical_temperature,
            'pseudo_critical_pressure': critical_pressure,
            'pseudo_critical_temperature': critical_temperature,
        }

    def calculate_gas_properties(self, pressure_kpa: float, temperature_c: float,
                                  composition: Dict[str, float]) -> Dict[str, object]:
        valid, message, normalized = self.validate_composition(composition)
        if not valid:
            return {
                'error': message,
                'validation': {'valid': False, 'message': message}
            }

        mix_props = self.calculate_mixture_properties(normalized)
        z_factor = self.calculate_compressibility_factor(pressure_kpa, temperature_c, normalized)
        density = self.calculate_density(pressure_kpa, temperature_c, normalized)
        pcs_mass, pci_mass = self.calculate_heating_values(normalized)
        wobbe_index = self.calculate_wobbe_index(normalized)
        specific_gravity = self.calculate_specific_gravity(normalized)

        hhv_vol = pcs_mass * density / 1000.0
        lhv_vol = pci_mass * density / 1000.0

        composition_molar = {
            self._component_formula(component): fraction
            for component, fraction in normalized.items()
        }

        return {
            'input_data': {
                'pressure_kpa': pressure_kpa,
                'temperature_c': temperature_c,
                'composition_raw': composition,
                'composition_molar': composition_molar,
            },
            'mixture_properties': {
                'molecular_weight': mix_props['molecular_weight'],
                'critical_temperature': mix_props['critical_temperature'],
                'critical_pressure': mix_props['critical_pressure'],
            },
            'density_properties': {
                'density_kg_m3': density,
                'relative_density': specific_gravity,
                'compressibility_factor': z_factor,
            },
            'heating_value': {
                'HHV_vol_MJ_m3': hhv_vol,
                'LHV_vol_MJ_m3': lhv_vol,
                'HHV_mass_MJ_kg': pcs_mass / 1000.0,
                'LHV_mass_MJ_kg': pci_mass / 1000.0,
            },
            'additional_properties': {
                'wobbe_index_HHV': wobbe_index / 1000.0,
                'wobbe_index_LHV': (wobbe_index * 0.9) / 1000.0,
                'methane_number': normalized.get('methane', 0.0) * 100.0,
            },
            'validation': {
                'valid': True,
                'message': message,
            }
        }


def test_aga8_gerg2008() -> Dict[str, float]:
    aga8 = AGA8_GERG2008()
    composition = {
        'methane': 0.965,
        'nitrogen': 0.003,
        'carbon_dioxide': 0.006,
        'ethane': 0.018,
        'propane': 0.0045,
        'n-butane': 0.001,
        'i-butane': 0.001,
        'i-pentane': 0.0005,
        'n-pentane': 0.0003,
        'n-hexane': 0.0007,
    }
    return aga8.calculate_properties(558, 55, composition)


if __name__ == '__main__':
    results = test_aga8_gerg2008()
    print('=== AGA 8 GERG 2008 - Resultados ===')
    for property_name, value in results.items():
        print(f'{property_name}: {value}')
