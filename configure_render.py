#!/usr/bin/env python3
"""
Script para configurar e verificar deploy no Render
Sistema de Validação de Boletins Cromatográficos
"""
import json
import subprocess
import sys
import os
from datetime import datetime


def print_header():
    """Imprime cabeçalho do script"""
    print("=" * 60)
    print("🚀 RENDER DEPLOY - CONFIGURAÇÃO AUTOMÁTICA")
    print("   Sistema de Validação de Boletins Cromatográficos")
    print("=" * 60)
    print()


def check_files():
    """Verifica se todos os arquivos necessários estão presentes"""
    print("📋 VERIFICANDO ARQUIVOS NECESSÁRIOS...")
    
    required_files = [
        'app.py',
        'requirements.txt', 
        'render.yaml',
        'runtime.txt',
        'gunicorn.conf.py',
        'boletins.db'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size:,} bytes)")
        else:
            missing_files.append(file)
            print(f"  ❌ {file} - AUSENTE")
    
    if missing_files:
        print(f"\n⚠️  ARQUIVOS AUSENTES: {', '.join(missing_files)}")
        return False
    
    print("\n✅ Todos os arquivos necessários presentes")
    return True


def validate_config():
    """Valida configurações nos arquivos"""
    print("\n🔧 VALIDANDO CONFIGURAÇÕES...")
    
    # Verificar render.yaml
    try:
        with open('render.yaml', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'gunicorn --config gunicorn.conf.py app:app' in content:
                print("  ✅ render.yaml - Start command OK")
            else:
                print("  ⚠️  render.yaml - Start command pode precisar de ajuste")
    except Exception as e:
        print(f"  ❌ Erro ao ler render.yaml: {e}")
    
    # Verificar requirements.txt
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            requirements = f.read()
            essential_deps = ['Flask', 'gunicorn', 'reportlab', 'pandas', 'openpyxl']
            missing_deps = []
            
            for dep in essential_deps:
                if dep.lower() not in requirements.lower():
                    missing_deps.append(dep)
            
            if not missing_deps:
                print("  ✅ requirements.txt - Dependências essenciais OK")
            else:
                print(f"  ⚠️  requirements.txt - Dependências ausentes: {missing_deps}")
    except Exception as e:
        print(f"  ❌ Erro ao ler requirements.txt: {e}")
    
    # Verificar runtime.txt
    try:
        with open('runtime.txt', 'r', encoding='utf-8') as f:
            runtime = f.read().strip()
            if runtime.startswith('python-3.11'):
                print(f"  ✅ runtime.txt - {runtime}")
            else:
                print(f"  ⚠️  runtime.txt - Versão: {runtime} (recomendado: python-3.11.x)")
    except Exception as e:
        print(f"  ❌ Erro ao ler runtime.txt: {e}")


def check_git_status():
    """Verifica status do git"""
    print("\n📡 VERIFICANDO STATUS DO GIT...")
    
    try:
        # Verificar se está em um repositório git
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            print("  ⚠️  Há arquivos não commitados:")
            for line in result.stdout.strip().split('\n')[:5]:  # Mostrar apenas os primeiros 5
                print(f"     {line}")
            print("\n  💡 Execute: git add . && git commit -m 'Deploy update' && git push")
        else:
            print("  ✅ Repositório limpo - todos os arquivos commitados")
        
        # Verificar último commit
        result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                              capture_output=True, text=True, check=True)
        if result.stdout:
            print(f"  📝 Último commit: {result.stdout.strip()}")
        
        # Verificar remote
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True, check=True)
        if result.stdout:
            print(f"  🔗 Repositório remoto: {result.stdout.strip()}")
            
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Erro ao verificar git: {e}")
        return False
    
    return True


def generate_render_config():
    """Gera configuração resumida para o Render"""
    print("\n📄 CONFIGURAÇÃO PARA O RENDER:")
    print("-" * 40)
    
    config = {
        "service_type": "Web Service",
        "name": "boletins-cromatograficos",
        "environment": "Python 3",
        "branch": "main",
        "build_command": "pip install -r requirements.txt",
        "start_command": "gunicorn --config gunicorn.conf.py app:app",
        "environment_variables": {
            "SECRET_KEY": "boletins_cromatograficos_render_2024",
            "FLASK_ENV": "production",
            "DEBUG": "false"
        }
    }
    
    print(f"📛 Nome do Serviço: {config['name']}")
    print(f"🐍 Ambiente: {config['environment']}")
    print(f"🌿 Branch: {config['branch']}")
    print(f"🔨 Build Command: {config['build_command']}")
    print(f"▶️  Start Command: {config['start_command']}")
    print("🔐 Variáveis de Ambiente:")
    for key, value in config['environment_variables'].items():
        print(f"   {key} = {value}")
    
    return config


def generate_render_urls():
    """Gera URLs esperadas no Render"""
    print("\n🌍 URLS ESPERADAS APÓS DEPLOY:")
    print("-" * 40)
    
    base_url = "https://boletins-cromatograficos.onrender.com"
    urls = [
        ("Página Principal", f"{base_url}"),
        ("Dashboard", f"{base_url}/dashboard"),
        ("Lista de Boletins", f"{base_url}/boletins"),
        ("Cadastro", f"{base_url}/cadastrar"),
        ("Importar Excel", f"{base_url}/importar")
    ]
    
    for name, url in urls:
        print(f"  📋 {name}: {url}")


def create_deployment_checklist():
    """Cria checklist de deployment"""
    print("\n✅ CHECKLIST DE DEPLOYMENT:")
    print("-" * 40)
    
    checklist = [
        "[ ] 1. Acesse https://render.com e faça login com GitHub",
        "[ ] 2. Clique em 'New +' > 'Web Service'", 
        "[ ] 3. Conecte o repositório 'mauricioamorim3r/validar_BoletimCromaAgosto'",
        "[ ] 4. Configure nome: 'boletins-cromatograficos'",
        "[ ] 5. Configure Build Command: 'pip install -r requirements.txt'",
        "[ ] 6. Configure Start Command: 'gunicorn --config gunicorn.conf.py app:app'",
        "[ ] 7. Adicione variáveis de ambiente (SECRET_KEY, FLASK_ENV, DEBUG)",
        "[ ] 8. Clique em 'Create Web Service'",
        "[ ] 9. Monitore logs de build (3-5 minutos)",
        "[ ] 10. Teste a URL gerada pelo Render",
        "[ ] 11. Verifique se dashboard mostra 23 boletins",
        "[ ] 12. Teste funcionalidades principais"
    ]
    
    for item in checklist:
        print(f"  {item}")


def main():
    """Função principal"""
    print_header()
    
    # Verificações
    files_ok = check_files()
    if not files_ok:
        print("\n❌ Corrija os arquivos ausentes antes de continuar")
        return 1
    
    validate_config()
    
    git_ok = check_git_status()
    if not git_ok:
        print("\n⚠️  Verifique a configuração do Git")
    
    # Gerar configurações
    config = generate_render_config()
    generate_render_urls()
    create_deployment_checklist()
    
    # Instruções finais
    print("\n" + "=" * 60)
    print("🎯 PRÓXIMOS PASSOS:")
    print("   1. Acesse https://render.com")
    print("   2. Siga o checklist acima") 
    print("   3. Monitore o deploy nos logs do Render")
    print("   4. Teste a aplicação na URL gerada")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())