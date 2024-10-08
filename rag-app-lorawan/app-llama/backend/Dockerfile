FROM python:3.11-slim as build

WORKDIR /backend

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /backend/

COPY .env /backend/.env

RUN poetry install --no-root --no-cache --only main

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
