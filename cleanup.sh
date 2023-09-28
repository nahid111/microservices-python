#!/bin/bash

kubectl delete -f kubernetes/rabbitmq.yaml
kubectl delete -f kubernetes/mongo.yaml
kubectl delete -f kubernetes/mysql.yaml
kubectl delete -f kubernetes/users-job.yaml
kubectl delete -f kubernetes/users-deployment.yaml
kubectl delete -f kubernetes/converter.yaml
kubectl delete -f kubernetes/notification.yaml
kubectl delete -f kubernetes/gateway.yaml

kubectl delete secret secrets

