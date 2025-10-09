# Microservices Architecture in Python

<hr />

## About

<p>
This is a <strong><a href="https://fastapi.tiangolo.com/">FastApi</a></strong> implementation of the <strong style="font-size: 18px;">video to mp3 converter system</strong> demonstrated at <strong><a href="https://www.youtube.com/watch?v=ZYAPH56ANC8" target="_blank">Kantan Coding</a></strong>
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

- create **.env** using ***.env.example*** in project root

- Run `$ docker compose up -d`
- Visit `http://0.0.0.0:5000/docs`
- Cleanup
  ```commandline
  $ docker compose down -v
  $ sudo rm -rf volMongo/ volMysql/ volRabbit/
  ```

## Deploy to local <a href="https://kind.sigs.k8s.io/docs/user/quick-start">kind</a> cluster 

- install <a href="https://kind.sigs.k8s.io/docs/user/quick-start">kind</a>, <a href="https://pwittrock.github.io/docs/tasks/tools/install-kubectl/#install-kubectl-binary-via-curl">kubectl</a> & <a href="https://helm.sh/docs/intro/install/#from-script">helm</a>

- create **.env** using ***.env.example*** in project root
- Deploy `$ ./deploy.sh`
- Cleanup `$ ./cleanup.sh`
- Delete cluster `$ kind delete cluster --name=my-cluster`


### <a href="./cmds.md">cmds</a>


> ### NOTE:
> When using tools like <a href="https://k8slens.dev/">Lens</a>, Make sure to select the proper **namespace** while inspecting the cluster workloads 