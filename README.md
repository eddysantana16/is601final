# FastAPI JWT Auth & Calculation Dashboard (IS601 Final Project)
This project is a secure FastAPI web application with JWT-based authentication, a calculation dashboard, and both front-end and API components. It includes full unit, integration, and end-to-end testing with Playwright, and a CI/CD pipeline that runs tests and pushes a Docker image to Docker Hub.

## Features

- Authentication
User registration with hashed passwords (bcrypt via passlib)
JWT token generation & verification for login
Protected API routes requiring authentication
- Front-End
register.html – User registration page with client-side validation
login.html – Login form that stores JWT in localStorage
dashboard.html – Displays calculation history & allows new calculations
- Calculations
Supports multiple operations: add, subtract, multiply, divide, power
Stores calculation history in the database with timestamps
User-specific history retrieval
- Security
Password hashing with bcrypt
Data validation using Pydantic v2
JWT tokens with expiration
- Testing
Unit tests for calculation services
Integration tests for authentication & history
Playwright E2E test for login → dashboard flow
- CI/CD
GitHub Actions pipeline:
Spins up PostgreSQL in CI
Runs all unit, integration, and E2E tests
On success, builds & pushes Docker image to Docker Hub

## Project Structure
is601final/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── database.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── calculations.py
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
├── tests/
│   ├── test_calc_service.py
│   ├── test_calculations_integration.py
│   ├── test_security.py
│   ├── test_users.py
│   └── test_e2e_dashboard.py
├── requirements.txt
├── Dockerfile
├── pytest.ini
├── README.md
└── .github/
    └── workflows/
        └── ci.yml

## Running the App Locally

- Clone repo
git clone https://github.com/eddysantana16/is601final.git
cd is601final
- Install dependencies
pip install -r requirements.txt
- Run locally
uvicorn app.main:app --reload
- Open: http://localhost:8000/register
- API Docs: http://localhost:8000/docs


## Run with Docker

- Pull from Docker Hub
docker pull eddysantana/is601final:latest
- Run container
docker run -d -p 8000:8000 eddysantana/is601final:latest
- Visit: http://localhost:8000

## CI/CD Workflow
- GitHub Actions is configured to:
- Spin up a PostgreSQL container
- Install dependencies
- Run unit + integration tests
- If all tests pass, build and push the Docker image to Docker Hub
- File: .github/workflows/ci.yml

## Testing
- Run all tests locally:
pytest -v
Includes: Unit tests for calculation logic, Integration tests for user registration, login, and history, Playwright E2E test for full login → dashboard flow

## CI/CD
- The GitHub Actions workflow:
- Spins up PostgreSQL container
- Installs dependencies
- Runs unit, integration, and E2E tests
- On success, builds & pushes Docker image to Docker Hub
- Located in .github/workflows/ci.yml

## Docker Hub
- Image URL: https://hub.docker.com/r/eddysantana/is601final
- Pull command: docker pull eddysantana/is601final:latest

## Author
- Eddy Santana