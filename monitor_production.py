#!/usr/bin/env python3
"""
Script de Monitoramento Pós-Deploy
Sistema de Validação de Boletins Cromatográficos
"""

import requests
import time
import logging
from datetime import datetime
from typing import Dict, Any


class ProductionMonitor:
    def __init__(self, base_url: str = "http://127.0.0.1:3000"):
        self.base_url = base_url
        self.setup_logging()
        
    def setup_logging(self):
        """Configura logging para monitoramento"""
        logging.basicConfig(
            filename=f'monitoring_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def health_check(self) -> Dict[str, Any]:
        """Executa verificação de saúde do sistema"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/", timeout=30)
            response_time = time.time() - start_time
            
            status = {
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code,
                'response_time': response_time,
                'healthy': response.status_code == 200 and response_time < 10,
                'url': self.base_url
            }
            
            if status['healthy']:
                self.logger.info(f"✅ Health check OK - Response time: {response_time:.2f}s")
                print(f"✅ {datetime.now().strftime('%H:%M:%S')} - Sistema saudável (Response: {response_time:.2f}s)")
            else:
                self.logger.warning(f"⚠️ Health check WARN - Status: {response.status_code}, Time: {response_time:.2f}s")
                print(f"⚠️ {datetime.now().strftime('%H:%M:%S')} - Sistema com problemas")
                
            return status
            
        except Exception as e:
            error_status = {
                'timestamp': datetime.now().isoformat(),
                'healthy': False,
                'error': str(e),
                'url': self.base_url
            }
            
            self.logger.error(f"❌ Health check FAILED - Error: {e}")
            print(f"❌ {datetime.now().strftime('%H:%M:%S')} - Sistema indisponível: {e}")
            return error_status
            
    def test_aga8_functionality(self) -> bool:
        """Testa funcionalidade AGA8"""
        try:
            from aga8_gerg2008 import AGA8_GERG2008
            solver = AGA8_GERG2008()
            
            # Composição teste
            composition = {
                'Metano': 90.0,
                'Etano': 5.0,
                'Propano': 3.0,
                'n-Butano': 2.0
            }
            
            valid, msg, normalized = solver.validate_composition(composition)
            if valid:
                result = solver.calculate_properties(558.0, 50.0, normalized)
                density = result.get('density', 0)
                
                if density > 0:
                    self.logger.info(f"✅ AGA8 funcionando - Densidade: {density:.6f}")
                    print(f"✅ AGA8 OK - Densidade: {density:.6f} kg/m³")
                    return True
                    
            self.logger.error(f"❌ AGA8 problema - {msg}")
            print(f"❌ AGA8 com problemas: {msg}")
            return False
            
        except Exception as e:
            self.logger.error(f"❌ AGA8 erro crítico - {e}")
            print(f"❌ AGA8 erro crítico: {e}")
            return False
    
    def monitor_continuously(self, interval: int = 300):
        """Monitora sistema continuamente (default: 5 minutos)"""
        print(f"🔍 Iniciando monitoramento contínuo (intervalo: {interval}s)")
        print("Pressione Ctrl+C para parar")
        
        try:
            while True:
                health = self.health_check()
                aga8_ok = self.test_aga8_functionality()
                
                if not health.get('healthy', False) or not aga8_ok:
                    print("🚨 ALERTA: Sistema com problemas detectados!")
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n⏹️ Monitoramento interrompido pelo usuário")
            self.logger.info("Monitoramento interrompido")


def main():
    """Função principal"""
    monitor = ProductionMonitor()
    
    print("🔍 MONITORAMENTO PÓS-DEPLOY")
    print("=" * 50)
    
    # Teste inicial
    print("\n1. Verificação inicial de saúde:")
    health = monitor.health_check()
    
    print("\n2. Teste de funcionalidade AGA8:")
    aga8_ok = monitor.test_aga8_functionality()
    
    print("\n3. Resumo do status:")
    if health.get('healthy', False) and aga8_ok:
        print("✅ Sistema totalmente operacional")
        status_code = 0
    else:
        print("⚠️ Sistema com problemas - verificar logs")
        status_code = 1
    
    print("\n4. Opções de monitoramento:")
    print("   - Logs salvos em: monitoring_<data>.log")
    print("   - Para monitoramento contínuo: python monitor_production.py --continuous")
    
    return status_code


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        monitor = ProductionMonitor()
        monitor.monitor_continuously()
    else:
        exit(main())