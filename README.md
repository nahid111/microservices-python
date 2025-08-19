# Microservices Architecture in Python

<hr />

## About

<p>
This is a <strong><a href="https://fastapi.tiangolo.com/">FastApi</a></strong> implementation of the <strong>video to mp3 converter system</strong> demonstrated at <strong><a href="https://www.youtube.com/watch?v=ZYAPH56ANC8" target="_blank">Kantan Coding</a></strong>
<p/>

### Components

- **Gateway**
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
  Create a **.env** file in project root with the values from **example.env** file
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

## Deploy to local <a href="https://kind.sigs.k8s.io/docs/user/quick-start">kind</a> cluster 

- install kubectl & helm

  ```shell
  # Helm
  curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

  # kubectl
  curl -LO "https://dl.k8s.io/release/$(curl -sSL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  chmod +x kubectl
  sudo mv kubectl /usr/local/bin
  ```

- create .env using .env.example

  ```
  POSTGRES_DB=
  POSTGRES_HOST=postgres-service
  POSTGRES_PORT=5432
  POSTGRES_USER=
  POSTGRES_PASSWORD=

  SECRET_KEY=this-is-needed
  SECRET_KEY_REFRESH=this-is-needed-too

  MONGO_INITDB_ROOT_USERNAME=root
  MONGO_INITDB_ROOT_PASSWORD=example
  MONGODB_URL=mongodb://root:example@mongoDB:27017/

  RABBITMQ_HOST=rabbitMQ
  QUEUE_NAME=videos_topic
  CONVERTER_QUEUE_TO_PUBLISH=mp3s_topic
  CONVERTER_QUEUE_TO_SUBSCRIBE=videos_topic
  NOTIFICATION_QUEUE_TO_SUBSCRIBE=mp3s_topic

  MAIL_USERNAME=
  MAIL_PASSWORD=
  
  USERS_SERVICE_URL=http://users-service:8008
  ```
- Run `./deploy.sh`
- For cleaning up, run `./cleanup.sh`
