FROM python:3.11 as build

WORKDIR /app

ENV PYTHONPATH=/app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Install Chromium for web loader
# Can disable this if you don't use the web loader to reduce the image size
RUN apt update && apt install -y chromium chromium-driver

# Install dependencies
COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --no-root --no-cache --only main

# ====================================
FROM build as release

COPY . .

ENV PATH="/opt/poetry/bin:$PATH"
ENV PYTHONPATH=/app

# Install runtime dependencies
RUN apt update && apt install -y chromium chromium-driver

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
