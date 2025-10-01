from flask import Flask, jsonify, render_template, redirect, url_for
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
    """Redireciona diretamente para a aplicação principal"""
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    """Dashboard principal usando template HTML"""
    try:
        conn = get_db_connection()
        if conn:
            total_boletins = conn.execute('SELECT COUNT(*) FROM boletins').fetchone()[0]
            pendentes = conn.execute('SELECT COUNT(*) FROM boletins WHERE status = "pendente"').fetchone()[0]
            aprovados = conn.execute('SELECT COUNT(*) FROM boletins WHERE status = "aprovado"').fetchone()[0]
            rejeitados = conn.execute('SELECT COUNT(*) FROM boletins WHERE status = "rejeitado"').fetchone()[0]
            
            # Boletins recentes
            recent = conn.execute('''
                SELECT numero_boletim, data_emissao, laboratorio, status 
                FROM boletins 
                ORDER BY data_criacao DESC 
                LIMIT 10
            ''').fetchall()
            
            conn.close()
        else:
            total_boletins = pendentes = aprovados = rejeitados = 0
            recent = []
        
        stats = {
            'total': total_boletins,
            'pendentes': pendentes,
            'aprovados': aprovados,
            'rejeitados': rejeitados,
            'recent': recent
        }
        
        return render_template('dashboard.html', stats=stats)
    except Exception as e:
        logger.error(f"Erro no dashboard: {e}")
        return render_template('dashboard.html', stats={'total': 0, 'pendentes': 0, 'aprovados': 0, 'rejeitados': 0, 'recent': []})


@app.route('/importar')
def importar():
    """Página de importação de Excel"""
    return render_template('importar_excel.html')


@app.route('/cadastrar')
def cadastrar():
    """Página de cadastro de boletim"""
    return render_template('cadastrar.html')


@app.route('/relatorio')
def relatorio():
    """Página de relatórios"""
    return render_template('relatorio.html')


@app.route('/editar/<int:id>')
def editar_boletim(id):
    """Página de edição de boletim"""
    # Obter dados do boletim pelo ID se necessário
    return render_template('editar_boletim.html', id=id)


@app.route('/listar')
def listar_boletins():
    """Listar todos os boletins"""
    try:
        conn = get_db_connection()
        if conn:
            boletins = conn.execute('SELECT * FROM boletins ORDER BY data_emissao DESC').fetchall()
            conn.close()
            return render_template('dashboard.html', boletins=boletins)
        else:
            return render_template('dashboard.html', boletins=[])
    except Exception as e:
        print(f"Erro ao listar boletins: {e}")
        return render_template('dashboard.html', boletins=[])


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
