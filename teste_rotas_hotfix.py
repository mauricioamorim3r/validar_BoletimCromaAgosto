#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das rotas de hotfix em produção
Testa se as diferentes rotas funcionam após o deploy
"""

import requests
import time

def testar_rotas_producao():
    """Testa as diferentes rotas em produção"""
    base_url = "https://validar-boletimcromatografia.onrender.com"
    
    # IDs de boletins para testar
    boletim_ids = [23, 22, 21, 20]
    
    print("🔍 TESTANDO ROTAS DE HOTFIX EM PRODUÇÃO")
    print("=" * 50)
    
    for boletim_id in boletim_ids:
        print(f"\n📋 TESTANDO BOLETIM ID: {boletim_id}")
        print("-" * 30)
        
        # 1. Testar rota normal (que está falhando)
        print("1️⃣ Testando rota normal:")
        try:
            response = requests.get(f"{base_url}/relatorio/{boletim_id}", timeout=30)
            if response.status_code == 200:
                print("   ✅ Rota normal FUNCIONANDO")
            else:
                print(f"   ❌ Rota normal FALHOU - Status: {response.status_code}")
        except Exception as e:
            print(f"   💥 Rota normal ERRO: {str(e)}")
        
        # 2. Testar rota de diagnóstico simples
        print("2️⃣ Testando rota de diagnóstico:")
        try:
            response = requests.get(f"{base_url}/relatorio/{boletim_id}/simple", timeout=30)
            if response.status_code == 200:
                print("   ✅ Rota diagnóstico FUNCIONANDO")
            else:
                print(f"   ❌ Rota diagnóstico FALHOU - Status: {response.status_code}")
        except Exception as e:
            print(f"   💥 Rota diagnóstico ERRO: {str(e)}")
        
        # 3. Testar rota de hotfix (sem CEP)
        print("3️⃣ Testando rota hotfix:")
        try:
            response = requests.get(f"{base_url}/relatorio/{boletim_id}/hotfix", timeout=30)
            if response.status_code == 200:
                print("   ✅ Rota hotfix FUNCIONANDO")
                print("   🎯 SUCESSO! Problema está nos cálculos CEP")
            else:
                print(f"   ❌ Rota hotfix FALHOU - Status: {response.status_code}")
        except Exception as e:
            print(f"   💥 Rota hotfix ERRO: {str(e)}")
        
        time.sleep(2)  # Pausa entre testes
        
        # Se encontramos uma rota que funciona, podemos parar
        if boletim_id == 23:  # Apenas para o primeiro teste
            try:
                hotfix_response = requests.get(f"{base_url}/relatorio/{boletim_id}/hotfix", timeout=30)
                if hotfix_response.status_code == 200:
                    print(f"\n🎉 HOTFIX FUNCIONOU!")
                    print("📊 DIAGNÓSTICO:")
                    print("   - Rota normal: FALHA (erro 500)")
                    print("   - Rota hotfix: SUCESSO")
                    print("   - CONCLUSÃO: Problema está nos cálculos CEP")
                    return True
            except:
                pass
    
    print(f"\n📈 RESUMO DOS TESTES:")
    print("   - Se hotfix funcionar: problema nos cálculos CEP")  
    print("   - Se hotfix falhar: problema mais profundo no sistema")
    
    return False

if __name__ == "__main__":
    testar_rotas_producao()