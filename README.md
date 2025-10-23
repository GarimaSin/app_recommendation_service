# Recommender - Personalized Content Recommendation System (Demo)

This repository contains a production-pattern, end-to-end recommendation system for OTT/TV/News platforms.
It includes offline model training, ANN index build, online FastAPI serving, Kafka-based event streaming for real-time updates, Redis feature store, and infra artifacts for local development.

This demo is runnable locally with Docker Compose (Kafka + Redis + API) and uses Annoy for ANN search.

See docs/architecture.md for details.
