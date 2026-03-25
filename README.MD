
# E-Commerce Microservices Application Deployment

This repository contains all the resources to deploy a **microservices-based e-commerce application** on Kubernetes. The application consists of multiple services orchestrated together, with **NGINX acting as a reverse proxy/API gateway**, and individual microservices handling orders and payments.

---

## Folder Structure

```

.
├── Commands.txt
├── loadbalancer-service.yaml
├── nginx-config.conf
├── nginx-configmap.yaml
├── nginx-deployment.yaml
├── order-service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── order-service-deployment.yaml
├── payment-service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── payment-service-deployment.yaml
├── setup-namespace.sh
└── README.md

```

- **order-service/**: Python Flask service for handling orders.
- **payment-service/**: Python Flask service for handling payment logic.
- **nginx-config.conf**: NGINX configuration to route traffic to backend services.
- **setup-namespace.sh**: Script to build/push Docker images and set up Kubernetes namespace.
- **nginx-deployment.yaml**: Kubernetes deployment for NGINX pods.
- **order-service-deployment.yaml** & **payment-service-deployment.yaml**: Kubernetes deployments for service pods.
- **loadbalancer-service.yaml**: Exposes NGINX pods externally through a LoadBalancer.

---

## Services Overview

### Order Service
- Built with **Flask**, exposes REST API endpoints.
- Stores orders in memory.
- Communicates with Payment Service over HTTP.
- Exposes a **health check** endpoint for Kubernetes probes.
- Runs on port `5000`.

### Payment Service
- Independent Python service for payment processing.
- Simulates payment success/failure randomly.
- Runs on port `5001`.
- No external dependencies on other services.

### NGINX
- Acts as **reverse proxy and API gateway**.
- Routes requests to backend services.
- Configuration highlights:
  - `upstream` blocks define backend service pools.
  - `proxy_pass` routes requests to backend.
  - `location /api/orders` forwards requests to Order Service.
  - `proxy_set_header` passes client information.

---

## Kubernetes Components

### Deployments
- **Order & Payment Service Deployments**
  - 2 replicas for redundancy.
  - Defines CPU/memory requests and limits.
  - **Liveness probe**: restarts pods on health failure.
  - **Readiness probe**: ensures pod is ready before receiving traffic.
  - **Service type**: ClusterIP (internal access only).

- **NGINX Deployment**
  - Mounts ConfigMap as `nginx.conf`.
  - Exposed internally via ClusterIP; fronted by LoadBalancer.

### Services
- **LoadBalancer Service**
  - Selects all pods with `app: nginx`.
  - Exposes port `80` externally.
  - Uses `sessionAffinity: ClientIP` to send the same client to the same pod when possible.

---

## Traffic Flow

```

User → LoadBalancer IP → Service → NGINX Pods → Backend Services (Order/Payment)

````

- Kubernetes load balances traffic across NGINX pods.
- NGINX routes requests to the appropriate backend service based on configuration.

---

## Setup Instructions

### Prerequisites
- Docker installed
- Kubernetes cluster (e.g., minikube, k3s, or cloud provider)
- kubectl configured
- DockerHub account (or another container registry)

### Step 1: Build & Push Service Images
```bash
./setup-namespace.sh
````

This script will:

* Build Docker images for order-service and payment-service.
* Push images to DockerHub.
* Create a Kubernetes namespace for logical separation.

### Step 2: Deploy Backend Services

```bash
kubectl apply -f order-service-deployment.yaml
kubectl apply -f payment-service-deployment.yaml
```

### Step 3: Deploy NGINX

```bash
kubectl apply -f nginx-configmap.yaml
kubectl apply -f nginx-deployment.yaml
```

### Step 4: Deploy LoadBalancer

```bash
kubectl apply -f loadbalancer-service.yaml
```

### Step 5: Verify Deployment

```bash
kubectl get all -n <your-namespace>
```

* Ensure all pods are `Running` and services are correctly exposed.

### Step 6: Test Application

* Access the application through the LoadBalancer IP on port `80`.
* Use `/api/orders` endpoint to interact with the Order Service.

---

## Notes

* Order Service stores data **in memory**, so all orders are lost when pods restart.
* Payment Service randomly simulates success/failure; suitable for testing communication between services.
* For production, consider using persistent storage and real payment integration.

---

This setup demonstrates **Kubernetes microservice orchestration** with **internal services, health checks, and external exposure via LoadBalancer**, while keeping deployments simple for local or cloud testing.


