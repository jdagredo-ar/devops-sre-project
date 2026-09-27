#  DevOps & SRE Production-Ready Architecture

Este repositorio contiene una arquitectura de referencia orientada a producción, diseñada bajo principios de **SRE (Site Reliability Engineering)**, **GitOps**, automatización de infraestructura y prácticas nativas de la nube (Cloud-Native). El proyecto integra microservicios backend, observabilidad avanzada, gestión segura de secretos y un pipeline de integración continua (CI/CD) completamente automatizado.

---

## Arquitectura y Stack Tecnológico

* **Orquestación y Despliegue:** Kubernetes (Manifests nativos y Custom Resources).
* **Gestión de Tráfico:** NGINX Ingress Controller.
* **Seguridad y Secretos:** Bitnami Sealed Secrets (`SealedSecret`) para el almacenamiento seguro de credenciales en repositorios públicos.
* **Observabilidad y SRE:** 
  * **Prometheus:** Recolección de métricas y reglas de alertas personalizadas para presupuestos de errores (*Error Budget Burn Rate*).
  * **Grafana:** Dashboards as Code (`golden-signals.json`) midiendo disponibilidad, latencia y tráfico.
* **CI/CD & Automatización:** GitHub Actions (Validación offline de esquemas YAML, pruebas de dependencias e imágenes OCI con Docker Buildx).
* **Lenguajes y Herramientas:** Python 3.11, Docker.

---

##  Implementación SRE (SLIs, SLOs y Alertas)

La arquitectura define objetivos estrictos de nivel de servicio para garantizar la confiabilidad del sistema:
* **Indicador de Nivel de Servicio (SLI):** Tasa de peticiones HTTP exitosas frente al total de solicitudes en la API del backend.
* **Objetivo de Nivel de Servicio (SLO):** Disponibilidad objetivo $\ge 99.9\%$.
* **Presupuesto de Errores (Error Budget):** Control estricto del margen de error permitido.
* **Alertas de Agotamiento (Error Budget Burn Rate):** Configuración de reglas en Prometheus (`alert.rules.yml`) montadas en el directorio de runtime `/etc/prometheus/rules/*.yml` para notificar cuando la tasa de consumo del presupuesto de errores supere los umbrales críticos de degradación.

---

##  Seguridad con Sealed Secrets

Para cumplir con las mejores prácticas de seguridad en repositorios de código abierto:
* Las credenciales sensibles (bases de datos, tokens de administración) se cifran localmente utilizando `kubeseal` antes de ser versionadas.
* El clúster de Kubernetes descifra de forma transparente estos secretos (`app-secrets`) mediante el controlador de Sealed Secrets, evitando exponer datos en texto plano (`Plaintext Secrets`).

---

##  Pipeline de CI/CD (GitHub Actions)

El flujo de integración continua (`.github/workflows/ci.yml`) se ejecuta de manera automatizada en cada `push` o `pull_request` sobre la rama principal, asegurando calidad antes de cualquier despliegue:

1. **Checkout & Entorno:** Descarga limpia del código fuente y configuración de Python 3.11.
2. **Dependencias:** Instalación y verificación de paquetes del backend.
3. **Validación Estructural (GitOps Readiness):** Análisis estricto de sintaxis y estructura de todos los manifiestos YAML en `k8s/` (incluyendo validación especializada para Custom Resources como *SealedSecrets*) mediante un validador offline basado en Python.
4. **Construcción de Contenedores:** Empaquetado OCI de la imagen Docker del backend utilizando **Docker Buildx**.

---

##  Estructura del Repositorio

```text
devops-sre-project/
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline de CI/CD en GitHub Actions
├── backend/
│   ├── Dockerfile             # Definición de contenedor OCI del backend
│   └── requirements.txt       # Dependencias del servicio
├── k8s/
│   ├── ingress.yaml           # Configuración de enrutamiento NGINX Ingress
│   ├── sealed-secret.yaml     # Credenciales cifradas de forma segura
│   ├── stack.yaml             # Configuración de Prometheus, Grafana y SLOs (ConfigMaps)
│   └── storage.yaml           # Volúmenes y persistencia de datos
└── README.md                  # Documentación técnica del proyecto