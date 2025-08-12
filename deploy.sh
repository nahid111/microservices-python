#!/bin/bash

# Build Docker images
echo "Building Docker images..."
docker build -t nahid111/py-micro-users ./users-service/
docker build -t nahid111/py-micro-converter ./converter-service/
docker build -t nahid111/py-micro-notification ./notification-service/
docker build -t nahid111/py-micro-gateway ./gateway/

# # Load images into kind cluster
echo "Loading images into kind cluster..."
kind load docker-image nahid111/py-micro-users
kind load docker-image nahid111/py-micro-converter
kind load docker-image nahid111/py-micro-notification
kind load docker-image nahid111/py-micro-gateway

# Create namespace
echo "Creating namespace..."
kubectl apply -f kubernetes/namespace.yaml

# Create secret from .env file
echo "Creating secrets..."
kubectl create secret generic secrets --namespace ns-py-micro --from-env-file=.env

# Apply Kubernetes configurations
echo "Deploying services..."
kubectl apply -f kubernetes/rabbitmq.yaml
kubectl apply -f kubernetes/mongo.yaml
kubectl apply -f kubernetes/postgres.yaml
kubectl apply -f kubernetes/users-job.yaml
kubectl wait --for=condition=complete job/users-migration-job --timeout=60s
kubectl apply -f kubernetes/users-deployment.yaml
kubectl apply -f kubernetes/converter.yaml
kubectl apply -f kubernetes/notification.yaml
kubectl apply -f kubernetes/gateway.yaml

# Wait for all deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=users --timeout=10s
kubectl wait --for=condition=ready pod -l app=converter --timeout=10s
kubectl wait --for=condition=ready pod -l app=notification --timeout=10s
kubectl wait --for=condition=ready pod -l app=gateway --timeout=10s

# Port forward the gateway service (since we're using kind)
echo "Setting up port forwarding for gateway service..."
kubectl port-forward svc/gateway-service -n ns-py-micro 8080:5000 &

echo "Deployment complete! Gateway service is accessible at http://localhost:8080"
