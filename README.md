# Traffic Monitoring API

## Project Context

This project implements a REST API using Django Rest Framework to monitor road traffic. The API was developed to meet the requirements of an admission exercise, using Docker, PostgreSQL/PostGIS, and following recommended best practices.

## Main Features

* **REST Endpoints:** Provides full CRUD operations for `RoadSegment` and `TrafficReading`.
* **Permissions System:** Controls access for `admin` users (full access) and `anonymous` users (read-only).
* **Interactive Documentation:** Access the API documentation at `/api/docs/`.
* **Data Seeding:** Includes a management command to populate the database with sample data.
* **Filtering:** Allows filtering of road segments based on the traffic intensity of the last reading.
* **Tests:** Contains unit tests for the API functionalities and permissions system.
---

## How to Run the Project

### Prerequisites
* Git
* Docker & Docker Compose

### Steps
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Afonso-Simoes/traffic-monitor-api.git
    ```

2.  **Create .env file (exemple):**
    ```bash
    POSTGRES_DB=trafficdb
    POSTGRES_USER=trafficuser
    POSTGRES_PASSWORD=trafficpassword
    DB_HOST=db
    ```

3.  **Start the containers:**
    ```bash
    docker-compose up -d --build
    ```

### Accessing the Application
* **Documentation:** `http://localhost:8000/api/docs/`
* **Admin Panel:** `http://localhost:8000/admin/` (User: `admin`, Password: `admin`)

### Authentication Notes
The API uses **Token-based authentication**. To make authenticated requests (e.g., `DELETE`, `POST`), you must include an `Authorization` header.
* The header must be in the format: `Authorization: Token <your_token>`
* You can generate tokens in the Django admin panel.

### Importing Data
* **Only works if the dtabase is empty**
    ```bash
    docker-compose run --rm django_api python manage.py import_traffic_data
    ```
---

### Tests
* **Run tests:**
    ```bash
    docker-compose run --rm django_api python manage.py test
    ```
---
