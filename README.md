# UptimeMonitor

## Overview

This project is a simple uptime monitoring application built as an MVP.

It allows users to add URLs, periodically checks whether they are reachable, records the latest response information, and displays the results in a React dashboard.

The goal was to build a complete end-to-end application with a backend, frontend, scheduled monitoring, Docker support, and clear documentation.

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* APScheduler
* SQLite
* Requests

### Frontend

* React
* Vite
* Axios

### Containerization

* Docker
* Docker Compose

---

## Project Structure

```text
backend/
frontend/
docker-compose.yml
README.md
AI_LOG.md
```

---

## Running the Project

Clone the repository and run:

```bash
docker compose up --build
```

After the containers start:

Frontend

```text
http://localhost:5173
```

Backend

```text
http://localhost:8000
```

Swagger API

```text
http://localhost:8000/docs
```

---

## API Endpoints

### Add a URL

POST `/urls`

Example

```json
{
  "url": "https://example.com"
}
```

---

### Get all monitored URLs

GET `/urls`

---

### Get latest status

GET `/status`

---

## Testing

### Healthy URL

Add:

```text
https://example.com
```

Expected result:

* Status should become **UP**
* HTTP status should be **200**
* Response time should be displayed

---

### Invalid URL

Add something like:

```text
https://this-domain-does-not-exist-123456789.com
```

Expected result:

* Status should become **DOWN**
* No HTTP status should be returned

---

### Restricted URL

Some websites block automated requests and may return HTTP 403.

These are shown as **RESTRICTED** instead of **DOWN**.

---

## Results
<img width="1805" height="901" alt="Screenshot 2026-07-21 113547" src="https://github.com/user-attachments/assets/b3931f8d-5ee9-4b7e-9a8c-3abb737526ec" />

<img width="1831" height="876" alt="Screenshot 2026-07-21 113628" src="https://github.com/user-attachments/assets/d665631c-2797-4286-9e46-35315a955218" />


## Deployment Sketch

If this project were deployed to AWS, I would keep the architecture simple.

```
User
   ↓
React Frontend (S3 + CloudFront)
   ↓
FastAPI Backend (ECS or EC2)
   ↓
PostgreSQL (RDS)
```

For an MVP, SQLite works well locally, but PostgreSQL would be a better choice for a hosted version.

---

## Notes

This project was intentionally kept simple to match the assignment requirements. The focus was on building a working full-stack application that is easy to run, easy to understand, and can be started with a single Docker Compose command.
