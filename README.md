# Algar Telecom API

Esta API coleta dados DNS de diversas empresas, gera relatórios em PDF e os envia por e-mail. A API está configurada para funcionar tanto em ambiente de desenvolvimento quanto em produção.

## Sumário

- [Algar Telecom API](#algar-telecom-api)
  - [Sumário](#sumário)
  - [Instalação](#instalação)
  - [Uso](#uso)
    - [Ambiente de Desenvolvimento](#ambiente-de-desenvolvimento)
    - [Ambiente de Produção](#ambiente-de-produção)
  - [Endpoints](#endpoints)
    - [Autenticação](#autenticação)
    - [Coleta de Dados DNS](#coleta-de-dados-dns)
    - [Integração com Akamai](#integração-com-akamai)
    - [Geração de Relatórios Internos](#geração-de-relatórios-internos)
  - [Monitoramento](#monitoramento)
  - [Documentação da API](#documentação-da-api)
  - [Configurações Adicionais](#configurações-adicionais)
    - [Configurar Variáveis de Ambiente](#configurar-variáveis-de-ambiente)
    - [Configurar Google Drive](#configurar-google-drive)
    - [Inicializar Banco de Dados](#inicializar-banco-de-dados)
  - [Estrutura de Pastas](#estrutura-de-pastas)

## Instalação

1. Clone o repositório:

```sh
   git clone <URL_DO_SEU_REPOSITORIO>
   cd project
```

2. Crie um arquivo `.env` com base no `.env.example` e preencha com suas informações:

```sh
   cp .env.example .env
```

3. Instale as dependências:

```sh
   pip install -r requirements.txt
```

## Uso

### Ambiente de Desenvolvimento

Para rodar em modo desenvolvimento:

```sh
python src/main.py
```

### Ambiente de Produção

Para rodar em produção usando Docker:

```sh
docker-compose up --build
```

## Endpoints

### Autenticação

Gera um token JWT para autenticação.

- **URL**: `/token`
- **Método**: `POST`
- **Corpo da Requisição**:
  ```json
  {
    "username": "seu_username",
    "password": "sua_senha"
  }
  ```
- **Resposta**:
  ```json
  {
    "token": "seu_token_jwt"
  }
  ```

### Coleta de Dados DNS

- **URL**: `/api/dns-data`
- **Método**: `GET`
- **Cabeçalho**:
  - `Authorization: Bearer seu_token_jwt`
- **Resposta**:

```json
  {
    "data": [...]
  }
```

### Integração com Akamai

- **URL**: `/api/akamai/data`
- **Método**: `GET`
- **Cabeçalho**:
  - `Authorization: Bearer seu_token_jwt`
- **Resposta**:
  
```json
  {
    "akamai_data": [...]
  }
```

### Geração de Relatórios Internos

- **URL**: `/api/internal-reports`
- **Método**: `GET`
- **Cabeçalho**:
  - `Authorization: Bearer seu_token_jwt`
- **Resposta**:

```json
  {
    "reports": [...]
  }
```

## Monitoramento

A API utiliza Prometheus e Grafana para monitoramento. O Prometheus coleta métricas e o Grafana exibe dashboards.

- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Grafana**: [http://localhost:3000](http://localhost:3000) (Login: `admin`, Senha: `admin`)

## Documentação da API

A documentação da API está disponível no formato Swagger.

- **Swagger**: [http://localhost:5000/swagger](http://localhost:5000/swagger)
- **Redoc**: [http://localhost:5000/redoc](http://localhost:5000/redoc)

## Configurações Adicionais

### Configurar Variáveis de Ambiente

Crie um arquivo `.env` com base no `.env.example` e preencha as informações necessárias.

### Configurar Google Drive

1. Crie uma conta de serviço no Google Cloud Console.
2. Baixe o arquivo JSON da chave da conta de serviço e salve-o como `service_account_credentials.json` na raiz do projeto.
3. Certifique-se de que a variável `GOOGLE_DRIVE_CREDENTIALS_PATH` no `.env` aponta para `./service_account_credentials.json`.

### Inicializar Banco de Dados

Inicialize o banco de dados executando as migrações:

```sh
flask db init
flask db migrate -m "Add DNSData model"
flask db upgrade
```

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
│   │       └── data_collector.py     # Serviço de coleta de dados DNS
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
```

---

_©2024 L8 Group_

---
