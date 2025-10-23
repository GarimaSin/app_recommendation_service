.PHONY: build up down train index test
build:
	docker build -t recommender:local .
up:
	docker-compose up --build
down:
	docker-compose down
train:
	python3 models/trainer.py
index:
	python3 ann/build_index.py
test:
	pytest -q
