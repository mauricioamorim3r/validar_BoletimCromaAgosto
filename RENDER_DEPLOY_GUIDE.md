# Sistema de Validação de Boletins Cromatográficos
# Deploy Guide para Render

## 🚀 Configuração do Deploy

### Configurações do Render:
- **Environment**: Python
- **Python Version**: 3.9
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

### Variáveis de Ambiente:
- `SECRET_KEY`: boletins_cromatograficos_render_2024
- `FLASK_ENV`: production

### Endpoints Disponíveis:
- `/` - Página principal
- `/api/health` - Health check
- `/api/status` - Status da API
- `/dashboard` - Dashboard (JSON)

### Recursos:
- ✅ Flask 3.0.0 application
- ✅ SQLite database
- ✅ Health monitoring
- ✅ Error handling
- ✅ Gunicorn WSGI server
- ✅ Python 3.11.7 runtime
- ✅ Minimal dependencies

### Deploy Steps:
1. Push para GitHub
2. Conectar repositório no Render
3. Deploy automático
4. Monitorar logs

### URLs:
- Production: https://[app-name].onrender.com
- Health Check: https://[app-name].onrender.com/api/health