# FinSync-Financial-Aggregation-Platform

## Table of Contents

- [FinSync-Financial-Aggregation-Platform](#finsync-financial-aggregation-platform)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setup](#setup)
    - [Docker Setup](#docker-setup)
    - [Local Environment](#local-environment)
    - [Dependencies](#dependencies)
  - [Usage](#usage)
    - [Running with Docker](#running-with-docker)
    - [Accessing the Services](#accessing-the-services)
    - [Black](#black)
    - [Flake8](#flake8)
    - [pytest](#pytest)
  - [Project Structure](#project-structure)
  - [Continuous Integration](#continuous-integration)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

**FinSync-Financial-Aggregation-Platform** is an information integration application that tracks the financial operations of an enterprise, aggregating data from different sources such as bank statements, ERP systems, CRM systems, and tax systems.

## Setup

### Docker Setup

To run the application using Docker:

1. Ensure you have Docker and Docker Compose installed on your system.
2. Clone the repository:
   ```bash
   git clone https://github.com/UtsvGrg/FinSync-Financial-Aggregation-Platform.git
   cd FinSync-Financial-Aggregation-Platform
   ```
3. Build and run the Docker containers:
   ```bash
   docker-compose build
   docker-compose up
   ```

### Local Environment

For local development without Docker:

1. Follow steps 1-2 from the Docker setup.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. To run the frontend:
   ```bash
   cd data_aggregator
   python manage.py runserver
   ```
5. Open the browser and go to
   ```bash
   http://127.0.0.1:8000/
   ```
   
   

### Dependencies

The project uses the following Python tools:

- **Flask**: A micro web framework for Python.
- **SQLite3**: A lightweight disk-based database.
- **Black**: A code formatter for consistent style.
- **Flake8**: A linting tool for style guide enforcement.
- **pytest**: A testing framework to ensure code correctness.

## Usage

### Running with Docker

To start the application:

```bash
docker-compose up
```

To rebuild the containers after making changes:

```bash
docker-compose build
docker-compose up
```

### Accessing the Services

After starting the containers, you can access the services at:

- PNL: http://localhost:5001/data
- Balance: http://localhost:5002/data
- Cash Flow: http://localhost:5003/data

### Black

To format your code:

```bash
black .
```

### Flake8

To run the linter:

```bash
flake8 .
```

### pytest

To run tests:

```bash
pytest
```

## Project Structure

The project is organized into three main services:

- **PNL (Profit and Loss)**
- **Balance Sheet**
- **Cash Flow**

Each service has its own directory under `data_sources/` containing:

- `Dockerfile`: Defines the container for the service.
- `app.py`: The Flask application for the service.
- `init_db.py`: Script to initialize the SQLite database.
- JSON file with sample data.

## Continuous Integration

This project uses GitHub Actions for CI. The pipeline runs on every push and pull request, performing code formatting checks, linting, and running tests.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

---
