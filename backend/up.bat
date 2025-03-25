docker compose build --no-cache && docker compose up -d

docker exec -it equeue_backend python -m alembic upgrade head
