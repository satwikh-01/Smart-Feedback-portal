## Running the Project with Docker

This project is containerized using Docker and Docker Compose for easy setup and deployment. Below are the instructions and details specific to this project:

### Project-Specific Docker Requirements
- **Python Version:** The Dockerfile uses `python:3.12-slim` as the base image.
- **Dependencies:** All Python dependencies are installed from `requirements.txt` into a virtual environment (`.venv`) inside the container.
- **System Packages:** The build stage installs `build-essential` for compiling any native extensions. The runtime stage installs `curl` (used for health checks).

### Environment Variables
- The Docker Compose file is set up to optionally use a `.env` file for environment variables. Uncomment the `env_file: ./.env` line in `docker-compose.yml` if you have environment variables to provide.

### Build and Run Instructions
1. **Build and start the application:**
   ```sh
   docker compose up --build
   ```
   This will build the Docker image and start the FastAPI application.

2. **Access the application:**
   - The FastAPI app will be available at [http://localhost:8000](http://localhost:8000)

### Ports
- **8000:** The FastAPI application is exposed on port 8000 (`localhost:8000`).

### Special Configuration
- The application runs as a non-root user (`appuser`) inside the container for improved security.
- Alembic migration files and configuration (`alembic/`, `alembic.ini`) are included in the image, so database migrations can be managed from within the container if needed.
- A health check is configured at `/healthz` (make sure this endpoint exists in your FastAPI app).
