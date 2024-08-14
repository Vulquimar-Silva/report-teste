# Algar Telecom API - Explicação Detalhada

Esta documentação explica detalhadamente a estrutura e funcionalidade da API desenvolvida para a Algar Telecom, que coleta dados DNS de diversas empresas, gera relatórios em PDF e os envia por e-mail.

## Sumário

- [Algar Telecom API - Explicação Detalhada](#algar-telecom-api---explicação-detalhada)
  - [Sumário](#sumário)
  - [Resumo da API](#resumo-da-api)
  - [Componentes Chave](#componentes-chave)
  - [Como Funciona](#como-funciona)
  - [Explicação dos Arquivos](#explicação-dos-arquivos)
    - [`docs/openapi.yaml`](#docsopenapiyaml)
    - [`prometheus/prometheus.yml`](#prometheusprometheusyml)
    - [`src/api/endpoints/dns_data_endpoint.py`](#srcapiendpointsdns_data_endpointpy)
    - [`src/api/endpoints/internal_report.py`](#srcapiendpointsinternal_reportpy)
    - [`src/api/endpoints/akamai_integration.py`](#srcapiendpointsakamai_integrationpy)
    - [`src/api/services/data_collector.py`](#srcapiservicesdata_collectorpy)
    - [`src/api/services/data_transformer.py`](#srcapiservicesdata_transformerpy)
    - [`src/api/services/email_sender.py`](#srcapiservicesemail_senderpy)
    - [`src/api/services/google_drive.py`](#srcapiservicesgoogle_drivepy)
    - [`src/api/services/pdf_generator.py`](#srcapiservicespdf_generatorpy)
    - [`src/core/config.py`](#srccoreconfigpy)
    - [`src/core/logger.py`](#srccoreloggerpy)
    - [`src/core/scheduler.py`](#srccoreschedulerpy)
    - [`src/core/security.py`](#srccoresecuritypy)
    - [`src/models/user.py`](#srcmodelsuserpy)
    - [`src/models/dns_data.py`](#srcmodelsdns_datapy)
    - [`src/models/report.py`](#srcmodelsreportpy)
    - [`src/main.py`](#srcmainpy)
    - [`template/css/styles-email.css`](#templatecssstyles-emailcss)
    - [`template/css/styles-pdf.css`](#templatecssstyles-pdfcss)
    - [`template/email_template.html`](#templateemail_templatehtml)
    - [`template/pdf_template.html`](#templatepdf_templatehtml)
    - [`.env`](#env)
    - [`.env.example`](#envexample)
    - [`docker-compose.yml`](#docker-composeyml)
    - [`Dockerfile`](#dockerfile)
    - [`README.md`](#readmemd)
    - [`requirements.txt`](#requirementstxt)
  - [Estrutura de Pastas](#estrutura-de-pastas)

## Resumo da API

A API desenvolvida para a Algar Telecom possui as seguintes funcionalidades principais:

1. **Coleta de Dados DNS**:

   - Coleta dados de navegação DNS de várias empresas usando uma API externa, incluindo a integração com a API da Akamai.
   - Cada empresa tem seus dados coletados de forma individualizada.
   
2. **Geração de Relatórios**:

   - Gera relatórios semanais em formato PDF contendo informações sobre os sites mais acessados, ameaças bloqueadas e outras estatísticas relevantes.
   - Utiliza templates HTML para a criação dos PDFs.

3. **Envio de Relatórios por E-mail**:

   - Envia os relatórios em PDF como anexos para os respectivos e-mails dos clientes.
   - Utiliza um template HTML estático para o corpo do e-mail.

4. **Armazenamento Seguro**:

   - Armazena os PDFs gerados no Google Drive corporativo por 90 dias.
   - Organiza os arquivos em uma estrutura de pastas específica no Google Drive.
   - Deleta automaticamente os relatórios após 90 dias.

5. **Autenticação e Segurança**:

   - Protege os endpoints da API utilizando autenticação JWT (JSON Web Token).
   - Oferece endpoints para registro de novos usuários e geração de tokens de autenticação.

6. **Monitoramento e Automação**:

   - Utiliza Prometheus para coletar métricas e Grafana para exibir dashboards de monitoramento.
   - Agendamento de tarefas automáticas para coleta de dados, geração e envio de relatórios.
   - Executa tarefas de coleta de dados diariamente e envio de relatórios em dias específicos (terça, quinta e sábado).

## Componentes Chave

- **Endpoints da API**:

  - `/token`: Gera um token JWT para autenticação.
  - `/register`: Registra um novo usuário.
  - `/api/dns-data`: Coleta os dados DNS (protegido por token JWT).
  - `/api/internal-reports`: Gera relatórios internos personalizados.
  - `/api/akamai/data`: Coleta dados da API da Akamai para proteção web (protegido por token JWT).
  
- **Serviços**:

  - `data_collector.py`: Coleta dados de navegação DNS e da API da Akamai.
  - `data_transformer.py`: Transforma e carrega os dados DNS coletados para o banco de dados.
  - `pdf_generator.py`: Gera PDFs dos relatórios.
  - `email_sender.py`: Envia os relatórios por e-mail.
  - `google_drive.py`: Faz upload dos PDFs para o Google Drive e gerencia a estrutura de pastas.

- **Segurança**:

  - `security.py`: Funções para geração e validação de tokens JWT.

- **Agendador de Tarefas**:

  - `scheduler.py`: Configura e gerencia as tarefas agendadas para coleta de dados e envio de relatórios.

## Como Funciona

1. **Coleta de Dados**:

   - O agendador executa a coleta de dados diariamente, chamando a API externa, incluindo a API da Akamai, para obter os dados DNS e de proteção de cada empresa.

2. **Transformação de Dados**:

   - Os dados brutos coletados são transformados e agregados pelo `data_transformer.py` e carregados no banco de dados.

3. **Geração de Relatórios**:

   - Com base nos dados coletados e transformados, a aplicação gera relatórios em PDF utilizando templates HTML.

4. **Envio de Relatórios**:

   - Os PDFs são enviados por e-mail para os clientes em dias específicos da semana.

5. **Armazenamento no Google Drive**:

   - Os PDFs são armazenados em uma estrutura de pastas organizada no Google Drive corporativo e mantidos por 90 dias.

6. **Autenticação e Segurança**:

   - Os endpoints sensíveis são protegidos por autenticação JWT, garantindo que apenas usuários autorizados possam acessar os dados.

7. **Monitoramento**:

   - A aplicação é monitorada utilizando Prometheus e Grafana, permitindo visualização em tempo real da saúde e desempenho da aplicação.

## Explicação dos Arquivos

### `docs/openapi.yaml`

Arquivo de configuração OpenAPI para a documentação da API.

### `prometheus/prometheus.yml`

Arquivo de configuração do Prometheus para monitoramento.

### `src/api/endpoints/dns_data_endpoint.py`

Este arquivo define o endpoint para coletar dados DNS. O endpoint é protegido por um token JWT.

### `src/api/endpoints/internal_report.py`

Este arquivo define o endpoint para gerar relatórios internos personalizados. O endpoint é protegido por um token JWT.

### `src/api/endpoints/akamai_integration.py`

Este arquivo define o endpoint para coletar dados diretamente da API da Akamai. O endpoint é protegido por um token JWT.

### `src/api/services/data_collector.py`

Este arquivo define a função para coletar dados DNS a partir de uma API externa e dados de proteção da API da Akamai.

### `src/api/services/data_transformer.py`

Este arquivo define a classe para transformar os dados DNS coletados e os dados da Akamai, carregando-os no banco de dados.

### `src/api/services/email_sender.py`

Este arquivo define a função para enviar e-mails com PDFs anexados utilizando smtplib.

### `src/api/services/google_drive.py`

Este arquivo define funções para autenticação e upload de arquivos para o Google Drive utilizando a Google API Client.

### `src/api/services/pdf_generator.py`

Este arquivo define a função para gerar PDFs utilizando templates Jinja2 e pdfkit.

### `src/core/config.py`

Este arquivo define a configuração da aplicação, carregando variáveis de ambiente a partir de um arquivo `.env`, incluindo a integração com a Akamai.

### `src/core/logger.py`

Este arquivo configura o logger para a aplicação, definindo o nível de log como INFO.

### `src/core/scheduler.py`

Este arquivo configura e inicia o agendador de tarefas utilizando APScheduler. Duas tarefas principais são agendadas: coleta de dados DNS, transformação dos dados e envio de relatórios.

### `src/core/security.py`

Este arquivo define funções de segurança, incluindo a geração de tokens JWT e a verificação de tokens para proteger endpoints da API.

### `src/models/user.py`

Este arquivo define o modelo de usuário, incluindo métodos para hashing de senha e verificação.

### `src/models/dns_data.py`

Este arquivo define o modelo para armazenar dados DNS transformados no banco de dados.

### `src/models/report.py`

Este arquivo define o modelo de relatório, incluindo informações sobre os relatórios gerados.

### `src/main.py`

Este é o ponto de entrada da aplicação Flask. Ele inicializa a aplicação, configura a conexão com o banco de dados, registra os blueprints para os endpoints da API e define as rotas para autenticação.

### `template/css/styles-email.css`

Estilos CSS para o template do e-mail.

### `template/css/styles-pdf.css`

Estilos CSS para o template do PDF.

### `template/email_template.html`

Template para o corpo do e-mail enviado aos clientes.

### `template/pdf_template.html`

Template para o relatório em PDF gerado para cada empresa.

### `.env`

Arquivo de variáveis de ambiente (não deve ser comitado).

### `.env.example`

Exemplo de arquivo de variáveis de ambiente.

### `docker-compose.yml`

Arquivo de configuração do Docker Compose.

### `Dockerfile`

Dockerfile para a construção da imagem Docker da aplicação.

### `README.md`

O README.md fornece uma visão geral da aplicação, incluindo instruções sobre como configurar e executar o projeto, os principais endpoints da API, e uma visão geral das funcionalidades e componentes da aplicação.

### `requirements.txt`

O arquivo `requirements.txt` lista todas as bibliotecas e pacotes Python necessários para executar a aplicação, incluindo versões específicas para garantir a compatibilidade. Este arquivo é usado para instalar as dependências com o comando `pip install -r requirements.txt`.

## Estrutura de Pastas

```plaintext
API/
├── src/
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── dns_data_endpoint.py  # Endpoint para dados DNS
│   │   │   └── internal_report.py    # Endpoint para relatórios internos
│   │   │   └── akamai_integration.py # Endpoint para integração com Akamai
│   │   ├── services/
│   │       └── data_collector.py     # Serviço de coleta de dados DNS e Akamai
│   │       └── data_transformer.py   # Serviço de transformação de dados (ETL)
│   │       └── email_sender.py       # Serviço de envio de e-mails
│   │       └── pdf_generator.py      # Serviço de geração de PDFs
│   │       └── google_drive.py       # Serviço de integração com Google Drive
│   ├── core/
│   │   ├── config.py                 # Configurações principais da aplicação, incluindo Akamai
│   │   ├── logger.py                 # Configuração de logs
│   │   ├── scheduler.py              # Agendamento de tarefas (APScheduler)
│   │   └── security.py               # Segurança e autenticação (JWT)
│   ├── models/
│   │   └── user.py                   # Modelo de usuário
│   │   └── dns_data.py               # Modelo de dados DNS
│   │   └── report.py                 # Modelo de relatório
│   ├── main.py                       # Arquivo principal da aplicação Flask, agora integrando Akamai
├── templates/
│   ├── css/
│   │   ├── styles-email.css          # Estilos CSS para e-mails
│   │   └── styles-pdf.css            # Estilos CSS para PDFs
│   ├── img/
│   │   ├── Logo_Algar.png            # Imagem do logo da Algar
│   │   └── security-algar.png        # Imagem de segurança da Algar
│   ├── email_template.html           # Template de e-mail
│   ├── pdf_template.html             # Template de PDF
├── docs/
│   ├── openapi.yaml                  # Documentação OpenAPI da API
├── prometheus/
│   ├── prometheus.yml                # Configuração do Prometheus
├── .env                              # Variáveis de ambiente (não versionado)
├── .env.example                      # Exemplo de variáveis de ambiente
├── Dockerfile                        # Dockerfile para a construção da imagem Docker
├── docker-compose.yml                # Arquivo de configuração do Docker Compose
├── README.md                         # Documentação principal do projeto
├── EXPLICACAO.md                     # Explicação detalhada da aplicação
└── requirements.txt                  # Dependências do projeto
