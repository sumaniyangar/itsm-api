# Mini ITSM REST API

A ServiceNow-inspired IT Service Management REST API built with Python FastAPI + SQLite.

## Features
- Full Incident lifecycle: New → In Progress → Resolved → Closed
- Change Request management with CAB workflow states
- Auto-generated INC/CHG numbers (ServiceNow-style)
- Business Rule-style automated timestamp logic
- Interactive Swagger UI at `/docs`
- Fully containerized with Docker

## Quick Start

### With Docker
docker-compose up --build

Open http://localhost:8000/docs

### Without Docker
pip install -r requirements.txt
uvicorn app.main:app --reload

## Tech Stack
Python · FastAPI · SQLAlchemy · SQLite · Docker · Pydantic