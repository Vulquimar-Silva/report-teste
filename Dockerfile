# Usa uma imagem oficial do Python como base
FROM python:3.10-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Instala dependências do sistema operacional necessárias e remove cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências para instalação
COPY requirements.txt /app/requirements.txt

# Instala as dependências do Python no modo de produção
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto para o container
COPY . /app

# Copia os arquivos .html para dentro da pasta templates
COPY templates/ /app/templates/

# Configura permissões no diretório de logs (caso seja criado pelo projeto)
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Cria um usuário não root para maior segurança
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Define variáveis de ambiente para evitar geração de bytecode e buffer do Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Comando para executar a aplicação Flask
CMD ["python", "src/main.py"]
