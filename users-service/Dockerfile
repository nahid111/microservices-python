FROM python:3.13.5-slim

# Set environment variables to avoid python buffering and ensure Poetry installs dependencies correctly
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.0

# Install system dependencies for psycopg2 and Poetry
RUN apt update \
    && apt install -y --no-install-recommends gcc libpq-dev python3-dev curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
ENV INSTALL_PATH=/users_svc_app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

# Copy the poetry configuration and pyproject.toml files
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies via Poetry (using the locked version)
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the application files to the container
COPY . $INSTALL_PATH

CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker", "--capture-output", "--log-level", "debug"]

