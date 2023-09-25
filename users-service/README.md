# Users-Service

## Getting Started

1. clone the repo & cd into it.
2. Install python devels:
   <br/><nbsp/>`sudo apt install python3-dev libmysqlclient-dev build-essential `
3. Create a virtual environment for installing dependencies:
   <br/><nbsp/>`python3 -m venv project_name_venv`
4. Source the virtual environment:
   <br/><nbsp/>`source project_name_venv/bin/activate`
5. Install the dependencies in the virtual environment:
   <br/><nbsp/>`pip install -r requirements.txt`

## Setting up DB

1. ```$ pkg-config```
2. create the .env file in the project root directory and set the values:
   ```shell
    MYSQL_DB=
    MYSQL_HOST=
    MYSQL_PORT=
    MYSQL_USER=
    MYSQL_PASSWORD=
    
    SECRET_KEY=
    SECRET_KEY_REFRESH=
    ACCESS_TOKEN_EXPIRES_IN=
    REFRESH_TOKEN_EXPIRES_IN=
   ```

2. Run migrations
   ```shell
   alembic upgrade head
   ```

## Running the Server

```shell
  uvicorn app.main:app --reload

  OR

  uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## View api documentation

- Visit `http://127.0.0.1:8000/docs`

# Running with docker-compose


