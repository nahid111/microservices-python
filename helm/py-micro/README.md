# Python Microservices Helm Chart

This Helm chart deploys a complete Python microservices stack including:
- PostgreSQL database
- RabbitMQ message broker
- Users service
- Gateway service
- Converter service
- Notification service

## Prerequisites

- Kubernetes 1.16+
- Helm 3.0+
- PV provisioner support in the underlying infrastructure

## Installing the Chart

1. Install the chart:
```bash
helm install py-micro ./helm/py-micro
```

## Configuration

The following table lists the configurable parameters of the chart and their default values. You can override these in your own `values.yaml` file.

| Parameter | Description | Default |
|-----------|-------------|---------|
| namespace | Namespace for all resources | ns-py-micro |
| storage.className | Storage class for PVs | standard |
| storage.postgres.size | Postgres PV size | 1Gi |
| storage.rabbitmq.size | RabbitMQ PV size | 1Gi |
| postgres.image | PostgreSQL image | postgres:latest |
| rabbitmq.image | RabbitMQ image | rabbitmq:3-management |
| gateway.image | Gateway service image | nahid111/py-micro-gateway |
| users.image | Users service image | nahid111/py-micro-users |
| converter.image | Converter service image | nahid111/py-micro-converter |
| notification.image | Notification service image | nahid111/py-micro-notification |

## Uninstalling the Chart

To uninstall/delete the deployment:

```bash
helm uninstall py-micro
```
