# Deployment Guide

## 1. Abrir WSL (Ubuntu)

Desde PowerShell, CMD o Windows Terminal, ejecuta:

```bash
wsl -d Ubuntu
```

Esto abrirá la consola Ubuntu (WSL).

## 2. Iniciar Minikube 

```bash
minikube start --driver=docker
kubectl get nodes
kubectl get pods -A
```

Verifica que Minikube y el clúster Kubernetes están activos y funcionando.

## 3. Construir y cargar la imagen Docker en Minikube

Para que Minikube pueda usar la imagen Docker local, sin tener que subirla a un repositorio externo, construye la imagen dentro del entorno Docker que utiliza Minikube:

```bash
minikube image build -t flask-otel-app:latest ./app
```

Este paso es fundamental para evitar el error ErrImageNeverPull al desplegar la aplicación.

## 4. Levantar infraestructura simulada con Terraform

Mostrar archivo previo a los cambios:

```bash
cd ~/observabilidad-k8s/terraform
cat infra_description.txt
```

Levantar la infraestructura:

```bash
terraform init
terraform apply -auto-approve
```

Mostrar archivo generado para demostrar cambios posteriores:

```bash
cat infra_description.txt
```

## 5. Desplegar manifiestos Kubernetes con Ansible

```bash
cd /mnt/c/Users/julia/observabilidad-k8s/ansible
ansible-playbook k8s.yml
```

## 6. Verificar el estado del clúster y pods

```bash
kubectl get pods -A
```

## Acceso a la aplicación Flask (Endpoints)

Como el servicio Flask está configurado como NodePort, pero sin IP externa, usaremos port-forward para acceder localmente:

Abre una terminal WSL y ejecuta:

```bash
kubectl port-forward deployment/flask-otel-app 5000:5000
```

Mientras este comando está activo, en Windows abre tu navegador y prueba:

```bash
http://localhost:5000/hello
http://localhost:5000/error
```

## 8. Acceso a dakshboards y servicios de observabilidad

De nuevo, usando port-forward:

```bash
kubectl port-forward deployment/otel-collector 8888:8888
kubectl port-forward deployment/prometheus 9090:9090
kubectl port-forward deployment/grafana 3000:3000
kubectl port-forward deployment/jaeger 16686:16686
```

Una vez activos, puedes consultar en navegador:

-  Otel Collector (Pipeline): http://localhost:8888/metrics

-  Prometheus (Métricas): http://localhost:9090

-  Grafana (Dashboards): http://localhost:3000

-  Jaeger (Trazas): http://localhost:16686

## Finalizar y limpiar (opcional)

```bash
kubectl delete -f manifests/
minikube stop
minikube delete
```