#!/bin/bash

# must run setup-cluster.sh first to create the cluster

# Label and annotate the namespace
# ---------------------------------------------------------------
echo ""
echo "🏷️  Labeling namespace for helm deployment..."
kubectl label namespace ns-py-micro app.kubernetes.io/managed-by=Helm
kubectl annotate namespace ns-py-micro \
  meta.helm.sh/release-name=py-micro \
  meta.helm.sh/release-namespace=ns-py-micro

# Install/Upgrade Helm chart
# ---------------------------------------------------------------
echo ""
echo "⚓ Deploying Helm chart..."
helm upgrade --install py-micro ./helm/py-micro \
    --namespace ns-py-micro \
    --create-namespace=false \
    --wait --timeout 5m --debug

# Wait for all pods to be ready
# ---------------------------------------------------------------
echo ""
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod --all -n ns-py-micro --timeout=20s

echo ""
echo "✅ Deployment complete!"
echo "🚀 Gateway service is accessible at http://localhost/docs"


# # Start port forwarding in the background
# kubectl port-forward -n ns-py-micro svc/rabbitmq 15672:15672 &> /dev/null &
# kubectl port-forward -n ns-py-micro svc/gateway-service 8000:8000 &> /dev/null &

# # Wait a moment for port forwarding to establish
# sleep 2

# echo "📊 RabbitMQ management UI is available at: http://localhost:15672"

