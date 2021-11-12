#!/bin/bash

helm upgrade -i -n dev -f helm/usecase-frontend/values.yaml frontend helm/usecase-frontend

echo -e "\n######## ADD INGRESS ADDRESSES ########\n"

echo -e "NEED TO RUN:\necho" $(kubectl get svc --namespace ingress-nginx nginx-ingress-nginx-controller --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}") blacklisted.testdev.com grafana.testdev.com " >> /etc/hosts\n"

echo -e "grafana-login:" $(kubectl get secrets victoria-grafana --namespace monitoring -o jsonpath='{.data.admin-user}' | base64 -D) "\n"

echo -e "grafana-password:" $(kubectl get secrets victoria-grafana --namespace monitoring -o jsonpath='{.data.admin-password}' | base64 -D) "\n"
