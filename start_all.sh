export COMPOSE_FILE=arize-phoenix/server/docker-compose.yml
export COMPOSE_FILE=$COMPOSE_FILE:huggingface/tgi/docker-compose.yml
export COMPOSE_FILE=$COMPOSE_FILE:huggingface/tei/docker-compose.yml

docker compose --verbose up -d