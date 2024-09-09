# Project Name

[FinSync-Financial-Aggregation-Platform](https://github.com/UtsvGrg/FinSync-Financial-Aggregation-Platform)

## Table of Contents

- [Project Name](#project-name)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setup](#setup)
    - [Local Environment](#local-environment)
    - [Dependencies](#dependencies)
  - [Usage](#usage)
    - [Black](#black)
    - [Flake8](#flake8)
    - [pytest](#pytest)
  - [Continuous Integration](#continuous-integration)
    - [CI Pipeline](#ci-pipeline)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

**FinSync-Financial-Aggregation-Platform** is an information integration application which tracks the financial operations of an enterprise pouring in from different sources such as bank statements, ERP systems, CRM systems, tax systems etc.

## Setup

### Local Environment

To set up the local development environment, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/UtsvGrg/FinSync-Financial-Aggregation-Platform.git
   cd FinSync-Financial-Aggregation-Platform
   ```

2. **Create and activate a virtual environment**:
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

The project uses the following Python tools:

- **Black**: A code formatter that ensures consistent style.
- **Flake8**: A linting tool that checks for style guide enforcement and simple errors.
- **pytest**: A testing framework to ensure code correctness.

These dependencies are listed in `requirements.txt`.

## Usage

### Black

**Black** is used to format your code automatically:

- To format your code:
  ```bash
  black .
  ```
- To check if the code is formatted correctly without changing files:
  ```bash
  black --check .
  ```

### Flake8

**Flake8** is used to enforce style guidelines and catch errors:

- To run Flake8 on your codebase:
  ```bash
  flake8 .
  ```
- To customize Flake8 settings, edit the `.flake8` file in the root directory.

### pytest

**pytest** is used to run tests and ensure your code works as expected:

- To run all tests:
  ```bash
  pytest
  ```
- To run a specific test file:
  ```bash
  pytest path/to/test_file.py
  ```
- For verbose output:
  ```bash
  pytest -v
  ```

## Continuous Integration

This project uses **GitHub Actions** to run a Continuous Integration (CI) pipeline.

### CI Pipeline

The CI pipeline is triggered on every push and pull request. It performs the following steps:

1. **Check out the code**.
2. **Set up Python** (specified version).
3. **Install dependencies**.
4. **Run Black** with `--check` to ensure code formatting.
5. **Run Flake8** to check for style guide adherence.
6. **Run pytest** to execute the test suite.

You can view the status of the CI pipeline under the "Actions" tab of the repository.

## Contributing

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the [MIT License](LICENSE).

---