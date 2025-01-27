# Guia Completo para Testes do Projeto Report-Teste

Este guia detalha a estrutura do projeto **Report-Algar** e fornece um passo a passo para execução e teste do ambiente. Alguns arquivos relevantes são explicados, e comandos essenciais são fornecidos para facilitar a execução.

---

## Estrutura de Pastas

```
report-algar/
├── .vscode/
├── docs/
├── logs/
│   └── app.log
├── prometheus/
│   └── prometheus.yml
├── scripts/
│   ├── list_drive_folders.py
│   ├── share_drive_folder.py
├── src/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── akamai_integration.py
│   │   │   ├── dns_data_endpoint.py
│   │   │   ├── internal_report.py
│   ├── services/
│   │   ├── data_collector.py
│   │   ├── data_transformer.py
│   │   ├── email_sender.py
│   │   ├── google_drive.py
│   │   ├── pdf_generator.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── logger.py
│   │   ├── scheduler.py
│   │   ├── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── dns_data.py
│   │   ├── report.py
│   │   ├── user.py
│   ├── templates/
│   │   ├── email_template.html
│   │   ├── pdf_template.html
│   ├── main.py
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
├── report-algar-xxxxxx-xxxxxxxxxxxx.json
├── requirements.txt
├── start_build_docker.sh
```

---

## Descrição dos Arquivos

### 1. Arquivos Principais

- **main.py**: Ponto de entrada da aplicação. Configura as rotas e inicializa o servidor Flask.
- **config.py**: Gerencia as variáveis de configuração carregadas do arquivo `.env`.
- **scheduler.py**: Configura e gerencia o processo ETL diário usando `apscheduler`.
- **docker-compose.yml**: Gerencia a configuração de contêineres Docker para o projeto.
- **Dockerfile**: Define a imagem Docker usada para criar o ambiente da aplicação.
- **requirements.txt**: Lista as dependências Python do projeto.
- **start_build_docker.sh**: Script para iniciar o ambiente Docker.

### 2. Diretórios

#### `/api/endpoints`
Contém os endpoints REST para integração com o sistema.

#### `/api/services`
Módulos de serviço que realizam ações específicas, como:
- **data_collector.py**: Coleta dados do `json-server` ou da API Akamai.
- **data_transformer.py**: Transforma e carrega os dados no banco.
- **pdf_generator.py**: Gera PDFs baseados nos dados processados.
- **google_drive.py**: Gerencia ações relacionadas ao Google Drive.

#### `/core`
- **database.py**: Configuração da conexão com o banco de dados PostgreSQL.
- **logger.py**: Configura o logger para a aplicação.

#### `/templates`
Contém os templates HTML usados na geração de PDFs e e-mails.

---

## Passo a Passo para Testes

### Pré-requisitos

1. **Instale o Docker e Docker Compose**.
2. **Configure as variáveis de ambiente no arquivo `.env`**:
   - Certifique-se de preencher corretamente os campos de acesso ao Google Drive e ao banco de dados.

### 1. Configurar Rede Docker
Se a rede `docker_network` ainda não foi criada, execute:
```bash
docker network create docker_network
```

### 2. Inicializar o `json-server`
Navegue até o diretório do `json-server` e execute:
```bash
docker-compose up --build
```

### 3. Iniciar o Ambiente do Projeto
Na raiz do projeto, execute:
```bash
sudo ./start_build_docker.sh
```

Verifique se todos os contêineres estão ativos:
```bash
docker-compose ps
```

### 4. Executar o Pipeline Manualmente
Para executar o pipeline ETL e gerar PDFs:
```bash
curl -X POST http://localhost:5000/run_pipeline
```

Para verificar os logs:
```bash
docker-compose logs -f web
```

### 5. Gerenciar Google Drive
- Para compartilhar o PDF gerado no google drive service com outro google drive, execute o comando abaixo. 
Observação: edit o arquivo share_drive_folder.py com o seu e-mail e ID da pasta que foi gerado no report.
```bash
python -m scripts.share_drive_folder
```
- Para listar as pastas disponíveis no google drive service:
```bash
python -m scripts.list_drive_folders
```
- Para deletar as pastas disponíveis no google drive service:
```bash
python -m scripts.delete_drive_files
```

---

## Testando o Projeto

1. **Execute os scripts fornecidos acima**.
2. **Valide os PDFs gerados no Google Drive**. Certifique-se de que os dados estão preenchidos corretamente.
3. **Verifique os logs em caso de erro** no arquivo `logs/app.log` ou execute o comando `docker-compose logs -f web`.

---
