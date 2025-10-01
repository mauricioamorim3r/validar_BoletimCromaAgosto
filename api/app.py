# -*- coding: utf-8 -*-
"""
API Flask adaptada para Vercel Serverless
Sistema de Validação de Boletins Cromatográficos
"""

import os
import sys
import sqlite3
from flask import Flask, request, jsonify

# Adicionar diretório pai ao path para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Imports locais
try:
    from config import LIMITES_AGA8
    from aga8_gerg2008 import AGA8_GERG2008
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    # Fallback para valores básicos
    LIMITES_AGA8 = {
        'temp_min': 250, 'temp_max': 450,
        'press_min': 1, 'press_max': 200
    }

# Configuração da aplicação Flask para Vercel
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave_secreta_para_vercel')

# Configuração para ambiente serverless
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def init_database():
    """Inicializa banco de dados SQLite em memória para Vercel"""
    try:
        # Para Vercel, usar banco em memória ou arquivo temporário
        db_path = '/tmp/boletins.db' if os.path.exists('/tmp') else ':memory:'
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Criar tabela básica se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS boletins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_boletim TEXT UNIQUE,
                data_emissao DATE,
                data_coleta DATE,
                densidade_aga8 REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        return db_path
        
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
        return ':memory:'


# Inicializar banco na primeira execução
DB_PATH = init_database()


@app.route('/', methods=['GET'])
def index():
    """Endpoint principal - Health check"""
    return jsonify({
        'status': 'ok',
        'message': 'Sistema de Validação de Boletins Cromatográficos',
        'version': '1.0.0',
        'endpoints': {
            '/': 'Health check',
            '/api/aga8': 'Cálculos AGA8 (POST)',
            '/api/health': 'Status do sistema',
            '/api/boletins': 'Lista boletins (GET)',
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Testar AGA8
        solver = AGA8_GERG2008()
        test_comp = {'Metano': 90.0, 'Etano': 5.0, 'Propano': 3.0, 'n-Butano': 2.0}
        valid, msg, norm = solver.validate_composition(test_comp)
        
        aga8_status = 'ok' if valid else 'error'
        
        return jsonify({
            'status': 'healthy',
            'timestamp': str(sqlite3.datetime.datetime.now()),
            'database': 'connected',
            'aga8_engine': aga8_status,
            'python_version': sys.version
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@app.route('/api/aga8', methods=['POST'])
def calcular_aga8():
    """Endpoint para cálculos AGA8"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Extrair parâmetros
        temperatura = float(data.get('temperatura', 558.0))
        pressao = float(data.get('pressao', 50.0))
        composicao = data.get('composicao', {})
        
        if not composicao:
            return jsonify({'error': 'Composição não fornecida'}), 400
        
        # Validar limites
        if not (LIMITES_AGA8['temp_min'] <= temperatura <= LIMITES_AGA8['temp_max']):
            return jsonify({
                'error': f'Temperatura fora dos limites ({LIMITES_AGA8["temp_min"]}-{LIMITES_AGA8["temp_max"]} K)'
            }), 400
            
        if not (LIMITES_AGA8['press_min'] <= pressao <= LIMITES_AGA8['press_max']):
            return jsonify({
                'error': f'Pressão fora dos limites ({LIMITES_AGA8["press_min"]}-{LIMITES_AGA8["press_max"]} bar)'
            }), 400
        
        # Calcular com AGA8
        solver = AGA8_GERG2008()
        valid, msg, normalized = solver.validate_composition(composicao)
        
        if not valid:
            return jsonify({'error': f'Composição inválida: {msg}'}), 400
        
        resultado = solver.calculate_properties(temperatura, pressao, normalized)
        
        return jsonify({
            'success': True,
            'parametros': {
                'temperatura': temperatura,
                'pressao': pressao,
                'composicao_original': composicao,
                'composicao_normalizada': normalized
            },
            'resultados': resultado,
            'timestamp': str(sqlite3.datetime.datetime.now())
        })
        
    except ValueError as e:
        return jsonify({'error': f'Valor inválido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Erro no cálculo: {str(e)}'}), 500


@app.route('/api/boletins', methods=['GET'])
def listar_boletins():
    """Lista boletins do banco de dados"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM boletins ORDER BY created_at DESC LIMIT 10')
        boletins = cursor.fetchall()
        
        conn.close()
        
        # Converter para formato JSON
        boletins_json = []
        for boletim in boletins:
            boletins_json.append({
                'id': boletim[0],
                'numero_boletim': boletim[1],
                'data_emissao': boletim[2],
                'data_coleta': boletim[3],
                'densidade_aga8': boletim[4],
                'created_at': boletim[5]
            })
        
        return jsonify({
            'success': True,
            'count': len(boletins_json),
            'boletins': boletins_json
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao listar boletins: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handler para 404"""
    return jsonify({
        'error': 'Endpoint não encontrado',
        'available_endpoints': {
            '/': 'Health check',
            '/api/aga8': 'Cálculos AGA8 (POST)',
            '/api/health': 'Status do sistema',
            '/api/boletins': 'Lista boletins (GET)',
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler para 500"""
    return jsonify({
        'error': 'Erro interno do servidor',
        'message': str(error)
    }), 500


# Handler principal para Vercel
def handler(request):
    """Handler principal para Vercel serverless"""
    return app(request.environ, lambda status, headers: None)


# Para desenvolvimento local
if __name__ == '__main__':
    app.run(debug=True, port=5000)