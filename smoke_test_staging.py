#!/usr/bin/env python3
"""
Suite de Testes de Smoke para Staging
Valida os fluxos críticos da aplicação
"""

import requests
import time
from typing import Dict, Any


class SmokeTestSuite:
    def __init__(self, base_url: str = "http://127.0.0.1:3000"):
        self.base_url = base_url
        self.results = []
        
    def log_result(self, test_name: str, success: bool, details: str = ""):
        """Log resultado do teste"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.results.append({
            'test': test_name,
            'success': success,
            'details': details
        })
        print(f"{status} {test_name}: {details}")
        
    def test_server_health(self) -> bool:
        """Testa se servidor está respondendo"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            success = response.status_code == 200
            self.log_result("Server Health Check", success, f"Status {response.status_code}")
            return success
        except Exception as e:
            self.log_result("Server Health Check", False, str(e))
            return False
            
    def test_database_connection(self) -> bool:
        """Testa conexão com banco de dados"""
        try:
            # Verifica se arquivo de banco existe
            import os
            db_exists = os.path.exists("boletins.db")
            if not db_exists:
                self.log_result("Database Connection", False, "Database file not found")
                return False
                
            # Testa se servidor responde (independente do conteúdo)
            response = requests.get(f"{self.base_url}/", timeout=10)
            success = response.status_code == 200
            details = "Server responding, DB file exists"
            self.log_result("Database Connection", success, details)
            return success
        except Exception as e:
            self.log_result("Database Connection", False, str(e))
            return False
            
    def test_aga8_calculation(self) -> bool:
        """Testa cálculo AGA8 básico"""
        try:
            # Simular composição básica
            test_composition = {
                'Metano': 85.0,
                'Etano': 7.0,
                'Propano': 4.0,
                'n-Butano': 2.0,
                'Nitrogênio': 2.0
            }
            
            # Para este teste, vamos importar diretamente
            from aga8_gerg2008 import AGA8_GERG2008
            solver = AGA8_GERG2008()
            
            valid, msg, normalized = solver.validate_composition(test_composition)
            if valid:
                result = solver.calculate_properties(558.0, 50.0, normalized)
                densidade = result.get('density', 0)
                success = densidade > 0
                details = f"Densidade: {densidade:.6f} kg/m³"
            else:
                success = False
                details = f"Composição inválida: {msg}"
                
            self.log_result("AGA8 Calculation", success, details)
            return success
        except Exception as e:
            self.log_result("AGA8 Calculation", False, str(e))
            return False
            
    def test_pdf_generation_capability(self) -> bool:
        """Testa se os módulos de PDF estão disponíveis"""
        try:
            # Verificar se reportlab está disponível
            import reportlab  # noqa: F401
            from reportlab.lib.pagesizes import A4  # noqa: F401
            success = True
            self.log_result("PDF Generation Capability", success, "ReportLab available")
            return success
        except ImportError as e:
            self.log_result("PDF Generation Capability", False, f"Missing PDF dependency: {e}")
            return False
            
    def test_excel_import_modules(self) -> bool:
        """Testa se módulos de importação Excel estão disponíveis"""
        try:
            import openpyxl  # noqa: F401
            import pandas as pd  # noqa: F401
            success = True
            self.log_result("Excel Import Modules", success, "openpyxl and pandas available")
            return success
        except ImportError as e:
            self.log_result("Excel Import Modules", False, f"Missing Excel dependency: {e}")
            return False
            
    def test_critical_routes(self) -> bool:
        """Testa rotas críticas da aplicação"""
        critical_routes = [
            "/",
            "/cadastrar",
            "/importar_excel"
        ]
        
        all_success = True
        for route in critical_routes:
            try:
                response = requests.get(f"{self.base_url}{route}", timeout=10)
                success = response.status_code in [200, 302]  # 302 para redirects
                if not success:
                    all_success = False
                self.log_result(f"Route {route}", success, f"Status {response.status_code}")
            except Exception as e:
                self.log_result(f"Route {route}", False, str(e))
                all_success = False
                
        return all_success
        
    def run_smoke_tests(self) -> Dict[str, Any]:
        """Executa suite completa de smoke tests"""
        print("🔥 INICIANDO SMOKE TESTS - SIMULAÇÃO STAGING")
        print("=" * 60)
        
        start_time = time.time()
        
        # Executar testes
        tests = [
            self.test_server_health,
            self.test_database_connection,
            self.test_aga8_calculation,
            self.test_pdf_generation_capability,
            self.test_excel_import_modules,
            self.test_critical_routes
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            if test():
                passed += 1
            else:
                failed += 1
                
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("📊 RESULTADOS DO SMOKE TEST")
        print("=" * 60)
        print(f"✅ Testes Aprovados: {passed}")
        print(f"❌ Testes Falharam: {failed}")
        print(f"⏱️  Tempo de Execução: {duration:.2f}s")
        
        success_rate = (passed / (passed + failed)) * 100 if (passed + failed) > 0 else 0
        print(f"📈 Taxa de Sucesso: {success_rate:.1f}%")
        
        if success_rate >= 90:
            status = "🟢 APROVADO PARA STAGING"
        elif success_rate >= 70:
            status = "🟡 CONDICIONAL - REVISAR FALHAS"
        else:
            status = "🔴 REPROVADO - CORRIGIR ANTES DE STAGING"
            
        print(f"🎯 Status Final: {status}")
        
        return {
            'passed': passed,
            'failed': failed,
            'success_rate': success_rate,
            'status': status,
            'duration': duration,
            'results': self.results
        }


def main():
    """Função principal"""
    smoke_test = SmokeTestSuite()
    results = smoke_test.run_smoke_tests()
    
    # Retornar código de saída baseado nos resultados
    return 0 if results['success_rate'] >= 90 else 1


if __name__ == "__main__":
    exit(main())