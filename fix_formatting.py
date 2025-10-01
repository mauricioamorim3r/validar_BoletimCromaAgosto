# -*- coding: utf-8 -*-
"""
Script para corrigir problemas de formatação específicos
"""

import re

def fix_formatting_issues():
    """
    Corrige problemas específicos de formatação nos arquivos
    """

    # Corrigir aga8_dc_calibrado.py
    try:
        with open('aga8_dc_calibrado.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Corrigir indentação da lista thermo_props
        old_pattern = r"    thermo_props = \['energy', 'enthalpy', 'entropy', 'isochoric_heat_capacity',\s*\n\s*'isobaric_heat_capacity', 'speed_of_sound', 'gibbs_energy',\s*\n\s*'joule_thomson_coefficient', 'isentropic_exponent'\]"
        new_pattern = "    thermo_props = ['energy', 'enthalpy', 'entropy', 'isochoric_heat_capacity',\n                    'isobaric_heat_capacity', 'speed_of_sound', 'gibbs_energy',\n                    'joule_thomson_coefficient', 'isentropic_exponent']"

        content = re.sub(old_pattern, new_pattern, content, flags=re.MULTILINE)

        # Remover espaços em branco no final das linhas
        content = '\n'.join(line.rstrip() for line in content.split('\n'))

        with open('aga8_dc_calibrado.py', 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ aga8_dc_calibrado.py corrigido")
    except Exception as e:
        print(f"❌ Erro ao corrigir aga8_dc_calibrado.py: {e}")

    # Corrigir aga8_detailed_characterization.py
    try:
        with open('aga8_detailed_characterization.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Corrigir indentação da função calculate_density_detailed
        old_pattern = r"def calculate_density_detailed\(self, pressure_kpa: float, temperature_c: float,\s*\n\s*composition: Dict\[str, float\]\) -> float:"
        new_pattern = "def calculate_density_detailed(self, pressure_kpa: float, temperature_c: float,\n                               composition: Dict[str, float]) -> float:"

        content = re.sub(old_pattern, new_pattern, content, flags=re.MULTILINE)

        # Remover espaços em branco no final das linhas
        content = '\n'.join(line.rstrip() for line in content.split('\n'))

        with open('aga8_detailed_characterization.py', 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ aga8_detailed_characterization.py corrigido")
    except Exception as e:
        print(f"❌ Erro ao corrigir aga8_detailed_characterization.py: {e}")

if __name__ == "__main__":
    fix_formatting_issues()
    print("\n🎉 Correção de formatação concluída!")
