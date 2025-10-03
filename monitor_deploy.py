#!/usr/bin/env python3
"""
Monitor do deploy e teste do relatório corrigido
Sistema de Validação de Boletins - SGM
"""

import requests
import time
import sys

def testar_relatorio():
    """Testa se o relatório está funcionando"""
    url = "https://validar-boletimcromatografia.onrender.com/relatorio/23"
    
    try:
        response = requests.get(url, timeout=30)
        return response.status_code == 200 and "Internal Server Error" not in response.text
    except:
        return False

def monitorar_deploy():
    """Monitora o deploy e testa quando estiver pronto"""
    print("🚀 Monitorando Deploy no Render")
    print("=" * 50)
    print("Aguardando deploy automático...")
    
    # Dar tempo para o deploy começar
    time.sleep(30)
    
    for tentativa in range(1, 11):
        print(f"\n🔄 Tentativa {tentativa}/10 - Testando relatório...")
        
        if testar_relatorio():
            print("✅ SUCESSO! Relatório funcionando corretamente!")
            print("🎉 Deploy concluído e erro corrigido!")
            print("\n📋 Verificações realizadas:")
            print("  • Status 200 OK")
            print("  • Sem 'Internal Server Error' na resposta")
            print("  • Relatório carregando normalmente")
            return True
        else:
            print(f"❌ Ainda com erro... aguardando mais {30}s")
            time.sleep(30)
    
    print("\n⚠️  Deploy pode ainda estar em andamento.")
    print("Verifique manualmente em alguns minutos.")
    return False

def teste_rapido():
    """Teste rápido sem aguardar"""
    print("🧪 Teste Rápido do Relatório")
    print("=" * 50)
    
    if testar_relatorio():
        print("✅ Relatório funcionando!")
    else:
        print("❌ Relatório ainda com erro")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rapido":
        teste_rapido()
    else:
        monitorar_deploy()