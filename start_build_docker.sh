#!/bin/bash

# reset_docker.sh

set -e  # Faz o script "falhar" imediatamente em caso de erro de qualquer comando

echo "[INFO] Derrubando containers da aplicação e removendo imagens, volumes e órfãos vinculados ao docker-compose atual..."

# Remove apenas os containers, imagens (locais geradas pelo build), volumes e
# possíveis contêineres 'órfãos' atrelados ao COMPOSE_PROJECT_NAME (ou ao docker-compose no diretório atual)
docker-compose down --rmi local --volumes --remove-orphans || {
  echo "[ERRO] Falha ao executar docker-compose down. Verifique os logs."
  exit 1
}

echo "[INFO] Recriando o ambiente a partir do docker-compose.yml..."

# echo "[INFO] Criando rede docker_network se não existir..."
# docker network create docker_network || true

# 1) Inicia os serviços normalmente
docker-compose up --build -d

# 2) Entre no container e rode o 'init' para criar a pasta migrations/
docker-compose exec web flask db init

# 3) Gera um script de migração inicial com base nas Models definidas
docker-compose exec web flask db migrate -m "Initial migration"

# 4) Aplica essa migração para criar as tabelas no banco
docker-compose exec web flask db upgrade

echo "[INFO] Ambiente reconstruído com sucesso."
