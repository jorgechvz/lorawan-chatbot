FROM python:3.11-slim as build

WORKDIR /backend

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy dependencies configuration files first to leverage Docker cache
COPY pyproject.toml poetry.lock* /backend/

# Copy .env file
COPY /backend/.env

# Install dependencies
RUN poetry install --no-root --no-cache --only main

# Copy all other project files
COPY . .

# Expose port and define default command
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
