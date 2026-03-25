#!/bin/bash
set -ex
# Create namespace
kubectl create namespace microservices-lab

# Set as default context
kubectl config set-context --current --namespace=microservices-lab

# view all the namespace
kubectl get namespaces
