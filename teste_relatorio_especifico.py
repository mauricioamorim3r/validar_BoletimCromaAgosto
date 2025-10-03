#!/usr/bin/env python3
"""
Teste específico para reproduzir o erro de relatório ID 23
Sistema de Validação de Boletins - SGM
"""

import requests
import traceback

def testar_relatorio_local():
    """Testa o relatório localmente"""
    try:
        print("🧪 Testando Relatório Local")
        print("=" * 50)
        
        # Testar primeiro com servidor local
        local_url = "http://127.0.0.1:8888/relatorio/23"
        
        try:
            response = requests.get(local_url, timeout=10)
            if response.status_code == 200:
                print("✅ Relatório local funcionando - Status 200")
                if "Internal Server Error" in response.text:
                    print("❌ Mas contém erro interno na resposta")
                else:
                    print("✅ Resposta HTML válida")
            else:
                print(f"❌ Erro local - Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("⚠️  Servidor local não está rodando")
        except Exception as e:
            print(f"❌ Erro ao testar local: {e}")
            
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        traceback.print_exc()

def testar_relatorio_producao():
    """Testa o relatório em produção"""
    try:
        print("\n🌐 Testando Relatório em Produção")
        print("=" * 50)
        
        prod_url = "https://validar-boletimcromatografia.onrender.com/relatorio/23"
        
        try:
            response = requests.get(prod_url, timeout=30)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 500:
                print("❌ Internal Server Error confirmado em produção")
                print("Possíveis causas:")
                print("  • Diferenças no banco de dados")
                print("  • Problema de conexão com banco")
                print("  • Erro nas funções de cálculo CEP")
                print("  • Problema nas validações ANP")
            elif response.status_code == 200:
                print("✅ Relatório produção funcionando")
            else:
                print(f"❌ Erro inesperado: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout - servidor pode estar sobrecarregado")
        except Exception as e:
            print(f"❌ Erro ao testar produção: {e}")
            
    except Exception as e:
        print(f"❌ Erro durante teste produção: {e}")

def main():
    """Função principal"""
    print("🔍 Diagnóstico do Erro de Relatório")
    print("Testando tanto local quanto produção")
    print("=" * 60)
    
    testar_relatorio_local()
    testar_relatorio_producao()
    
    print("\n" + "=" * 60)
    print("💡 Próximos passos:")
    print("1. Se local funciona e produção não:")
    print("   • Verificar diferenças no banco de dados")
    print("   • Verificar logs do Render")
    print("   • Fazer deploy das correções")
    print("2. Se ambos falham:")
    print("   • Investigar função calculate_cep_limits")
    print("   • Verificar validacao_prazos_anp")

if __name__ == "__main__":
    main()