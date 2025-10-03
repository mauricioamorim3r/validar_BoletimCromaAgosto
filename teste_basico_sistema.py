#!/usr/bin/env python3
"""
Teste de status básico do sistema
Sistema de Validação de Boletins - SGM
"""

import requests

def testar_sistema_basico():
    """Testa endpoints básicos do sistema"""
    
    base_url = "https://validar-boletimcromatografia.onrender.com"
    
    testes = [
        ("Dashboard", f"{base_url}/dashboard"),
        ("Listar Boletins", f"{base_url}/listar_boletins"),
        ("Home", f"{base_url}/"),
    ]
    
    print("🔍 Testando Sistema Básico")
    print("=" * 50)
    
    for nome, url in testes:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                print(f"✅ {nome}: OK")
            else:
                print(f"❌ {nome}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {nome}: Erro - {e}")
    
    print("\n🎯 Teste Específico - Relatório")
    print("-" * 30)
    
    # Testar relatório problemático
    try:
        response = requests.get(f"{base_url}/relatorio/23", timeout=15)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 500:
            print("❌ Erro 500 confirmado - problema na aplicação")
        elif response.status_code == 200:
            if "Internal Server Error" in response.text:
                print("❌ HTML de erro - problema interno")
            else:
                print("✅ Relatório funcionando!")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    testar_sistema_basico()