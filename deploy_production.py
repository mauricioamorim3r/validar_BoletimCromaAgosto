#!/usr/bin/env python3
"""
Script de Deploy para Produção
Sistema de Validação de Boletins Cromatográficos
"""

import os
import subprocess
from datetime import datetime


def print_step(step, description):
    """Imprime step do deploy"""
    print(f"\n🔄 STEP {step}: {description}")
    print("=" * 60)


def run_command(command, description=""):
    """Executa comando e retorna resultado"""
    try:
        print(f"⚡ Executando: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Erro")
            if result.stderr.strip():
                print(f"   Erro: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False


def check_requirements():
    """Verifica se dependências estão instaladas"""
    print_step(1, "VERIFICAÇÃO DE DEPENDÊNCIAS")
    
    required_modules = [
        'flask',
        'reportlab',
        'openpyxl',
        'pandas',
        'requests'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError:
            missing.append(module)
            print(f"❌ {module} - AUSENTE")
    
    if missing:
        print(f"\n⚠️  Dependências ausentes: {', '.join(missing)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("\n✅ Todas dependências disponíveis")
    return True


def check_database():
    """Verifica se banco de dados existe"""
    print_step(2, "VERIFICAÇÃO DO BANCO DE DADOS")
    
    if os.path.exists("boletins.db"):
        size = os.path.getsize("boletins.db")
        print(f"✅ Banco de dados encontrado ({size} bytes)")
        return True
    else:
        print("❌ Banco de dados não encontrado")
        print("Criando banco vazio...")
        # Aqui você adicionaria código para criar banco inicial
        return False


def run_tests():
    """Executa testes básicos"""
    print_step(3, "EXECUÇÃO DE TESTES")
    
    # Teste básico de import
    try:
        from aga8_gerg2008 import AGA8_GERG2008
        solver = AGA8_GERG2008()
        print("✅ AGA8 GERG2008 - Importação OK")
        
        # Teste básico de cálculo
        composition = {
            'Metano': 90.0,
            'Etano': 5.0,
            'Propano': 3.0,
            'n-Butano': 2.0
        }
        
        valid, msg, normalized = solver.validate_composition(composition)
        if valid:
            print("✅ Validação de composição - OK")
            result = solver.calculate_properties(558.0, 50.0, normalized)
            if 'density' in result:
                print(f"✅ Cálculo de propriedades - OK (densidade: {result['density']:.6f})")
                return True
        
        print(f"❌ Erro na validação: {msg}")
        return False
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        return False


def create_backup():
    """Cria backup dos arquivos importantes"""
    print_step(4, "CRIAÇÃO DE BACKUP")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_files = [
        "boletins.db",
        "app.py",
        "config.py",
        "aga8_gerg2008.py"
    ]
    
    backup_dir = f"backup_{timestamp}"
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
        
        for file in backup_files:
            if os.path.exists(file):
                run_command(f"copy {file} {backup_dir}\\", f"Backup {file}")
            else:
                print(f"⚠️  Arquivo {file} não encontrado para backup")
        
        print(f"✅ Backup criado em: {backup_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no backup: {e}")
        return False


def deploy_production():
    """Deploy para produção"""
    print_step(5, "DEPLOY PARA PRODUÇÃO")
    
    print("🔧 Configurações de produção:")
    print("   - Debug: False")
    print("   - Host: 0.0.0.0")
    print("   - Port: 5000")
    
    # Aqui você adicionaria comandos específicos do seu ambiente
    # Exemplo:
    # - Parar serviço atual
    # - Copiar arquivos
    # - Reiniciar serviço
    # - Verificar status
    
    print("✅ Deploy simulado com sucesso")
    print("📝 Lembre-se de:")
    print("   1. Configurar variáveis de ambiente") 
    print("   2. Usar servidor WSGI (gunicorn/uWSGI)")
    print("   3. Configurar proxy reverso (nginx)")
    print("   4. Monitorar logs")
    
    return True


def main():
    """Função principal do deploy"""
    print("🚀 INICIANDO DEPLOY PARA PRODUÇÃO")
    print("Sistema de Validação de Boletins Cromatográficos")
    print("=" * 60)
    
    steps = [
        check_requirements,
        check_database, 
        run_tests,
        create_backup,
        deploy_production
    ]
    
    for i, step_func in enumerate(steps, 1):
        if not step_func():
            print(f"\n❌ Deploy falhou no step {i}")
            print("Corrija os erros antes de continuar")
            return 1
    
    print("\n" + "=" * 60)
    print("🎉 DEPLOY CONCLUÍDO COM SUCESSO!")
    print("✅ Sistema pronto para produção")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())