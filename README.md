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
* **Part 3:** Implements endpoints for ingesting sensor data and searching for car passages.

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

2.  **Start the containers:**
    ```bash
    docker-compose up -d --build
    ```

### Accessing the Application
* **Documentation:** `http://localhost:8000/api/docs/`
* **Admin Panel:** `http://localhost:8000/admin/` (User: `admin`, Password: `admin`)

### Tests
* **Run tests:**
    ```bash
    docker-compose exec django_api python manage.py test
    ```
---
