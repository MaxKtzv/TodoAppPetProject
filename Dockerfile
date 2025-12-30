# syntax=docker/dockerfile:1

# Sets the image's base with preinstalled Python.
FROM python:3.14.0-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create the app working directory inside the container.
WORKDIR /app

# Copy only the dependency files first to leverage Docker caching
COPY pyproject.toml uv.lock ./

# Install dependancies into the container.
RUN uv sync --frozen --no-install-project

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]