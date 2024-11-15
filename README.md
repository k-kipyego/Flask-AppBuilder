The Flask-AppBuilder Site
========================

A web application built using Flask-AppBuilder framework that provides a robust foundation for building data-driven applications with authentication, user management, and automated CRUD operations.

Prerequisites
------------
- Python 3.7+
- pip package manager
- virtualenv (recommended)

Quick Start Guide
---------------

1. Set up your environment:
    ```bash
    python -m venv venv
    ```
    ```bash
    source venv/bin/activate
    ```
    ```bash
    pip install Flask-AppBuilder
    ```

2. Configure and start:
    ```bash
    cd app
    ```
    ```bash
    export FLASK_ENV=development
    ```
    ```bash
    flask fab create-admin
    ```
    ```bash
    flask run
    ```

Alternative Start Method:
```bash
python run.py