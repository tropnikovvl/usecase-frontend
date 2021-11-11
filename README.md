# usecase-frontend


kubectl get svc --namespace dev frontend-usecase-frontend --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}
