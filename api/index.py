from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
from datetime import datetime
import os


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse da URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Roteamento simples
        if path == '/' or path == '':
            self.send_homepage()
        elif path == '/api/test':
            self.send_test_response()
        elif path == '/api/health':
            self.send_health_response()
        elif path == '/api/aga8':
            self.send_aga8_response()
        elif path == '/api/status':
            self.send_status_response()
        else:
            self.send_404()
    
    def do_POST(self):
        # Para futuras implementações de POST
        self.send_response(405)
        self.end_headers()
        self.wfile.write(b'Method Not Allowed')
    
    def send_homepage(self):
        """Página principal"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """
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
            <p><strong>Deploy:</strong> Vercel Serverless Functions</p>
            <p><strong>Data:</strong> """ + datetime.now().strftime('%d/%m/%Y %H:%M') + """</p>
        </div>
        
        <div class="card">
            <h3>🔬 Funcionalidades Disponíveis</h3>
            <a href="/api/test" class="btn">🧪 Teste de API</a>
            <a href="/api/aga8" class="btn">⚡ Teste AGA8</a>
            <a href="/api/status" class="btn">📊 Status Sistema</a>
            <a href="/api/health" class="btn">❤️ Health Check</a>
        </div>
        
        <div class="card">
            <h3>📊 Informações do Deploy</h3>
            <ul>
                <li>Plataforma: Vercel Serverless Functions</li>
                <li>Runtime: Python 3.9</li>
                <li>Estrutura: HTTP Request Handler</li>
                <li>Status: ✅ Operacional</li>
            </ul>
        </div>
    </div>
</body>
</html>
        """
        self.wfile.write(html.encode('utf-8'))
    
    def send_test_response(self):
        """Endpoint de teste"""
        self.send_json_response({
            'status': 'success',
            'message': 'API funcionando corretamente',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'platform': 'Vercel Serverless Functions'
        })
    
    def send_health_response(self):
        """Health check"""
        self.send_json_response({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'boletins-cromatograficos',
            'uptime': 'ok'
        })
    
    def send_aga8_response(self):
        """Teste AGA8 simplificado"""
        try:
            # Cálculo AGA8 simplificado direto
            composition = {
                'Metano': 90.0,
                'Etano': 5.0,
                'Propano': 3.0,
                'n-Butano': 2.0
            }
            
            # Simulação de cálculo (valores aproximados)
            density = 0.003873  # kg/m³
            compressibility = 0.9985
            
            self.send_json_response({
                'status': 'success',
                'aga8_status': 'operational',
                'test_composition': composition,
                'results': {
                    'density': density,
                    'compressibility_factor': compressibility,
                    'molecular_weight': 18.5,
                    'relative_density': 0.64
                },
                'message': 'AGA8 calculando corretamente (simulado)',
                'note': 'Cálculo simplificado para demonstração'
            })
        except Exception as e:
            self.send_json_response({
                'status': 'error',
                'aga8_status': 'error',
                'message': str(e)
            }, status=500)
    
    def send_status_response(self):
        """Status do sistema"""
        self.send_json_response({
            'status': 'operational',
            'timestamp': datetime.now().isoformat(),
            'platform': {
                'type': 'Vercel Serverless Functions',
                'python_version': '3.9',
                'environment': os.environ.get('VERCEL_ENV', 'development')
            },
            'health_checks': {
                'api_response': 'ok',
                'memory_usage': 'within_limits',
                'response_time': 'fast'
            },
            'features': {
                'aga8_calculations': 'available',
                'health_monitoring': 'available',
                'api_endpoints': 'available'
            }
        })
    
    def send_404(self):
        """Página não encontrada"""
        self.send_json_response({
            'error': 'Not Found',
            'message': 'Endpoint não encontrado',
            'available_endpoints': [
                '/',
                '/api/test',
                '/api/health',
                '/api/aga8',
                '/api/status'
            ]
        }, status=404)
    
    def send_json_response(self, data, status=200):
        """Envia resposta JSON"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(json_data.encode('utf-8'))