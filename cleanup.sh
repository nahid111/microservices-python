#!/bin/bash

# Kill any existing port-forward processes
echo "🛑 Stopping port-forward processes..."
pkill -f "kubectl port-forward"

echo ""
# Check if Helm release exists and uninstall it
if helm list -n ns-py-micro | grep -q py-micro; then
    echo "⚓️🧹 Uninstalling Helm release: py-micro"
    helm uninstall py-micro -n ns-py-micro
else
    # Delete remaining Kubernetes resources
    echo "☸️ 🧹 Removing Kubernetes resources..."
    kubectl delete -f k8s/gateway.yaml
    kubectl delete -f k8s/notification.yaml
    kubectl delete -f k8s/converter.yaml
    kubectl delete -f k8s/users-deployment.yaml
    kubectl delete -f k8s/users-job.yaml
fi

# Delete secrets
echo ""
echo "🔐🧹 Removing secrets..."
kubectl delete secret secrets -n ns-py-micro

# Delete namespace
echo ""
echo "📦🧹 Removing namespace..."
kubectl delete -f k8s/namespace.yaml

echo ""
echo "✅ Cleanup complete!"
