# Users-Service

## Getting Started
1. clone the repo & cd into it.
<!-- 2. Install python devels:
   <br/><nbsp/>`sudo apt install python3-dev libmysqlclient-dev build-essential ` -->
2. Create a virtual environment for installing dependencies:
   <br/><nbsp/>`python3 -m venv project_name_venv`
3. Source the virtual environment:
   <br/><nbsp/>`source project_name_venv/bin/activate`
4. Install the dependencies in the virtual environment:
   <br/><nbsp/>`pip install poetry`
   <br/><nbsp/>`poetry install --no-root`

## Setting up DB
1. create the .env file using .env.example file in the project root directory and set the
2. Run migrations
   ```shell
   alembic upgrade head
   ```


### Migrations
- create migratrion ```$ alembic revision --autogenerate -m "MESSAGE"```
- apply migration ```$ alembic upgrade head```

## Running the Server
```shell
  fastapi dev

  OR

  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## View api documentation
- Visit `http://127.0.0.1:8000/docs`


# Running with docker-compose


