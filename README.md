# 🧪 Sistema de Validação de Boletins Cromatográficos - BRAVA Energia

Sistema completo para validação de análises cromatográficas usando metodologia A.G.A #8 e Controle Estatístico de Processo (CEP) para o Campo de Atalaia.

## 🚀 Características Principais

### ✅ **Validação Automática**
- **Metodologia A.G.A #8**: Validação automática de 15 componentes gasosos
- **Controle Estatístico de Processo (CEP)**: Análise de tendências com 8 amostras
- **Cálculo Automático de Propriedades**: Massa Molecular, Fator de Compressibilidade, Massa Específica
- **Validação em Tempo Real**: JavaScript para feedback imediato durante preenchimento

### 📊 **Dashboard Avançado**
- **Estatísticas Visuais**: Cards com métricas de performance
- **Gráficos Interativos**: Tendências CEP com Chart.js
- **Análise de Componentes**: Identificação automática de componentes problemáticos
- **Filtros Dinâmicos**: Por período, status e componente

### 📋 **Relatórios Profissionais**
- **Exportação PDF**: Relatórios completos com identidade visual BRAVA
- **Layout Excel-Style**: Interface familiar ao processo atual
- **Checklist Completo**: 15 itens de validação conforme regulamentação
- **Histórico Completo**: Rastreabilidade total das análises

### 🎨 **Interface Moderna**
- **Design Figma**: Interface moderna baseada no protótipo fornecido
- **Responsivo**: Funciona em desktop, tablet e mobile
- **Glassmorphism**: Efeitos visuais modernos
- **UX Otimizada**: Fluxo intuitivo baseado no workflow Excel atual

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.7+
- Pip (gerenciador de pacotes Python)

### 1. **Instalar Dependências**
```bash
pip install flask reportlab
```

### 2. **Executar a Aplicação**
```bash
python app.py
```

### 3. **Acessar o Sistema**
Abra seu navegador e acesse: `http://127.0.0.1:8080`

## 📁 Estrutura do Projeto

```
validar_BoletimCromaAgosto/
├── app.py                    # Aplicação Flask principal
├── boletins.db              # Banco de dados SQLite (criado automaticamente)
├── static/
│   ├── css/
│   │   └── style.css        # Estilos personalizados
│   └── js/
│       └── app.js           # Validação JavaScript em tempo real
├── templates/
│   ├── base.html            # Template base
│   ├── dashboard.html       # Dashboard principal
│   ├── cadastrar.html       # Formulário de cadastro
│   └── relatorio_excel.html # Visualização de relatórios
└── README.md               # Este arquivo
```

## 🧪 Como Usar

### 1. **Cadastrar Novo Boletim**
1. Acesse o Dashboard
2. Clique em "CADASTRAR" 
3. Preencha os dados do boletim
4. Insira os percentuais molares dos 15 componentes
5. O sistema calculará automaticamente as propriedades do fluido
6. Clique em "Validar e Cadastrar Boletim"

### 2. **Visualizar Dashboard**
- **Cards de Estatísticas**: Total de boletins, taxa de validação, aprovados por metodologia
- **Componentes Problemáticos**: Lista dos componentes com maior taxa de erro CEP
- **Últimos Boletins**: Tabela com os boletins mais recentes e seus status
- **Gráfico de Tendências**: Visualização das tendências CEP dos componentes principais

### 3. **Aplicar Filtros**
- **Por Período**: 7, 30, 90 ou 365 dias
- **Por Status**: Validados, Invalidados ou Pendentes  
- **Por Componente**: Metano, Etano, Propano, Nitrogênio, CO2

### 4. **Gerar Relatórios PDF**
- No dashboard, clique no botão "PDF" ao lado de qualquer boletim
- Ou acesse o relatório detalhado e clique em "Download PDF"
- O PDF será gerado com layout profissional BRAVA

## 🔬 Metodologias de Validação

### **A.G.A #8 (American Gas Association)**
Limites de validação por componente:
- **Metano**: 0-100%
- **Etano**: 0-100%  
- **Propano**: 0-12%
- **i-Butano/n-Butano**: 0-6%
- **i-Pentano/n-Pentano**: 0-4%
- **Oxigênio**: 0-21%
- **Hidrocarbonetos Pesados**: 0-100%
- **Nitrogênio**: 0-100%
- **CO2**: 0-100%

### **CEP (Controle Estatístico de Processo)**
- **Método**: Amplitude Móvel com 8 amostras
- **Limites**: ±3σ (99,7% de confiança)
- **Constante d2**: 1.128 para n=2
- **Aplicação**: Componentes e propriedades calculadas

### **Cálculo Automático de Propriedades**
- **Massa Molecular**: Σ(xi × Mi) onde xi = fração molar, Mi = massa molar
- **Fator de Compressibilidade**: Baseado na composição (condições padrão 15°C, 1 atm)
- **Massa Específica**: ρ = (P × M) / (Z × R × T) a 20°C, 101.325 kPa

## 📊 Componentes Validados

O sistema valida automaticamente os 15 componentes obrigatórios:

1. **Metano** (C1)
2. **Etano** (C2)  
3. **Propano** (C3)
4. **i-Butano** (iC4)
5. **n-Butano** (nC4)
6. **i-Pentano** (iC5)
7. **n-Pentano** (nC5)
8. **Hexano** (C6)
9. **Heptano** (C7)
10. **Octano** (C8)
11. **Nonano** (C9)
12. **Decano** (C10)
13. **Oxigênio** (O2)
14. **Nitrogênio** (N2)
15. **Dióxido de Carbono** (CO2)

## 🛡️ Segurança e Backup

### **Banco de Dados Local**
- Arquivo SQLite: `boletins.db`
- Localização: Pasta raiz do projeto
- **Backup Recomendado**: Copiar regularmente o arquivo `boletins.db`

### **Dados Armazenados**
- Boletins completos com metadados
- Histórico completo de componentes para CEP
- Histórico de propriedades calculadas
- Checklist de validação por boletim

## 🚀 Melhorias e Manutenção

### **Log de Operações**
Todas as operações são registradas no console Python para auditoria.

### **Extensibilidade**
- Fácil adição de novos componentes
- Modificação de limites A.G.A #8
- Customização de cálculos de propriedades
- Novos tipos de relatório

### **Performance**
- SQLite otimizado para aplicações locais
- Queries indexadas para consultas rápidas
- Cache de cálculos estatísticos

---

## 📞 **Suporte Técnico**

Sistema desenvolvido especificamente para BRAVA Energia - Campo de Atalaia
Baseado no PRD fornecido e workflow Excel existente
Interface moderna baseada no protótipo Figma

**Versão**: 2.0 Final
**Data**: Agosto 2025
**Status**: Pronto para Produção ✅