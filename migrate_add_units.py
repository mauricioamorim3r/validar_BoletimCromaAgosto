#!/usr/bin/env python3
"""
Script de Migração - Adicionar Campos de Unidades e Metodologia
Sistema de Validação de Boletins Cromatográficos - BRAVA Energia

Adiciona os seguintes campos:
- pressao_unit: Unidade da pressão (atm, kpa, pa, bar, psi)
- temperatura_unit: Unidade da temperatura (celsius, kelvin)
- metodologia_aprovada: Boolean indicando se existe metodologia aprovada
"""

import sqlite3
import sys
import os

def get_db_connection():
    """Conecta ao banco de dados"""
    db_path = 'boletins.db'
    if not os.path.exists(db_path):
        print(f"Erro: Banco de dados {db_path} não encontrado!")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def check_column_exists(conn, table_name, column_name):
    """Verifica se uma coluna existe na tabela"""
    try:
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]
        return column_name in columns
    except Exception as e:
        print(f"Erro ao verificar coluna {column_name}: {e}")
        return False

def add_new_columns(conn):
    """Adiciona os novos campos na tabela boletins"""
    campos_novos = [
        {
            'nome': 'pressao_unit',
            'tipo': 'TEXT DEFAULT "atm"',
            'descricao': 'Unidade da pressão (atm, kpa, pa, bar, psi)'
        },
        {
            'nome': 'temperatura_unit', 
            'tipo': 'TEXT DEFAULT "celsius"',
            'descricao': 'Unidade da temperatura (celsius, kelvin)'
        },
        {
            'nome': 'metodologia_aprovada',
            'tipo': 'INTEGER DEFAULT 0',
            'descricao': 'Se existe metodologia de validação aprovada (0=não, 1=sim)'
        }
    ]
    
    campos_adicionados = []
    campos_existentes = []
    
    for campo in campos_novos:
        if not check_column_exists(conn, 'boletins', campo['nome']):
            try:
                sql = f"ALTER TABLE boletins ADD COLUMN {campo['nome']} {campo['tipo']}"
                conn.execute(sql)
                campos_adicionados.append(f"✅ {campo['nome']}: {campo['descricao']}")
            except Exception as e:
                print(f"❌ Erro ao adicionar campo {campo['nome']}: {e}")
                return False, campos_adicionados, campos_existentes
        else:
            campos_existentes.append(f"⚠️ {campo['nome']}: já existe")
    
    return True, campos_adicionados, campos_existentes

def update_existing_records(conn):
    """Atualiza registros existentes com valores padrão"""
    try:
        # Contar registros existentes
        cursor = conn.execute("SELECT COUNT(*) FROM boletins")
        total_registros = cursor.fetchone()[0]
        
        if total_registros == 0:
            return True, "Nenhum registro existente para atualizar"
        
        # Atualizar campos que podem estar NULL
        updates = [
            ("pressao_unit", "atm", "pressao_unit IS NULL"),
            ("temperatura_unit", "celsius", "temperatura_unit IS NULL"),
            ("metodologia_aprovada", "0", "metodologia_aprovada IS NULL")
        ]
        
        registros_atualizados = 0
        
        for campo, valor_padrao, condicao in updates:
            cursor = conn.execute(f"UPDATE boletins SET {campo} = ? WHERE {condicao}", (valor_padrao,))
            registros_atualizados += cursor.rowcount
        
        return True, f"✅ {registros_atualizados} campos atualizados em {total_registros} registros"
        
    except Exception as e:
        return False, f"❌ Erro ao atualizar registros: {e}"

def verificar_estrutura_final(conn):
    """Verifica a estrutura final da tabela"""
    try:
        cursor = conn.execute("PRAGMA table_info(boletins)")
        colunas = cursor.fetchall()
        
        campos_verificar = ['pressao_unit', 'temperatura_unit', 'metodologia_aprovada']
        campos_encontrados = []
        
        for coluna in colunas:
            nome_coluna = coluna[1]
            if nome_coluna in campos_verificar:
                campos_encontrados.append(f"✅ {nome_coluna} ({coluna[2]})")
        
        return campos_encontrados
        
    except Exception as e:
        return [f"❌ Erro na verificação: {e}"]

def main():
    """Função principal da migração"""
    print("🚀 MIGRAÇÃO - Adicionando Campos de Unidades e Metodologia")
    print("=" * 65)
    
    # Conectar ao banco
    conn = get_db_connection()
    if not conn:
        sys.exit(1)
    
    try:
        # Iniciar transação
        conn.execute("BEGIN TRANSACTION")
        
        # Adicionar novos campos
        print("\n📊 Adicionando novos campos...")
        sucesso, campos_adicionados, campos_existentes = add_new_columns(conn)
        
        if not sucesso:
            conn.rollback()
            sys.exit(1)
        
        # Mostrar resultados
        if campos_adicionados:
            print("\n🆕 Campos adicionados:")
            for campo in campos_adicionados:
                print(f"   {campo}")
        
        if campos_existentes:
            print("\n📋 Campos já existentes:")
            for campo in campos_existentes:
                print(f"   {campo}")
        
        # Atualizar registros existentes
        print("\n🔄 Atualizando registros existentes...")
        sucesso_update, mensagem_update = update_existing_records(conn)
        print(f"   {mensagem_update}")
        
        if not sucesso_update:
            conn.rollback()
            sys.exit(1)
        
        # Confirmar transação
        conn.commit()
        
        # Verificação final
        print("\n🔍 Verificação final da estrutura:")
        campos_finais = verificar_estrutura_final(conn)
        for campo in campos_finais:
            print(f"   {campo}")
        
        print("\n" + "=" * 65)
        print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("\n📋 Novos recursos disponíveis:")
        print("   • Seletor de unidades de pressão (atm, kPa, Pa, bar, psi)")
        print("   • Seletor de unidades de temperatura (Celsius, Kelvin)")
        print("   • Campo para metodologia de validação aprovada")
        print("   • Conversão automática entre unidades")
        print("   • Validação de prazos ANP com duas condições")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ ERRO NA MIGRAÇÃO: {e}")
        sys.exit(1)
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()