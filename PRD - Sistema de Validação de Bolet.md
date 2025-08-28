PRD - Sistema de Validação de Boletins Cromatográficos
1. Visão Geral
1.1 Descrição do Produto
Sistema web para validação de resultados de análises cromatográficas de fluidos gasosos, implementando as metodologias A.G.A #8 e Controle Estatístico de Processo (CEP). A aplicação oferece interface inspirada em planilhas Excel para fácil adoção por usuários familiarizados com ferramentas tradicionais.

1.2 Público-Alvo
Laboratórios de análise de fluidos gasosos
Empresas do setor de petróleo e gás
Técnicos responsáveis pela coleta e validação de amostras
Órgãos reguladores (como ANP)
1.3 Problema a Resolver
Validação manual demorada e propensa a erros
Falta de padronização na validação de amostras
Dificuldade em detectar anomalias estatísticas
Impossibilidade de acompanhar histórico de amostras de forma eficiente
2. Requisitos Funcionais
2.1 Cadastro de Boletins
RF1: O sistema deve permitir o cadastro de boletins de análise com:

Identificação do boletim
Datas (coleta, recebimento, análise, emissão)
Identificação da instalação
Agente regulado
Ponto de medição
Responsável pela amostragem
Condições do processo (pressão, temperatura)
Propriedades do fluido (fator de compressibilidade, massa específica, massa molecular)
Componentes gasosos (15 componentes com percentual molar)
Responsáveis (técnico, elaboração, aprovação)
Observações
RF2: Validação automática de campos obrigatórios durante o cadastro

RF3: Cálculo automático da soma dos percentuais dos componentes (deve ser ~100%)

2.2 Validação de Componentes
RF4: Validação A.G.A #8 com limites:

Metano: 0-100%
Etano: 0-100%
Propano: 0-12%
i-Butano: 0-6%
n-Butano: 0-6%
i-Pentano: 0-4%
n-Pentano: 0-4%
Hexano: 0-100%
Heptano: 0-100%
Octano: 0-100%
Nonano: 0-100%
Decano: 0-100%
Oxigênio: 0-21%
Nitrogênio: 0-100%
CO2: 0-100%
RF5: Validação CEP usando:

Últimas 8 amostras válidas
Amplitude móvel (MR)
Média das amplitudes móveis (MR̄)
Fator d2 = 1.128 (para n=2)
Limites: LCS = x̄ + 3 * MR̄ / d2, LCI = x̄ - 3 * MR̄ / d2
RF6: Armazenamento do histórico de todos os componentes para cálculo do CEP

2.3 Geração de Relatórios
RF7: Relatórios de validação com:

Informações completas do boletim
Tabela de componentes com status (A.G.A #8 e CEP)
Tabela de propriedades do fluido
Observações
Área de aprovação com responsáveis
RF8: Status geral do boletim (VALIDADO/INVALIDADO) baseado na validação de todos os componentes

2.4 Visualização de Dados
RF9: Interface com abas estilo Excel:

Cadastrar Boletim
Relatórios
Histórico
RF10: Lista de boletins com:

Número do boletim
Instalação
Data de coleta
Data de validação
Status
Ação para visualizar relatório
RF11: Histórico de análises por componente com:

Componente
Boletim
Data coleta
Valor
Status A.G.A #8
Status CEP
2.5 Validações em Tempo Real
RF12: Validação durante cadastro:

Status A.G.A #8 para cada componente
Campos obrigatórios
Soma dos percentuais
3. Requisitos Não Funcionais
3.1 Desempenho
RNF1: Carregamento em até 3 segundos
RNF2: Suporte a 1000+ boletins simultaneamente
3.2 Usabilidade
RNF3: Interface inspirada em planilhas Excel
RNF4: Design responsivo para dispositivos móveis
RNF5: Mensagens de erro claras e específicas
3.3 Segurança
RNF6: Validação de todas as entradas
RNF7: Armazenamento seguro de dados
3.4 Confiabilidade
RNF8: Integridade dos dados em falhas
RNF9: Backup e recuperação de dados
3.5 Manutenibilidade
RNF10: Código bem documentado e modular
RNF11: Facilidade para adicionar novos componentes
4. Estrutura do Banco de Dados
4.1 Tabelas
boletins
id (PK, AI)
numero_boletim (TEXT, NOT NULL)
data_coleta (TEXT, NOT NULL)
data_recebimento (TEXT)
data_analise (TEXT)
data_emissao (TEXT)
identificacao_instalacao (TEXT)
agente_regulado (TEXT)
ponto_medicao (TEXT)
responsavel_amostragem (TEXT)
pressao (REAL)
temperatura (REAL)
observacoes (TEXT)
data_validacao (TEXT)
status (TEXT)
responsavel_tecnico (TEXT)
responsavel_elaboracao (TEXT)
responsavel_aprovacao (TEXT)
componentes
id (PK, AI)
boletin_id (FK, NOT NULL)
nome (TEXT, NOT NULL)
percentual_molar (REAL, NOT NULL)
status_aga (TEXT)
status_cep (TEXT)
propriedades
id (PK, AI)
boletin_id (FK, NOT NULL)
nome (TEXT, NOT NULL)
valor (REAL, NOT NULL)
status_aga (TEXT)
status_cep (TEXT)
historico_componentes
id (PK, AI)
componente (TEXT, NOT NULL)
boletin_id (FK, NOT NULL)
valor (REAL, NOT NULL)
data_coleta (TEXT, NOT NULL)
5. Fluxo de Trabalho
5.1 Cadastro de Boletim
Usuário acessa aba "Cadastrar Boletim"
Preenche todos os campos obrigatórios
Sistema valida em tempo real:
Campos obrigatórios
Soma dos percentuais
Status A.G.A #8
Ao submeter:
Armazena dados do boletim
Valida cada componente (A.G.A #8 e CEP)
Armazena histórico para futuras validações
Determina status geral
Redireciona para relatório de validação
5.2 Visualização de Relatórios
Usuário acessa aba "Relatórios"
Sistema lista todos os boletins
Usuário seleciona boletim para visualizar
Sistema exibe relatório completo
5.3 Histórico
Usuário acessa aba "Histórico"
Sistema lista todas as análises por componente
Permite busca por componente ou período
6. Interface do Usuário
6.1 Design
Inspirado em planilhas Excel
Cores: Azul para ações primárias, verde para validado, vermelho para inválido
Fonte: Segoe UI (padrão Windows)
Layout: Organizado em seções com bordas e fundos claros
6.2 Componentes Principais
Abas de navegação
Formulários com campos rotulados
Tabelas com bordas e cabeçalhos destacados
Badges para status
Botões com ícones
7. Tecnologias Utilizadas
7.1 Backend
Python 3.7+
Flask
SQLite
7.2 Frontend
HTML5
CSS3
JavaScript
Bootstrap 5
7.3 Arquitetura
MVC (Model-View-Controller)
Camadas de lógica separadas
Validações no backend e frontend
8. Arquivos Necessários para o Desenvolvimento
8.1 Backend
app.py - Aplicação principal Flask
Configurações do Flask
Rotas da aplicação
Lógica de validação (A.G.A #8 e CEP)
Funções do banco de dados
database.py - Configuração do banco de dados
Definição das tabelas
Funções de conexão
Inicialização do banco
8.2 Frontend
templates/base.html - Template base com estrutura HTML
Navegação
Estrutura geral
Inclusão de CSS e JS
templates/main.html - Página principal com abas
Abas de navegação
Conteúdo de cada aba
Lista de boletins
templates/cadastrar.html - Formulário de cadastro
Campos do boletim
Tabela de componentes
Validações em tempo real
templates/relatorio.html - Relatório de validação
Informações do boletim
Tabela de componentes
Status de validação
Área de aprovação
8.3 Assets
static/css/style.css - Estilos CSS
Design Excel-like
Responsividade
Cores e tipografia
static/js/app.js - Funcionalidades JavaScript
Validações em tempo real
Interações do usuário
Formatação de dados
9. Instalação e Execução
9.1 Pré-requisitos
Python 3.7 ou superior
pip (gerenciador de pacotes Python)
9.2 Passos de Instalação
Criar estrutura de pastas:

Line Wrapping

Collapse
Copy
1
2
3
4
5
6
7
8
9
10
11
12
/app
  /static
    /css
      style.css
    /js
      app.js
  /templates
    base.html
    main.html
    cadastrar.html
    relatorio.html
  app.py
Instalar dependências:
bash

Line Wrapping

Collapse
Copy
1
pip install flask
Executar a aplicação:
bash

Line Wrapping

Collapse
Copy
1
python app.py
Acessar o sistema:
Abrir navegador
Acessar http://localhost:5000
10. Casos de Teste
10.1 Testes de Funcionalidade
Cadastro de boletim válido
Cadastro com campos obrigatórios vazios
Cadastro com soma de percentuais fora do range
Validação A.G.A #8 com valores dentro e fora dos limites
Validação CEP com histórico suficiente e insuficiente
Geração de relatório
Visualização de histórico
10.2 Testes de Interface
Responsividade em diferentes tamanhos de tela
Validações em tempo real
Navegação entre abas
Formatação de tabelas e dados
11. Manutenção e Evolução
11.1 Atualizações Futuras
Adição de novos componentes
Modificação de limites da norma
Exportação de relatórios em PDF
Autenticação de usuários
Integração com outros sistemas
11.2 Monitoramento
Logs de erros
Métricas de performance
Feedback dos usuários
12. Considerações Finais
Este PRD detalha todos os requisitos para o desenvolvimento do Sistema de Validação de Boletins Cromatográficos. A aplicação foi projetada para ser robusta, intuitiva e alinhada às necessidades do setor de petróleo e gás, seguindo as melhores práticas de desenvolvimento e as especificações técnicas fornecidas.