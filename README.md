# usecase-frontend

**IMPORTANT**: This product may only be used for test purposes. Not for the production environment

## About This Repository

This repository contains a test version of the web application.
The application has a small web interface and sends action requests to the backend

**Flask_routes:**
- "/" - main page with two buttons
- "/healthz" - http check application status
- "/blacklisted" - takes the user's IP, DATE, URL_PATH and sends them to the backend to block him
- "/unlock" - provides an opportunity to unblock yourself
- "/debug" - returns json with parameters: IP, DATA, PATH.
- "/metrics" - flask metrics in prometheus format

## Pre-requisites

Your computer must have the following settings installed and configured:
- python3
- pip3

## How to install automatically
- bash install.sh

## How to install Manually

**deploy Kubernetes:**
- helm upgrade -i -n dev -f helm/usecase-frontend/values.yaml frontend helm/usecase-frontend

**deploy Docker (example):**
- docker run --rm -d --name frontend \
-e BACKEND_URL="http://192.168.1.61" \
-e BACKEND_PORT="8080" \
-p 8081:8081 \
tropnikovvl/usecase-frontend:latest

**config /etc/hosts:**
- echo $(kubectl get svc --namespace ingress-nginx nginx-ingress-nginx-controller --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}") blacklisted.testdev.com grafana.testdev.com >> /etc/hosts

**grafana login/password:**
- login: kubectl get secrets victoria-grafana --namespace monitoring -o jsonpath='{.data.admin-user}' | base64 -D
- password: kubectl get secrets victoria-grafana --namespace monitoring -o jsonpath='{.data.admin-password}' | base64 -D
