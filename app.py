from flask import Flask, jsonify
import sqlite3
from datetime import datetime
import os
import logging

# Configuração
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'boletins_cromatograficos')

# Banco de dados
DATABASE = 'boletins.db'


def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Erro no banco: {e}")
        return None


def init_db():
    try:
        conn = get_db_connection()
        if conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS boletins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_boletim TEXT NOT NULL,
                    data_emissao DATE NOT NULL,
                    laboratorio TEXT NOT NULL,
                    status TEXT DEFAULT 'pendente',
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
    except Exception as e:
        logger.error(f"Erro init_db: {e}")


# Inicializar
init_db()


@app.route('/')
def index():
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Sistema de Validação de Boletins</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
            .header {{ text-align: center; color: #2c3e50; }}
            .status {{ background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .btn {{ background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧪 Sistema de Validação de Boletins</h1>
                <p>Deploy no Render - Versão 2.0</p>
            </div>
            <div class="status">
                <h3>✅ Sistema Online</h3>
                <p>Plataforma: Render</p>
                <p>Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
            <div>
                <a href="/api/health" class="btn">Health Check</a>
                <a href="/api/status" class="btn">Status</a>
                <a href="/dashboard" class="btn">Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html


@app.route('/dashboard')
def dashboard():
    try:
        conn = get_db_connection()
        if conn:
            total = conn.execute('SELECT COUNT(*) FROM boletins').fetchone()[0]
            conn.close()
        else:
            total = 0
        
        return jsonify({
            'total_boletins': total,
            'timestamp': datetime.now().isoformat(),
            'status': 'ok'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health')
def health():
    try:
        conn = get_db_connection()
        db_ok = conn is not None
        if conn:
            conn.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'ok' if db_ok else 'error',
            'timestamp': datetime.now().isoformat(),
            'platform': 'render'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/status')
def status():
    return jsonify({
        'status': 'operational',
        'version': '2.0.0',
        'platform': 'Render',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
