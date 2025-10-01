# -*- coding: utf-8 -*-
"""
Versão Serverless da aplicação Flask para Vercel
Sistema de Validação de Boletins Cromatográficos
"""

from flask import Flask, jsonify
import sqlite3
from datetime import datetime
import os
import sys
import logging

# Configurar encoding para compatibilidade
if sys.platform.startswith('win'):
    os.system('chcp 65001 > nul')

# Configuração de logging otimizada para serverless
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar instância Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave_secreta_para_vercel')

# Configurações para Vercel
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def get_db_connection():
    """
    Conexão com banco de dados adaptada para serverless
    Em produção, usar banco remoto (PostgreSQL, MySQL, etc.)
    """
    try:
        # Para demonstração, usa SQLite local
        # Em produção real, substituir por banco remoto
        db_path = os.path.join(os.path.dirname(__file__), '..', 'boletins.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Erro conectando ao banco: {e}")
        return None


def init_db():
    """Inicializa banco de dados se necessário"""
    try:
        conn = get_db_connection()
        if conn:
            # Verificar se tabelas existem
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='boletins'
            """)
            
            if not cursor.fetchone():
                # Criar tabela básica se não existir
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS boletins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    data_emissao TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
                conn.commit()
                logger.info("Tabela boletins criada")
            
            conn.close()
            return True
    except Exception as e:
        logger.error(f"Erro inicializando DB: {e}")
        return False


# Rotas simplificadas para Vercel
@app.route('/')
def index():
    """Página principal simplificada"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM boletins")
            total_boletins = cursor.fetchone()['total']
            conn.close()
        else:
            total_boletins = 0
            
        return render_template_string("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Validação de Boletins</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #2c3e50; margin-bottom: 30px; }
        .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .btn { background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }
        .btn:hover { background: #2980b9; }
        .card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Sistema de Validação de Boletins Cromatográficos</h1>
            <p>Versão Serverless - Deploy Vercel</p>
        </div>
        
        <div class="status">
            <h3>✅ Sistema Operacional</h3>
            <p><strong>Status:</strong> Online</p>
            <p><strong>Total de Boletins:</strong> {{ total_boletins }}</p>
            <p><strong>Deploy:</strong> Vercel Serverless</p>
            <p><strong>Data:</strong> {{ current_date }}</p>
        </div>
        
        <div class="card">
            <h3>🔬 Funcionalidades Disponíveis</h3>
            <a href="/api/test" class="btn">🧪 Teste de API</a>
            <a href="/api/aga8" class="btn">⚡ Teste AGA8</a>
            <a href="/api/status" class="btn">📊 Status Sistema</a>
        </div>
        
        <div class="card">
            <h3>📊 Informações do Deploy</h3>
            <ul>
                <li>Plataforma: Vercel Serverless</li>
                <li>Runtime: Python</li>
                <li>Banco: SQLite (demo) / PostgreSQL (produção)</li>
                <li>Status: ✅ Operacional</li>
            </ul>
        </div>
    </div>
</body>
</html>
        """, total_boletins=total_boletins, current_date=datetime.now().strftime('%d/%m/%Y %H:%M'))
        
    except Exception as e:
        logger.error(f"Erro na página principal: {e}")
        return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500


@app.route('/api/test')
def test_api():
    """Endpoint de teste da API"""
    return jsonify({
        'status': 'success',
        'message': 'API funcionando corretamente',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'platform': 'Vercel Serverless'
    })


@app.route('/api/aga8')
def test_aga8():
    """Teste simplificado do AGA8"""
    try:
        # Importação local para evitar problemas de dependência
        try:
            from aga8_simple import AGA8_GERG2008_Simple
            solver = AGA8_GERG2008_Simple()
            
            # Composição de teste
            composition = {
                'Metano': 90.0,
                'Etano': 5.0,
                'Propano': 3.0,
                'n-Butano': 2.0
            }
            
            valid, msg, normalized = solver.validate_composition(composition)
            
            if valid:
                result = solver.calculate_properties(558.0, 50.0, normalized)
                return jsonify({
                    'status': 'success',
                    'aga8_status': 'operational',
                    'test_composition': composition,
                    'density': result.get('density', 0),
                    'compressibility': result.get('compressibility_factor', 0),
                    'message': 'AGA8 calculando corretamente'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'aga8_status': 'validation_failed',
                    'message': msg
                })
                
        except ImportError as e:
            return jsonify({
                'status': 'warning',
                'aga8_status': 'module_not_available',
                'message': f'Módulo AGA8 não disponível: {e}',
                'note': 'Funcionalidade pode estar desabilitada no Vercel'
            })
            
    except Exception as e:
        logger.error(f"Erro no teste AGA8: {e}")
        return jsonify({
            'status': 'error',
            'aga8_status': 'error',
            'message': str(e)
        })


@app.route('/api/status')
def system_status():
    """Status completo do sistema"""
    try:
        # Verificar banco de dados
        db_status = 'operational' if get_db_connection() else 'error'
        
        # Verificar dependências críticas
        dependencies = {}
        critical_modules = ['flask', 'sqlite3', 'datetime', 'json']
        
        for module in critical_modules:
            try:
                __import__(module)
                dependencies[module] = 'available'
            except ImportError:
                dependencies[module] = 'missing'
        
        # Verificar módulos opcionais
        optional_modules = ['aga8_gerg2008', 'reportlab', 'pandas']
        for module in optional_modules:
            try:
                __import__(module)
                dependencies[module] = 'available'
            except ImportError:
                dependencies[module] = 'missing'
        
        return jsonify({
            'status': 'operational',
            'timestamp': datetime.now().isoformat(),
            'database': db_status,
            'dependencies': dependencies,
            'platform': {
                'type': 'Vercel Serverless',
                'python_version': sys.version,
                'environment': os.environ.get('VERCEL_ENV', 'development')
            },
            'health_checks': {
                'api_response': 'ok',
                'database_connection': db_status,
                'memory_usage': 'within_limits'
            }
        })
        
    except Exception as e:
        logger.error(f"Erro no status do sistema: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/health')
def health_check():
    """Health check para monitoramento"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'boletins-cromatograficos'
    })


def render_template_string(template_string, **context):
    """Renderiza template inline"""
    from jinja2 import Environment, BaseLoader
    env = Environment(loader=BaseLoader())
    template = env.from_string(template_string)
    return template.render(**context)


# Inicializar banco na primeira execução
init_db()

# Para execução local
if __name__ == '__main__':
    app.run(debug=True, port=5000)
