# Attributions Wiki

Something Dana wanted me to make.

## Introduction
This project is built using a modern, efficient, and highly scalable tech stack, designed to provide a robust backend and a dynamic frontend experience. The technologies used range from a fast and efficient API framework to a powerful ORM and a flexible front-end design system.

## Tech Stack Overview

### Backend
1. **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. Used as the core framework for our API development.
2. **Prisma**: An open-source database toolkit. It includes an ORM (Object-Relational Mapping) for PostgreSQL, simplifying database operations and interactions.
3. **PostgreSQL**: A powerful, open-source object-relational database system that uses and extends the SQL language combined with many features to safely store and scale complicated data workloads.
4. **Uvicorn**: An ASGI server implementation for Python. Used to serve the FastAPI application, offering a lightning-fast, asynchronous server gateway interface.
5. **Pytest**: A framework that makes it easy to write small tests, yet scales to support complex functional testing. Used for testing our Python codebase.

### Frontend
1. **Jinja2**: A modern and designer-friendly templating language for Python, modeled after Django’s templates. Used for rendering HTML on the frontend.
2. **HTMX**: Allows you to access AJAX, CSS Transitions, WebSockets, and Server Sent Events directly in HTML, significantly simplifying the process of making dynamic interfaces.
3. **Tailwind CSS**: A utility-first CSS framework packed with classes that can be composed to build any design, directly in your markup. Integrated via CDN to simplify usage.

### Development Tools
1. **Poetry**: Used for Python package management and dependency resolution, ensuring a consistent development environment.
2. **Ruff**: A fast Python linter for enforcing a consistent code style.
3. **Pyright**: A static type checker for Python, ensuring code quality and consistency, especially when used with Python’s type hints.

### Hosting
1. **Railway**: A platform for building, deploying, and scaling applications quickly. Used for hosting our application.

Certainly! I'll outline a developer setup guide for your project, covering the necessary steps to get the environment running. This guide will be structured for MacOS or Linux/WSL users.

---

## Developer Setup Guide

### Prerequisites
- Ensure you have Python 3.7+ installed on your system.
- Install Poetry for Python package management.
- Install PostgreSQL on your system.

### 1. Setting Up PostgreSQL
Before you can run the application, you need to have PostgreSQL installed and properly configured:

#### For MacOS:
- Install PostgreSQL using Homebrew: `brew install postgresql`
- After installation, start the PostgreSQL service: `brew services start postgresql`
- Create a new PostgreSQL user (if needed) and remember the credentials as they will be used in your application configuration.

#### For Linux/WSL:
- Update your system's package list: `sudo apt update`
- Install PostgreSQL: `sudo apt install postgresql postgresql-contrib`
- Start the PostgreSQL service: `sudo service postgresql start`
- Optionally, switch to the `postgres` user: `sudo -i -u postgres` and create a new user/database as needed.

### 2. Database Setup with Prisma
After setting up PostgreSQL, follow these steps to configure the database with Prisma:

- Install Prisma CLI globally: `pip install prisma`
- Navigate to your project directory.
- Configure your database connection string in the Prisma schema file (usually `prisma/schema.prisma`). Update the `provider` and `url` fields under the `datasource` block.
- Run Prisma migrations to set up your database schema: `prisma migrate dev`. This step also seeds the database if a seed script is configured.

### 3. Running the Application
To run the application and access its features:

- Inside your project directory, install project dependencies using Poetry: `poetry install`.
- Activate the virtual environment created by Poetry: `poetry shell`.
- Start the FastAPI application. This is typically done using a command like `uvicorn app.main:app --reload`, but refer to your specific project documentation for the exact command.
- Once the server is running, you can access:
  - The Swagger UI for API documentation at `http://localhost:8000/docs`.
  - The web pages rendered by Jinja2 templates, accessible via the defined routes in your FastAPI application (e.g., `http://localhost:8000`).

### 4. Development Workflow
- Ensure you activate the Poetry virtual environment (`poetry shell`) each time you start a new development session. This ensures that you are using the correct versions of dependencies.
- Utilize the provided linters and type checkers (Ruff and Pyright) to maintain code quality.
- Write and run tests frequently using pytest to ensure the stability of new features and bug fixes.

### Additional Notes
- You may need to adjust the database connection settings, server host, and port as per your development environment.
- Always pull the latest changes from the repository and run `poetry install` to keep your dependencies up to date.

---

Make sure to tailor these instructions to align with any specific configurations or additional steps unique to your project. This guide provides a general outline but may need adjustments based on your project's setup and requirements.
## License
IDK yet






Factor: label
    Description too
    Beliefs a series of strings people can type

Beliefs have attributional structure

attribution
- Locus             isInternal ()
- Stability         isStable
- Controllability   isControllable

Locus, Stability, contrllability are all enums

enum Locus {
    Internal
    External
}

attribution 
    id
    Locus, 
    Stability
    Controllability

Belief 
    id
    Description
    Attribution
    Factors List of Factors

Factor
    Description 


Search by factor
