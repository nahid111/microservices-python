#!/bin/bash
set -e

# create a kind cluster if it doesn't exist
# ---------------------------------------------------------------
echo ""
if ! kind get clusters | grep -q "my-cluster"; then
    echo "🌱 Creating a new kind cluster named 'my-cluster'..."
    kind create cluster --name my-cluster --config ./scripts/kind-cluster-config.yaml
else
    echo "🔄 Using existing kind cluster 'my-cluster'."
fi

# Set the current context to the kind cluster
# ---------------------------------------------------------------
echo ""
echo "🌐 Setting kubectl context to kind-my-cluster..."
kubectl config use-context kind-my-cluster


# Install NGINX Ingress Controller
# ---------------------------------------------------------------
echo ""
echo "🔧 Installing NGINX Ingress Controller..."
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml

# Wait for NGINX Ingress Controller to be ready
# ---------------------------------------------------------------
echo ""
echo "⏳ Waiting for NGINX Ingress Controller to be ready..."
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Verify ingress is working
# ---------------------------------------------------------------
echo ""
echo "🔍 Verifying Ingress setup..."
kubectl -n ingress-nginx get services

# Build Docker images
# ---------------------------------------------------------------
echo ""
echo "🔨 Building Docker images..."
docker build -t nahid111/py-micro-users ./users-service/
docker build -t nahid111/py-micro-converter ./converter-service/
docker build -t nahid111/py-micro-notification ./notification-service/
docker build -t nahid111/py-micro-gateway ./gateway/

# Load images into kind cluster
# ---------------------------------------------------------------
echo ""
echo "📦 Loading images into kind cluster..."
kind load docker-image nahid111/py-micro-users --name my-cluster
kind load docker-image nahid111/py-micro-converter --name my-cluster
kind load docker-image nahid111/py-micro-notification --name my-cluster
kind load docker-image nahid111/py-micro-gateway --name my-cluster

# Create namespace if it doesn't exist
# ---------------------------------------------------------------
echo ""
echo "📁 Creating namespace..."
kubectl create namespace ns-py-micro --dry-run=client -o yaml | kubectl apply -f -

# Create secret from .env file
# ---------------------------------------------------------------
echo ""
echo "🔑 Creating secrets..."
kubectl create secret generic secrets --namespace ns-py-micro --from-env-file=.env


