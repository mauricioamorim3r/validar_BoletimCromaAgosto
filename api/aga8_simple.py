# -*- coding: utf-8 -*-
"""
Versão Simplificada do AGA8 para Vercel Serverless
Calculadora básica de propriedades de gás natural
"""




class AGA8_GERG2008_Simple:
    """Versão simplificada do AGA8 para ambiente serverless"""
    
    def __init__(self):
        # Componentes suportados (versão simplificada)
        self.components = {
            'Metano': {'weight': 16.043, 'tc': 190.564, 'pc': 45.99},
            'Etano': {'weight': 30.070, 'tc': 305.322, 'pc': 48.72},
            'Propano': {'weight': 44.097, 'tc': 369.830, 'pc': 42.48},
            'n-Butano': {'weight': 58.123, 'tc': 425.125, 'pc': 37.96},
            'Nitrogênio': {'weight': 28.014, 'tc': 126.192, 'pc': 33.958},
            'CO2': {'weight': 44.010, 'tc': 304.128, 'pc': 73.77}
        }
        
    def validate_composition(self, composition):
        """Valida e normaliza composição"""
        try:
            if not composition:
                return False, "Composição vazia", {}
            
            # Verificar componentes válidos
            invalid_components = []
            for comp in composition.keys():
                if comp not in self.components:
                    invalid_components.append(comp)
            
            if invalid_components:
                return False, f"Componentes inválidos: {invalid_components}", {}
            
            # Normalizar composição
            total = sum(composition.values())
            if total <= 0:
                return False, "Soma da composição deve ser > 0", {}
            
            normalized = {comp: (value / total) * 100
                          for comp, value in composition.items()}
            
            return True, "Composição válida", normalized
            
        except Exception as e:
            return False, f"Erro na validação: {e}", {}
    
    def calculate_properties(self, temperature_r, pressure_psia, composition):
        """
        Cálculo simplificado de propriedades
        
        Args:
            temperature_r: Temperatura em Rankine
            pressure_psia: Pressão em psia
            composition: Composição normalizada
        
        Returns:
            dict: Propriedades calculadas
        """
        try:
            # Converter unidades
            temp_k = temperature_r / 1.8  # Rankine para Kelvin
            press_mpa = pressure_psia * 0.00689476  # psia para MPa
            
            # Calcular propriedades médias da mistura
            avg_molecular_weight = 0
            avg_tc = 0
            avg_pc = 0
            
            for comp, fraction in composition.items():
                if comp in self.components:
                    props = self.components[comp]
                    frac_decimal = fraction / 100.0
                    
                    avg_molecular_weight += props['weight'] * frac_decimal
                    avg_tc += props['tc'] * frac_decimal
                    avg_pc += props['pc'] * frac_decimal
            
            # Calcular propriedades reduzidas
            tr = temp_k / avg_tc  # Temperatura reduzida
            pr = press_mpa / avg_pc  # Pressão reduzida
            
            # Fator de compressibilidade (aproximação simplificada)
            # Baseado na equação de Pitzer
            z_factor = self._calculate_z_factor(tr, pr)
            
            # Densidade (kg/m³)
            # ρ = (P * MW) / (Z * R * T)
            R = 0.008314  # Constante dos gases (MPa·m³)/(kmol·K)
            density = (press_mpa * avg_molecular_weight) / (z_factor * R * temp_k)
            
            # Densidade relativa (ar = 1.0)
            air_density = 28.97  # Peso molecular médio do ar
            relative_density = avg_molecular_weight / air_density
            
            return {
                'density': density,
                'compressibility_factor': z_factor,
                'molecular_weight': avg_molecular_weight,
                'relative_density': relative_density,
                'reduced_temperature': tr,
                'reduced_pressure': pr,
                'temperature_k': temp_k,
                'pressure_mpa': press_mpa,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'density': 0.0,
                'compressibility_factor': 1.0,
                'error': str(e),
                'status': 'error'
            }
    
    def _calculate_z_factor(self, tr, pr):
        """
        Cálculo simplificado do fator de compressibilidade
        Baseado em correlações generalizadas
        """
        try:
            # Correlação de Lee-Kesler simplificada
            if pr < 0.1:
                # Gás ideal para pressões baixas
                return 1.0
            
            # Aproximação para gases reais
            # Z = 1 + B*P/RT (aproximação virial truncada)
            b0 = 0.083 - 0.422 / (tr ** 1.6)
            b1 = 0.139 - 0.172 / (tr ** 4.2)
            
            B = b0 + b1 * pr
            z_factor = 1.0 + B * pr / tr
            
            # Limitar valores físicos
            z_factor = max(0.1, min(2.0, z_factor))
            
            return z_factor
            
        except Exception:
            return 1.0  # Fallback para gás ideal


# Alias para compatibilidade
AGA8_GERG2008 = AGA8_GERG2008_Simple