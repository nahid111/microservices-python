## <a href="./README.md">README</a>

### setup cluster
```shell
# create a kind cluster
kind create cluster --name my-cluster --config ./k8s/kind-cluster-config.yaml
# Set the current context to the kind cluster
kubectl config use-context kind-my-cluster

# Install NGINX Ingress Controller
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
# Wait for NGINX Ingress Controller to be ready
kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=120s
# Verify ingress is working
kubectl -n ingress-nginx get services

# Create namespace & secrets
kubectl create namespace ns-py-micro --dry-run=client -o yaml | kubectl apply -f -
kubectl create secret generic secrets --namespace ns-py-micro --from-env-file=.env
```

### build & load images onto the kind cluster
```bash
# Build images
docker build -t nahid111/py-micro-users ./src/users-service/
docker build -t nahid111/py-micro-converter ./src/converter-service/
docker build -t nahid111/py-micro-notification ./src/notification-service/
docker build -t nahid111/py-micro-gateway ./src/gateway/
# Load images
kind load docker-image nahid111/py-micro-users --name my-cluster
kind load docker-image nahid111/py-micro-converter --name my-cluster
kind load docker-image nahid111/py-micro-notification --name my-cluster
kind load docker-image nahid111/py-micro-gateway --name my-cluster
```

### helm 
```bash
# label namespace
kubectl label namespace ns-py-micro app.kubernetes.io/managed-by=Helm
# annotate namespace
kubectl annotate namespace ns-py-micro \
  meta.helm.sh/release-name=py-micro \
  meta.helm.sh/release-namespace=ns-py-micro

# Install/Upgrade Helm chart
helm upgrade --install py-micro ./helm/py-micro \
    --namespace ns-py-micro \
    --create-namespace=false \
    --wait --timeout 5m --debug

# Wait for all pods to be ready
kubectl wait --for=condition=ready pod --all -n ns-py-micro --timeout=20s
```