#!/usr/bin/env python3
"""
Teste para verificar remoção do texto órfão próximo ao botão Salvar Boletim
Sistema de Validação de Boletins - SGM
"""

import os
import sys

def verificar_remocao_texto():
    """Verifica se o texto órfão foi removido da tela de cadastrar"""
    print("🧪 Testando Remoção de Texto Órfão")
    print("=" * 50)
    
    template_file = "templates/cadastrar.html"
    
    if not os.path.exists(template_file):
        print("❌ Arquivo cadastrar.html não encontrado")
        return False
    
    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se o texto órfão foi removido
    textos_orfaos = [
        '<th class="text-center">Limite Inferior</th>',
        '<th class="text-center">Limite Superior</th>',
    ]
    
    print("🔍 Verificando remoção de textos órfãos:")
    for texto in textos_orfaos:
        if texto in content:
            print(f"❌ Texto órfão ainda presente: {texto}")
            return False
        else:
            print(f"✅ Texto órfão removido: {texto}")
    
    # Verificar se o botão Salvar Boletim ainda existe
    botao_salvar = '<i class="bi bi-check-circle"></i> Salvar Boletim'
    if botao_salvar in content:
        print("✅ Botão 'Salvar Boletim' mantido corretamente")
    else:
        print("❌ Botão 'Salvar Boletim' não encontrado")
        return False
    
    # Verificar se a estrutura HTML está íntegra
    estruturas_importantes = [
        '</form>',
        '<script>',
        'document.addEventListener',
    ]
    
    print("\n🔍 Verificando integridade da estrutura HTML:")
    for estrutura in estruturas_importantes:
        if estrutura in content:
            print(f"✅ Estrutura mantida: {estrutura}")
        else:
            print(f"❌ Estrutura perdida: {estrutura}")
            return False
    
    return True

def main():
    """Função principal"""
    try:
        sucesso = verificar_remocao_texto()
        
        print("\n" + "=" * 50)
        if sucesso:
            print("🎉 SUCESSO: Texto órfão removido com sucesso!")
            print("📋 O que foi feito:")
            print("   • Removidos textos 'Limite Inferior' e 'Limite Superior' órfãos")
            print("   • Mantido o botão 'Salvar Boletim' intacto")
            print("   • Preservada a estrutura HTML e JavaScript")
        else:
            print("❌ ERRO: Algumas verificações falharam")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()