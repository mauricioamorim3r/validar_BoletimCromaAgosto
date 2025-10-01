# Deploy no Vercel - Sistema de Validação de Boletins

## 🚀 Configuração para Deploy

Este projeto foi configurado para deploy no Vercel com as seguintes adaptações:

### Estrutura do Projeto para Vercel
```
├── api/
│   └── app.py          # Flask app como serverless function
├── static/             # Arquivos estáticos
├── index.html          # Página principal
├── vercel.json         # Configuração do Vercel
├── requirements-vercel.txt  # Dependências otimizadas
└── [outros arquivos do projeto]
```

### Configurações Aplicadas

1. **vercel.json**: Configuração de builds e rotas
2. **api/app.py**: Flask adaptado para serverless functions
3. **requirements-vercel.txt**: Dependências otimizadas para Vercel
4. **index.html**: Interface web para testar a API

### Como Fazer Deploy

#### Opção 1: Vercel CLI
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

#### Opção 2: GitHub Integration
1. Conecte seu repositório ao Vercel
2. O deploy será automático a cada push

### Endpoints Disponíveis Após Deploy

- `GET /` - Health check e documentação
- `GET /api/health` - Status do sistema
- `POST /api/aga8` - Cálculos AGA8
- `GET /api/boletins` - Lista boletins

### Exemplo de Uso da API

```bash
# Health check
curl https://seu-projeto.vercel.app/api/health

# Cálculo AGA8
curl -X POST https://seu-projeto.vercel.app/api/aga8 \
  -H "Content-Type: application/json" \
  -d '{
    "temperatura": 558.0,
    "pressao": 50.0,
    "composicao": {
      "Metano": 85.0,
      "Etano": 7.0,
      "Propano": 4.0,
      "n-Butano": 2.0,
      "Nitrogênio": 2.0
    }
  }'
```

### Limitações do Vercel

1. **Timeout**: Máximo 60s por request
2. **Memória**: Limitada para serverless functions
3. **Storage**: Sem persistência permanente (use banco externo para produção)
4. **Cold Start**: Primeira requisição pode ser mais lenta

### Próximos Passos

1. Testar todos os endpoints após deploy
2. Considerar banco de dados externo (PostgreSQL, MongoDB Atlas)
3. Implementar cache para melhor performance
4. Monitorar logs e métricas no dashboard do Vercel

### Troubleshooting

- Se houver erro de timeout, otimize os cálculos AGA8
- Para erros de importação, verifique requirements-vercel.txt
- Logs disponíveis no dashboard do Vercel