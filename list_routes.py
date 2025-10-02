#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lista todas as rotas disponíveis na aplicação
"""

import sys
import os

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def list_app_routes():
    """Lista todas as rotas da aplicação Flask"""
    print("=" * 70)
    print("ROTAS DISPONÍVEIS NA APLICAÇÃO")
    print("=" * 70)
    
    try:
        from app import app
        
        print(f"📦 Aplicação carregada: {app.name}")
        print(f"🌐 Host configurado: {app.config.get('HOST', 'N/A')}")
        print(f"🔌 Porta configurada: {app.config.get('PORT', 'N/A')}")
        print()
        
        routes = []
        for rule in app.url_map.iter_rules():
            methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            routes.append((rule.rule, methods, rule.endpoint))
        
        # Ordenar por rota
        routes.sort()
        
        print(f"📋 Total de rotas encontradas: {len(routes)}")
        print("-" * 70)
        print(f"{'ROTA':<40} {'MÉTODOS':<15} {'ENDPOINT'}")
        print("-" * 70)
        
        for route, methods, endpoint in routes:
            print(f"{route:<40} {methods:<15} {endpoint}")
        
        print("-" * 70)
        
        # Destacar rotas principais
        principais = [r for r in routes if r[0] in ['/', '/dashboard', '/boletins', '/cadastrar']]
        if principais:
            print("\n🔥 ROTAS PRINCIPAIS:")
            for route, methods, endpoint in principais:
                print(f"   ✅ {route} ({methods})")
        
        # Destacar APIs
        apis = [r for r in routes if '/api' in r[0]]
        if apis:
            print(f"\n🚀 APIs DISPONÍVEIS ({len(apis)}):")
            for route, methods, endpoint in apis:
                print(f"   🔗 {route} ({methods})")
        else:
            print("\n⚠️  Nenhuma API encontrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao listar rotas: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    list_app_routes()