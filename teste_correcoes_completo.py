#!/usr/bin/env python3
"""
Teste completo das correções do relatório
Sistema de Validação de Boletins - SGM
"""

import requests
import time
import sys

def testar_relatorio_completo():
    """Testa a rota de relatório completa"""
    url = "https://validar-boletimcromatografia.onrender.com/relatorio/23"
    
    try:
        print("🔄 Testando relatório completo...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            if "Internal Server Error" in response.text:
                print("❌ Relatório completo ainda com erro 500")
                return False
            else:
                print("✅ Relatório completo funcionando!")
                return True
        else:
            print(f"❌ Relatório completo - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar relatório completo: {e}")
        return False

def testar_relatorio_diagnostico():
    """Testa a rota de relatório de diagnóstico"""
    url = "https://validar-boletimcromatografia.onrender.com/relatorio/23/simple"
    
    try:
        print("🔄 Testando relatório de diagnóstico...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            if "Relatório Simplificado" in response.text:
                print("✅ Relatório de diagnóstico funcionando!")
                return True
            else:
                print("❌ Relatório de diagnóstico - resposta inesperada")
                return False
        else:
            print(f"❌ Relatório de diagnóstico - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar relatório de diagnóstico: {e}")
        return False

def aguardar_deploy_e_testar():
    """Aguarda deploy e testa ambas as rotas"""
    print("🚀 Aguardando Deploy e Testando Correções")
    print("=" * 60)
    print("⏰ Aguardando 60 segundos para o deploy ser aplicado...")
    
    time.sleep(60)
    
    for tentativa in range(1, 6):
        print(f"\n🔄 Tentativa {tentativa}/5:")
        print("-" * 30)
        
        # Testar relatório de diagnóstico primeiro
        diagnostico_ok = testar_relatorio_diagnostico()
        
        # Testar relatório completo
        completo_ok = testar_relatorio_completo()
        
        if completo_ok:
            print("🎉 SUCESSO TOTAL! Ambos relatórios funcionando!")
            print("\n📋 Status Final:")
            print("  ✅ Relatório completo: OK")
            print("  ✅ Relatório diagnóstico: OK")
            print("  ✅ Erro corrigido completamente!")
            return True
        elif diagnostico_ok:
            print("⚠️  Diagnóstico OK, mas relatório completo ainda com erro")
            print("   → Isso indica que as correções básicas funcionaram")
            print("   → Problema pode estar nas funções de cálculo CEP")
        else:
            print("❌ Ambos com erro - deploy pode ainda estar em andamento")
        
        if tentativa < 5:
            print(f"   Aguardando mais 30s antes da próxima tentativa...")
            time.sleep(30)
    
    print("\n⚠️  Deploy pode ainda estar em andamento ou há problemas adicionais")
    print("📋 Recomendações:")
    print("  1. Aguardar mais alguns minutos")
    print("  2. Verificar logs do Render")
    print("  3. Testar rota de diagnóstico: /relatorio/23/simple")
    
    return False

def teste_rapido():
    """Teste rápido sem aguardar"""
    print("🧪 Teste Rápido das Correções")
    print("=" * 50)
    
    diagnostico_ok = testar_relatorio_diagnostico()
    completo_ok = testar_relatorio_completo()
    
    print("\n📊 Resultados:")
    print(f"  Diagnóstico: {'✅ OK' if diagnostico_ok else '❌ Erro'}")
    print(f"  Completo: {'✅ OK' if completo_ok else '❌ Erro'}")
    
    if completo_ok:
        print("\n🎉 Problema resolvido completamente!")
    elif diagnostico_ok:
        print("\n⚠️  Progresso: Correções básicas funcionaram")
        print("   Problema específico no cálculo CEP ou validação ANP")
    else:
        print("\n❌ Deploy ainda não aplicado ou problema persiste")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rapido":
        teste_rapido()
    else:
        aguardar_deploy_e_testar()