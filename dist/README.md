# SISTEMA DE VALIDAÇÃO DE BOLETINS CROMATOGRÁFICOS
## BRAVA ENERGIA - Campo Atalaia

**Build gerado em:** 2025-08-30 19:34:52

## RUN: COMO EXECUTAR

### Desenvolvimento:
```
python app.py
```
Acesse: http://127.0.0.1:3000

### Produção:
```
start_production.bat
```
Acesse: http://localhost:8080

## REPORT: FUNCIONALIDADES

OK: **Dashboard Analítico**
- Estatísticas de validação
- Gráficos de tendência
- Filtros avançados

OK: **Validação A.G.A #8**
- Limites normativos por componente
- Validação automática

OK: **Validação CEP (Controle Estatístico)**
- Cartas de controle 3-sigma
- Histórico de 8 amostras
- Detecção de outliers

OK: **Importação Excel**
- Template estruturado
- Processamento em lote
- Validação automática

OK: **Relatórios PDF**
- Análises completas
- Gráficos integrados
- Formatação profissional

## INFO: ESTRUTURA DE ARQUIVOS

```
dist/
├── app.py                 # Aplicação principal Flask
├── config.py             # Configurações desenvolvimento
├── config_production.py  # Configurações produção
├── excel_import.py       # Módulo importação Excel
├── boletins.db          # Banco de dados SQLite
├── requirements.txt     # Dependências Python
├── start.bat           # Iniciar desenvolvimento
├── start_production.bat # Iniciar produção
├── templates/          # Templates HTML
└── static/            # Arquivos estáticos (CSS/JS)
```

## DADOS: DADOS DO SISTEMA

- **Boletins processados:** 23
- **Componentes validados:** 348
- **Registros histórico:** 345

## AVISO: IMPORTANTE

1. **Desenvolvimento:** Use `start.bat`
2. **Produção:** Use `start_production.bat`
3. **Segurança:** Altere SECRET_KEY em produção
4. **Backup:** Faça backup regular de `boletins.db`

## HELP: SUPORTE

- **Verificar sistema:** Execute `python verificar_cep.py`
- **Logs:** Verifique terminal para erros
- **Banco:** Use SQLite Browser para inspeção

---
**© 2025 BRAVA ENERGIA - Campo Atalaia**
