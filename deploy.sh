#!/bin/bash

kubectl create secret generic secrets --from-env-file=.env

kubectl apply -f kubernetes/rabbitmq.yaml
kubectl apply -f kubernetes/mongo.yaml
kubectl apply -f kubernetes/mysql.yaml
kubectl apply -f kubernetes/users-job.yaml
kubectl apply -f kubernetes/users-deployment.yaml
kubectl apply -f kubernetes/converter.yaml
kubectl apply -f kubernetes/notification.yaml
kubectl apply -f kubernetes/gateway.yaml

#files=('rabbitmq' 'mongo' 'mysql' 'users-job' 'users-deployment' 'converter' 'notification' 'gateway')
#for f in "${files[@]}"; do
#    kubectl apply -f kubernetes/"$f".yaml
#    sleep 2s
#done

minikube service gateway-service
minikube service mongodb-service
minikube service rabbitmq

