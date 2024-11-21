# FinSync-Financial-Aggregation-Platform


FinSync is an enterprise financial data integration platform that aggregates and harmonizes data from multiple financial sources. The system performs three core operations:


1. **Query Generation & Federation**
   - Generates SQL queries for different financial data sources
   - Federates these queries across multiple microservices (PNL, Balance Sheet, Cash Flow)
   - Handles data retrieval from distributed containers


2. **Data Processing & Validation**
   - Validates and corrects company IDs against known valid entries
   - Maps different schema formats to a standardized structure
   - Handles both numeric and non-numeric data types
   - Performs data cleaning and normalization


3. **Aggregation & Output**
   - Aggregates financial data across all sources per company
   - Calculates averages for numeric values
   - Generates timestamped CSV outputs
   - Provides API endpoints for frontend integration


## Table of Contents


- [FinSync-Financial-Aggregation-Platform](#finsync-financial-aggregation-platform)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
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
  - [System Architecture](#system-architecture)
  - [API Documentation](#api-documentation)
    - [Endpoints](#endpoints)
    - [Query Parameters](#query-parameters)
  - [Error Handling](#error-handling)
  - [Performance Considerations](#performance-considerations)
  - [Security](#security)
  - [Configuration](#configuration)
    - [Sample config.json](#sample-configjson)
  - [Troubleshooting](#troubleshooting)


## Introduction


**FinSync-Financial-Aggregation-Platform** is an enterprise-grade financial data integration platform that tracks and consolidates financial operations across multiple sources. The system:


- Aggregates data from bank statements, cash flow statements, and balance sheets
- Processes three main financial statements:
  - Profit & Loss (PNL)
  - Balance Sheet
  - Cash Flow Statement
- Provides real-time data validation and correction
- Outputs standardized financial reports
- Supports both API and CSV-based data access


The platform uses a microservices architecture with separate containers for each financial data source, ensuring scalability and maintainability.
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


## System Architecture


```
┌─────────────────┐
│    Frontend     │
│    Interface    │
└────────┬────────┘
         │
┌────────┴────────┐
│  Query Handler  │
└────────┬────────┘
         │
    ┌────┴────┐
    │  Main   │
    └────┬────┘
         │
┌────────┴────────┐
│Microservices DB │
└────────┬────────┘
┌────────┴────────┐
│ Data Processing │
└────────┬────────┘
         │
┌────────┴────────┐
│    Frontend     │
│    Interface    │
└─────────────────┘
```


## API Documentation


### Endpoints


1. **PNL Service** (Port 5001)
   - GET `/data`: Retrieve PNL data
   - GET `/query`: Execute custom PNL queries


2. **Balance Sheet Service** (Port 5002)
   - GET `/data`: Retrieve balance sheet data
   - GET `/query`: Execute custom balance sheet queries


3. **Cash Flow Service** (Port 5003)
   - GET `/data`: Retrieve cash flow data
   - GET `/query`: Execute custom cash flow queries


### Query Parameters
- `q`: SQL query string (required)
- `company_id`: Filter by company ID (optional)
- `date_range`: Filter by date range (optional)


## Error Handling


The system implements robust error handling for:
- Invalid company IDs
- Failed microservice connections
- Schema mapping errors
- Data type mismatches
- Query execution failures


## Performance Considerations


- Supports concurrent processing of multiple data sources
- Implements caching for frequently accessed data
- Optimizes query execution through federation
- Handles large datasets through pagination
- Uses connection pooling for database operations


## Security


- Input validation for all queries
- Company ID verification
- Rate limiting on API endpoints
- Secure configuration management
- Error message sanitization


## Configuration


### Sample config.json
```json
{
  "company_ids": ["COMP001", "COMP002", "COMP003"],
  "schema_mapping": {
    "pnl": {
      "revenue": "total_revenue",
      "expenses": "total_expenses"
    },
    "balance_sheet": {
      "assets": "total_assets",
      "liabilities": "total_liabilities"
    }
  }
}
```


## Troubleshooting


Common issues and solutions:
1. **Container Connection Failures**
   - Verify all containers are running
   - Check network configuration
   - Ensure correct ports are exposed


2. **Data Aggregation Issues**
   - Validate company IDs in config.json
   - Check schema mapping configuration
   - Verify data types in source systems


3. **Performance Issues**
   - Monitor container resources
   - Check query optimization
   - Verify connection pooling settings


---



