FROM python:3.13-slim

# Set environment variables to avoid python buffering and ensure Poetry installs dependencies correctly
ENV PYTHONUNBUFFERED=1 
# ENV POETRY_VIRTUALENVS_CREATE=false

# Set working directory inside the container
ENV WORK_DIR=/users_svc_app
RUN mkdir -p $WORK_DIR
WORKDIR $WORK_DIR

# Install system dependencies for psycopg2
RUN apt update && apt install -y libpq-dev gcc

# Copy the poetry configuration and pyproject.toml files
COPY pyproject.toml poetry.lock README.md $WORK_DIR
RUN pip install poetry

# Install project dependencies via Poetry (using the locked version)
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application files to the container
COPY . $WORK_DIR

CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker", "--capture-output", "--log-level", "debug"]

# gunicorn app.main:app --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker --capture-output --log-level debug
