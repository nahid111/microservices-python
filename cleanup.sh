#!/bin/bash

# Kill any existing port-forward processes
echo "Stopping port-forward processes..."
pkill -f "kubectl port-forward"

# Delete all deployed resources
echo "Removing Kubernetes resources..."
kubectl delete -f kubernetes/gateway.yaml
kubectl delete -f kubernetes/notification.yaml
kubectl delete -f kubernetes/converter.yaml
kubectl delete -f kubernetes/users-deployment.yaml
kubectl delete -f kubernetes/users-job.yaml
kubectl delete -f kubernetes/postgres.yaml
kubectl delete -f kubernetes/mongo.yaml
kubectl delete -f kubernetes/rabbitmq.yaml

# Delete secrets
echo "Removing secrets..."
kubectl delete secret secrets -n ns-py-micro

# Delete namespace
echo "Removing namespace..."
kubectl delete -f kubernetes/namespace.yaml

echo "Cleanup complete!"
