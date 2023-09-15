# FastAPI-Hotels-

Technologies used:
FastAPI
SQLAlchemy 2
Alembic
Pydantic
PostgreSQL
Redis for caching
Redis as message broker
Celery
Flower
Pytest
Sentry

./app.sh

alembic revision --autogenerate -m 'initial migration'

alembic upgrade head

docker run -d --name redis_db -p 6379:6379 redis  

celery -A app.tasks.celery:celery worker --loglevel=INFO

celery -A app.tasks.celery:celery flower  # http://localhost:5555/

http://127.0.0.1:8000/pages/hotels?location=Sey&date_from=2023-09-21&date_to=2023-09-28

