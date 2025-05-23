# Proyecto Final - Observabilidad Full Stack con Kubernetes

## Descripción

Este proyecto implementa un sistema completo de observabilidad para una aplicación Flask desplegada en Kubernetes. Utiliza herramientas como Prometheus, Grafana, Loki, Jaeger y OpenTelemetry para recopilar métricas, logs y trazas.

## Tecnologías utilizadas

- **Kubernetes**: Orquestación de contenedores
- **Ansible**: Automatización del despliegue de manifiestos Kubernetes
- **Terraform**: Simulación de infraestructura como código
- **Prometheus, Grafana, Loki, Jaeger, OpenTelemetry**: Componentes de observabilidad
- **WSL (Ubuntu)**: Entorno de desarrollo

## Arquitectura

Se despliegan múltiples componentes en Kubernetes para la recopilación y visualización de datos de observabilidad:

- Aplicación Flask instrumentada con OpenTelemetry
- Prometheus para métricas
- Grafana para dashboards
- Loki para logs
- Jaeger para trazas distribuidas

## Cómo levantar el entorno

3. Ejecutar Terraform para simular la infraestructura:

```bash
cd terraform
terraform init
terraform apply
```

- null_resource ejecuta un pequeño script que simula (imprime) que Kubernetes se está desplegando
- local_file crea el archivo infra_description.txt, mostrando un output legible que demuestra que la infraestructura ha sido simulada.

De esta forma se puede mostrar la implementación de Terraform sin crear recursos en la nube (e incurrir en costos adicionales).

## Detalles de implementación

Los manifiestos Kubernetes están en la carpeta manifests/.

Ansible usa un rol k8s_deploy para aplicar los manifiestos.

Terraform simula infraestructura local con local_file y null_resource.

El entorno se ejecuta en WSL para compatibilidad y estabilidad.

## Autora

Julia G.
