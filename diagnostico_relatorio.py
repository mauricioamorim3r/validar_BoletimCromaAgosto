#!/usr/bin/env python3
"""
Teste para verificar se a tabela historico_componentes existe e diagnóstico do erro
"""

import sqlite3
import traceback

def verificar_banco():
    try:
        db = sqlite3.connect('boletins.db')
        db.row_factory = sqlite3.Row
        
        # Verificar se a tabela historico_componentes existe
        cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='historico_componentes'")
        result = cursor.fetchone()
        if result:
            print('✅ Tabela historico_componentes existe')
        else:
            print('❌ Tabela historico_componentes NÃO existe')
            
        # Verificar se existe algum boletim com ID 23
        cursor = db.execute('SELECT * FROM boletins WHERE id = 23')
        boletim = cursor.fetchone()
        if boletim:
            print('✅ Boletim ID 23 existe')
            print(f'   Número: {boletim["numero_boletim"]}')
        else:
            print('❌ Boletim ID 23 NÃO existe')
            
        # Listar primeiros 5 boletins disponíveis
        cursor = db.execute('SELECT id, numero_boletim FROM boletins ORDER BY id LIMIT 5')
        boletins = cursor.fetchall()
        print(f'\n📋 Boletins disponíveis:')
        for b in boletins:
            print(f'   ID: {b["id"]} - Número: {b["numero_boletim"]}')
            
        db.close()
        return True
        
    except Exception as e:
        print(f'❌ Erro ao verificar banco: {e}')
        traceback.print_exc()
        return False

def testar_funcao_historico():
    """Testa se a função get_historico_componente funciona"""
    try:
        from app import get_historico_componente
        resultado = get_historico_componente('Metano, CH₄')
        print(f'✅ Função get_historico_componente funciona - retornou {len(resultado)} itens')
        return True
    except Exception as e:
        print(f'❌ Erro na função get_historico_componente: {e}')
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Diagnóstico do Erro de Relatório")
    print("=" * 50)
    
    banco_ok = verificar_banco()
    print()
    funcao_ok = testar_funcao_historico()
    
    print("\n" + "=" * 50)
    if banco_ok and funcao_ok:
        print("🎉 Diagnóstico concluído - sistema aparenta estar funcionando")
    else:
        print("❌ Problemas identificados - necessária correção")