# Ansible AAP (Ansible as a Platform)

This project provides a web-based interface to run Ansible playbooks. It consists of a Python backend using FastAPI and a Vue.js frontend.

## Project Structure

```
.
├── ansible/            # Contains Ansible playbooks
├── api/                # FastAPI backend
├── frontend/           # Vue.js frontend
├── docker-compose.yml  # Docker Compose configuration
└── README.md
```

## Prerequisites

*   Docker
*   Docker Compose
*   Ansible
*   Python 3.9+
*   Node.js 16+
*   npm

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kimzhong/ansible_aap.git
cd ansible_aap
```

### 2. Backend Setup

The backend is a FastAPI application that exposes an API to run Ansible playbooks.

**Running with Docker:**

```bash
docker-compose build api
docker-compose up -d api
```

The API will be available at `http://localhost:8000`.

**Running locally:**

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Frontend Setup

The frontend is a Vue.js application that provides a user interface to interact with the API.

**Running with Docker:**

```bash
docker-compose build frontend
docker-compose up -d frontend
```

The frontend will be available at `http://localhost:8080`.

**Running locally:**

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## Usage

1.  Open your browser and navigate to the frontend URL (e.g., `http://localhost:5173`).
2.  The application will display a list of available Ansible playbooks.
3.  Click the "Run" button next to a playbook to execute it.
4.  The application will poll the backend for the task status and display the results once the playbook execution is complete.

## API Endpoints

### Authentication

*   `POST /api/v1/register`: Register a new user.
*   `POST /api/v1/token`: Authenticate a user and get a JWT access token.

### Users

*   `GET /api/v1/users/me`: Get the details of the currently authenticated user.

### Projects

*   `GET /api/v1/projects`: Get a list of all projects.
*   `POST /api/v1/projects`: Create a new project.
*   `GET /api/v1/projects/{project_id}`: Get the details of a specific project.
*   `PUT /api/v1/projects/{project_id}`: Update a specific project.
*   `DELETE /api/v1/projects/{project_id}`: Delete a specific project.

### Tasks

*   `GET /api/v1/tasks`: Get a list of all tasks.
*   `POST /api/v1/tasks`: Create a new task (run a playbook).
*   `GET /api/v1/tasks/{task_id}`: Get the status and result of a specific task.
*   `DELETE /api/v1/tasks/{task_id}`: Delete a specific task.

## Components

### Backend

*   **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Uvicorn**: An ASGI server implementation, for running the FastAPI application.
*   **Ansible Runner**: A tool and Python library that helps when interfacing with Ansible directly or as part of another system.

### Frontend

*   **Vue.js**: A progressive JavaScript framework for building user interfaces.
*   **Vite**: A build tool that aims to provide a faster and leaner development experience for modern web projects.
*   **Element Plus**: A Vue 3 based component library for developers, designers and product managers.
*   **Axios**: A promise-based HTTP client for the browser and Node.js.