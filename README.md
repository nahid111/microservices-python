# Microservices Architecture in Python

<hr />

## About

<p>
This is a <strong><a href="https://fastapi.tiangolo.com/">FastApi</a></strong> implementation of the <strong>video to mp3 converter system</strong> demonstrated at <strong><a href="https://www.youtube.com/watch?v=ZYAPH56ANC8" target="_blank">Kantan Coding</a></strong>
<p/>

### Components

- **Api-Gateway**
    - Gateway to the system for handling all incoming requests from clients.
    - Stores uploaded videos in a **MongoDB** database.
    - Puts a message in **RabbitMQ** when a video is uploaded.
- **users-service**
    - Responsible for user registration and user authentication.
    - Stores user data in a **MySql** database.
- **Converter-Service**
    - Consumes message from **RabbitMQ** to get video file ID and downloads the video.
    - Converts the video to mp3 and stores in **MongoDB**.
    - Puts a message in **RabbitMQ** with the mp3 file ID.
- **Notification-Service**
    - Consumes message from **RabbitMQ** to get mp3 file ID.
    - Sends email to the client with the mp3 file ID.
    - Client can then send a request to the Api-Gateway with the mp3 file id along with his/her jwt to download the mp3.

## Running with docker compose
- Required envs <br/>
    Create a **.env** file in project root with the following environment variables.<br/>
    ```dotenv
    MYSQL_HOST="mysqlDB"
    MYSQL_PORT=3306
    MYSQL_DATABASE="db_local"
    MYSQL_PASSWORD=
    MYSQL_ROOT_PASSWORD=

    ACCESS_TOKEN_EXPIRES_IN=15
    REFRESH_TOKEN_EXPIRES_IN=60
    SECRET_KEY=
    SECRET_KEY_REFRESH=

    USERS_SERVICE_URL="http://users-service:8000"
    RABBITMQ_HOST="rabbitMQ"
    QUEUE_NAME="videos_queue_topic"
    MONGO_INITDB_ROOT_USERNAME=
    MONGO_INITDB_ROOT_PASSWORD=
    MONGODB_URL="mongodb://<YOUR_USER>:<YOUR_PASSWORD>@mongoDB:27017/"

    CONVERTER_QUEUE_TO_PUBLISH="mp3s_queue_topic"
    CONVERTER_QUEUE_TO_SUBSCRIBE="videos_queue_topic"

    NOTIFICATION_QUEUE_TO_SUBSCRIBE="mp3s_queue_topic"
    MAIL_USERNAME=
    MAIL_PASSWORD=
    ```
- Run docker compose
  ```commandline
  $ docker compose up
  ```
  Or run in detached mode
  ```commandline
  $ docker compose up -d
  ```
- Visit for Api Docs
  ```
  http://0.0.0.0:5000/docs
  ```
- Cleanup
  ```commandline
  $ docker compose down -v
  $ sudo rm -rf volMongo/ volMysql/ volRabbit/
  ```
