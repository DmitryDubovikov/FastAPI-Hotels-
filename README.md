# FastAPI-Hotels

This project is 1/2 test assignment and 1/2 pet project for skills development and demonstration.

The FastAPI Hotel Booking project is a web application designed to facilitate hotel booking reservations. It allows users to browse available hotels, view details of each hotel, and make reservations for their desired dates. The project primarily serves as a RESTful API for hotel booking operations.

## Technologies used:
* FastAPI: For building the RESTful API, providing high performance and asynchronous capabilities.
* SQLAlchemy 2: As the ORM (Object-Relational Mapping) tool to interact with the PostgreSQL database, making it easier to manage and query hotel and user data.
* Alembic: Used for database migrations, allowing smooth updates to the database schema as the project evolves.
* Pydantic: For data validation, serialization, and modeling, ensuring clean and efficient data handling.
* PostgreSQL: The chosen relational database system for storing hotel information, user data, and reservations.
* Redis for Caching: Utilized for caching frequently accessed data, improving application speed and responsiveness.
* Redis as a Message Broker: Acts as a message broker for communication between components using publish-subscribe patterns.
* Celery: A distributed task queue system, integrated for handling background tasks such as email notifications.
* Flower: Provides a real-time monitoring and management dashboard for Celery, allowing administrators to monitor task progress.
* Pytest: Employed for testing the application, ensuring its reliability and correctness.
* Sentry: For error tracking and monitoring, helping to identify and resolve issues in real-time.
* Prometheus: Used for collecting and storing metrics from the application, enabling performance monitoring and analysis.
* Grafana: Integrated with Prometheus to create visual dashboards for monitoring application metrics and performance in real-time.
* SQLAdmin: Used for database administration, providing a graphical user interface and tools for managing PostgreSQL database.

## How to run:

* Clone project.

* Create .env file based on .env.example.
 
* Run containers:
 ```bash
 docker compose up --build
 ```
 
* Optional: load sample data from test_data_db.sql
 
* Check endpoints with OpenAPI docs:
http://localhost:8080/docs

 <img src=".screens/endpoints.png" alt="Image Alt Text" width="600">
 
* Admin panel:
 http://localhost:8080/admin

 <img src=".screens/endpoints.png" alt="Image Alt Text" width="800">
 
* Prometheus:
http://localhost:9090
 
* Grafana:
http://localhost:3000
 
* Flower:
http://localhost:5555/


./app.sh

alembic revision --autogenerate -m 'initial migration'

alembic upgrade head

docker run -d --name redis_db -p 6379:6379 redis  

celery -A app.tasks.celery:celery worker --loglevel=INFO

celery -A app.tasks.celery:celery flower  # http://localhost:5555/

http://127.0.0.1:8000/pages/hotels?location=Sey&date_from=2023-09-21&date_to=2023-09-28

