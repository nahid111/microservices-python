# Users-Service

## Getting Started
### Install dependencies
1. clone the repo & cd into it.

2. Install libraries for using postgres with python: <br/>
   `$ sudo apt update` <br/>
   `$ sudo apt install -y libpq-dev gcc`
3. Create a virtual environment for installing dependencies:<br/>
   `$ python3 -m venv .venv`
4. Activate the virtual environment:<br/>
   `$ source .venv/bin/activate`
5. Install uv:<br/>
   `$ pip install uv`
6. Install the dependencies in the virtual environment:<br/>
   `$ uv sync --frozen`

### Setting up DB
- create the .env file using .env.example file in the project root directory and set the

- Run migrations <br/>
   `$ alembic upgrade head`


### Migrations
- create a migratrion  <br/>
   `$ alembic revision --autogenerate -m "MESSAGE"`

- apply migrations  <br/>
   `$ alembic upgrade head`

### Running the Server
- Run <br/>
   `$ fastapi dev`
   <br/>OR<br/>
   `$ uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

- View api documentation at http://127.0.0.1:8000/docs


# Running with docker-compose


# Code Quality

The project uses `ruff` for code formatting and linting:

```bash
# Format code
ruff format .

# Fix linting issues
ruff check . --fix

# Fix import sorting
ruff check . --select I --fix

# Fix unused imports
ruff check . --select I,F401 --fix
```