#!/usr/bin/env python3
"""
Teste para verificar as unidades simplificadas (apenas símbolos)
Sistema de Validação de Boletins - SGM
"""

import os
import sys

def verificar_arquivo_js():
    """Verifica se o arquivo JavaScript foi atualizado corretamente"""
    print("🧪 Testando Unidades Simplificadas")
    print("=" * 50)
    
    js_file = "static/js/unit-converter.js"
    
    if not os.path.exists(js_file):
        print("❌ Arquivo unit-converter.js não encontrado")
        return False
    
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se as unidades estão simplificadas
    verificacoes = [
        ("Temperatura Celsius simplificada", "celsius: { name: '°C', symbol: '°C'"),
        ("Temperatura Kelvin simplificada", "kelvin: { name: 'K', symbol: 'K'"),
        ("Pressão atm simplificada", "atm: { name: 'atm', symbol: 'atm'"),
        ("Pressão kPa simplificada", "kpa: { name: 'kPa', symbol: 'kPa'"),
        ("Pressão Pa simplificada", "pa: { name: 'Pa', symbol: 'Pa'"),
        ("Pressão bar simplificada", "bar: { name: 'bar', symbol: 'bar'"),
        ("Pressão psi simplificada", "psi: { name: 'psi', symbol: 'psi'"),
        ("Opções do seletor simplificadas", "option.textContent = config.symbol;"),
    ]
    
    for descricao, codigo in verificacoes:
        if codigo in content:
            print(f"✅ {descricao}")
        else:
            print(f"❌ {descricao}")
            return False
    
    # Verificar se os nomes longos foram removidos
    nomes_longos = [
        "Celsius",
        "Kelvin", 
        "Atmosfera",
        "Quilopascal", 
        "Pascal",
        "Bar",
        "PSI"
    ]
    
    print("\n🔍 Verificando remoção de nomes longos:")
    for nome in nomes_longos:
        if f"name: '{nome}'" in content:
            print(f"❌ Nome longo ainda presente: {nome}")
            return False
        else:
            print(f"✅ Nome longo removido: {nome}")
    
    return True

def main():
    """Função principal"""
    try:
        sucesso = verificar_arquivo_js()
        
        print("\n" + "=" * 50)
        if sucesso:
            print("🎉 SUCESSO: Unidades simplificadas corretamente!")
            print("📋 Agora as unidades mostram apenas símbolos:")
            print("   • Temperatura: °C, K")
            print("   • Pressão: atm, kPa, Pa, bar, psi")
        else:
            print("❌ ERRO: Algumas verificações falharam")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()