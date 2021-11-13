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
- "/?n=x" - squaring any integer 'x'

## Pre-requisites

Your computer must have the following settings installed and configured:
- python3
- pip3
- Helm


**Important**
The KUBE_NETWORK_CIDR parameter must be specified on line 87 in the Helm file, it is necessary to allow free access to the application by kubernetes pods (metrics, healthchecks and etc)
By default 10.244.0.0/16

It can be found using the command below
```shell
kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}'
```


## How to install automatically
```shell
bash install.sh
```

## How to install Manually

**deploy Kubernetes:**
```shell
helm upgrade -i -n dev -f helm/usecase-frontend/values.yaml frontend helm/usecase-frontend
```

**deploy Docker (example):**
```shell
docker run --rm -d --name frontend \
-e BACKEND_URL="http://192.168.1.61" \
-e BACKEND_PORT="8080" \
-p 8081:8081 \
tropnikovvl/usecase-frontend:latest
```

**config /etc/hosts:**
```shell
echo $(kubectl get svc --namespace ingress-nginx nginx-ingress-nginx-controller --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}") blacklisted.testdev.com grafana.testdev.com >> /etc/hosts
```

**grafana login/password:**
- login: kubectl get secrets victoria-grafana --namespace monitoring -o jsonpath='{.data.admin-user}' | base64 -D
- password: kubectl get secrets victoria-grafana --namespace monitoring -o jsonpath='{.data.admin-password}' | base64 -D
