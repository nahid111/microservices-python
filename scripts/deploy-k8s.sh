#!/bin/bash

# must run setup-cluster.sh first to create the cluster

# Apply Kubernetes configurations
echo ""
echo "🚚 Deploying services..."
kubectl apply -f k8s/rabbitmq.yaml
kubectl apply -f k8s/mongo.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/users-job.yaml
# name: users-migration-job
kubectl wait --for=condition=complete job/users-migration-job.yaml --timeout=120s
# Resource pattern is <resource-type>/<resource-name> - 
# "job" is the type and "users-migration-job" is the resource name as defined in users-job.yaml
kubectl apply -f k8s/users-deployment.yaml
kubectl apply -f k8s/converter.yaml
kubectl apply -f k8s/notification.yaml
kubectl apply -f k8s/gateway.yaml

# Wait for all deployments to be ready
echo ""
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=users -n ns-py-micro --timeout=30s
kubectl wait --for=condition=ready pod -l app=converter -n ns-py-micro --timeout=30s
kubectl wait --for=condition=ready pod -l app=notification -n ns-py-micro --timeout=30s
kubectl wait --for=condition=ready pod -l app=gateway -n ns-py-micro --timeout=30s

# Port forward the gateway service (since we're using kind)
echo ""
echo "🔗 Setting up port forwarding for gateway service..."
kubectl port-forward svc/gateway-service -n ns-py-micro 8080:5000 &

echo ""
echo "✅ Deployment complete!"
echo "🚀 Gateway service is accessible at http://localhost:8080/docs"
