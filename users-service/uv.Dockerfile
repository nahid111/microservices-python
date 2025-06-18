FROM python:3.13-slim

# Set working directory inside the container
ENV WORK_DIR=/users_svc_app
RUN mkdir -p $WORK_DIR
WORKDIR $WORK_DIR

# Install system dependencies for psycopg2
RUN apt update && apt install -y libpq-dev gcc

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/

# Copy the uv configuration and pyproject.toml files
COPY pyproject.toml uv.lock README.md $WORK_DIR
RUN uv sync --locked

# Copy the project into the image
COPY . $WORK_DIR

CMD ["uv", "run", "gunicorn", "app.main:app", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker", "--capture-output", "--log-level", "debug"]

