.PHONY: build up down logs shell migrate makemigrations createsuperuser run clean

# Docker Compose コマンド
build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

# Django コマンド
shell:
	docker compose exec web bash

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

createsuperuser:
	docker compose exec web python manage.py createsuperuser

collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

# 初回セットアップ（マイグレーション実行）
run:
	docker compose exec web python manage.py migrate

# 全部リセット
clean:
	docker compose down -v
	docker system prune -f
