# E-Commerce Microservices Deployment (Kubernetes)

This project demonstrates how to deploy a **microservices-based e-commerce application** using Kubernetes. It includes multiple independent services, containerized with Docker and exposed via a reverse proxy.

---

## Architecture Overview

The system consists of the following components:

* **NGINX** → Reverse proxy & API Gateway
* **Order Service** → Handles order creation and communication with payment service
* **Payment Service** → Simulates payment processing
* **Kubernetes LoadBalancer** → Exposes services externally

---

## Microservices Description

### 🔹 Order Service

* Built using **Flask (Python)**
* Provides REST API endpoints for order operations
* Stores orders **in-memory**
* Communicates with Payment Service via HTTP
* Includes health check endpoints for Kubernetes probes
* Runs on **port 5000**

### 🔹 Payment Service

* Independent Python service
* Simulates payment processing with **random success/failure**
* No dependency on other services
* Runs on **port 5001**

---

## Project Structure

```
.
├── Commands.txt
├── setup-namespace.sh
├── order-service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── payment-service
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

---

## Prerequisites

Make sure you have:

* Docker installed
* Kubernetes cluster (e.g., Minikube, K3s, EKS)
* kubectl configured
* Docker Hub account

---

## Setup & Deployment

### 1. Build & Push Docker Images

The `setup-namespace.sh` script:

* Builds Docker images for:

  * Order Service
  * Payment Service
* Pushes images to Docker Hub
* Creates a Kubernetes namespace
* Sets it as the default namespace

```bash
chmod +x setup-namespace.sh
./setup-namespace.sh
```

---

### 2. Deploy Services to Kubernetes

Apply your Kubernetes manifests:

```bash
kubectl apply -f k8s/
```

*(Assumes you have YAML files for deployments and services in `k8s/` directory)*

---

### 3. Verify Deployment

Check pods:

```bash
kubectl get pods
```

Check services:

```bash
kubectl get svc
```

---

### 4. Access the Application

If using LoadBalancer:

```bash
kubectl get svc
```

Get the external IP and access via browser or curl:

```bash
curl http://<EXTERNAL-IP>/orders
```

---

## Request Flow

1. Client sends request to **NGINX**
2. NGINX routes request to **Order Service**
3. Order Service:

   * Creates order
   * Calls **Payment Service**
4. Payment Service:

   * Simulates success/failure
5. Response flows back to client

---

## Health Checks

Both services expose endpoints for Kubernetes probes:

* Liveness Probe → ensures container is running
* Readiness Probe → ensures service is ready to receive traffic

---

## Important Notes (Production vs Learning)

###  What Juniors Often Assume

* In-memory storage is acceptable
* Service-to-service HTTP is always reliable
* LoadBalancer = production-ready exposure
* No need for retries or timeouts

### What Experienced Engineers Know

* **State must be externalized** → use databases (PostgreSQL, Redis)
* **Network calls fail frequently** → implement:

  * retries
  * circuit breakers
  * timeouts
* **Observability is critical**:

  * logging (ELK / Loki)
  * metrics (Prometheus)
  * tracing (Jaeger)
* **NGINX is not a full API gateway** → consider:

  * rate limiting
  * auth
  * service mesh (Istio / Linkerd)
* **LoadBalancer alone is not secure**:

  * TLS termination
  * WAF
  * proper ingress controller

---

## Future Improvements

* Add persistent database for orders
* Introduce message queue (Kafka/RabbitMQ) for async processing
* Implement retry & circuit breaker logic
* Add CI/CD pipeline
* Use Helm for Kubernetes packaging
* Introduce service mesh for advanced traffic control

---

## 🧪 Example API Endpoints

### Create Order

```bash
POST /orders
```

### Health Check

```bash
GET /health
```

---

## 🧹 Cleanup

To delete resources:

```bash
kubectl delete namespace microservices-lab
```

---

## 📚 Summary

This project demonstrates:

* Microservices architecture basics
* Docker containerization
* Kubernetes deployment
* Service-to-service communication
* Reverse proxy usage with NGINX

It serves as a strong foundation for moving toward **production-grade distributed systems**.

---
