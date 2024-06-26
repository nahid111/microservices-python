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

## Deploy to Kubernetes Cluster (<a href="https://minikube.sigs.k8s.io/">minikube</a>)

- Build your images and push them to dockerhub
- Set them appropriately in the deployment yaml files like so
  ```yaml
  apiVersion: apps/v1
  ...
  spec:
    ...
    template:
      ...
        containers:
          - image: nahid111/py-micro-users
  ```
- Populate envs properly
  ```dotenv
  MYSQL_HOST=mysql-service
  RABBITMQ_HOST=rabbitmq
  MONGODB_URL=mongodb://<YOUR_USER>:<YOUR_PASSWORD>@mongodb-service:27017/
  ```
- Change permission for deployment scripts
  ```commandline
  $ chmod +x deployment.sh
  $ chmod +x cleanup.sh
  ```
- Run `./deployment.sh`
- Use the minikube service url outputted in the terminal
  ```commandline
  |-----------|---------------|-------------|---------------------------|
  | NAMESPACE |     NAME      | TARGET PORT |            URL            |
  |-----------|---------------|-------------|---------------------------|
  | default   |gateway-service|        5000 | http://192.168.49.2:30312 |
  |-----------|---------------|-------------|---------------------------|
  ```
- For cleaning up, run `./cleanup.sh`
