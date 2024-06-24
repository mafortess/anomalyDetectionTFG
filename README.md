# anomalyDetectionTFG

## Monitorización de sistemas para la detección de anomalías

### Descripción del Proyecto

Este proyecto tiene como objetivo desarrollar una solución integral para la monitorización de diversos sistemas, incluyendo hosts, contenedores Docker y Kubernetes, así como dispositivos físicos. Utilizando Prometheus como herramienta central, se supervisan métricas clave como CPU, RAM, memoria, tráfico de red y consumo de energía. Los datos recolectados se almacenan en InfluxDB y se visualizan en dashboards creados con Grafana, los cuales se integran en una aplicación web fullstack desarrollada con Django.

### Estructura del Repositorio

Este repositorio contiene los archivos esenciales para montar el sistema de monitorización por tu cuenta. Aquí están los componentes principales:

- **django_web/**: Archivos del proyecto Django que incluyen el backend y el frontend de la aplicación web.
- **alertmanager/**: Archivo de configuración de AlertManager.
- **prometheus/**: Archivo de configuración de Prometheus.
- **scrape_configs/**: Configuraciones adicionales para la recolección de métricas.
- **docker/**: Archivos `.yml` para el despliegue de contenedores Docker.
- **simulations/**: Códigos de simulación para el consumo energético y otras pruebas.
- **scripts/**: Scripts utilizados para el monitoreo y pruebas, incluyendo tshark, iperf3, stress-ng y las tareas cron.
- **telegram_api/**: Scripts para enviar notificaciones al bot de Telegram.

### Características del Proyecto

1. **Backend en Django**: Gestiona la recolección de datos y la comunicación con Prometheus, además de integrar aplicaciones para ciberseguridad e inteligencia artificial.
2. **Frontend Personalizable**: Presenta las métricas al usuario final a través de dashboards creados con Grafana.
3. **Monitorización en Tiempo Real**: Supervisión de hosts, contenedores Docker y Kubernetes, así como dispositivos físicos.
4. **Inteligencia Artificial**: Implementada con librerías como scikit-learn y modelos como Isolation Forest para detectar anomalías en tiempo real.
5. **Alertas Automáticas**: AlertManager envía notificaciones a través de APIs a bots de Telegram, Discord y correo electrónico.

### Tecnologías Utilizadas

- **Prometheus**: Herramienta central para la recolección y almacenamiento de métricas.
- **AlertManager**: Sistema de gestión de alertas para Prometheus.
- **Grafana**: Plataforma de visualización y análisis de datos.
- **InfluxDB**: Base de datos de series temporales para el almacenamiento de métricas.
- **Django**: Framework web para el desarrollo del backend.
- **scikit-learn**: Biblioteca de aprendizaje automático para la implementación de modelos de IA.
- **cAdvisor, node_exporter, windows_exporter**: Exporters para la recolección de métricas de diversos sistemas.

### Simulaciones Realizadas

1. **Monitorización de Servidores Ubuntu**: Simulación de carga con stress-ng y alertas activadas por diferencias de carga mayores al 20%.
2. **Monitorización de Docker Engines**: Simulación de carga y alertas por superación de umbrales.
3. **Detección de Anomalías con IA**: Modelos de Isolation Forest para hosts y contenedores.
4. **Monitorización de Consumo Energético**: Comparación entre datos simulados y reales con un medidor de tensión ACS712 y una ESP32.

### Scripts y Configuraciones Adicionales

- **scripts/**: 
  - **tshark**: Scripts para capturas de tráfico de red.
  - **iperf3**: Scripts para pruebas de ancho de banda de red.
  - **stress-ng**: Scripts para generar carga de CPU y RAM.
  - **cron_jobs**: Configuraciones de tareas programadas para la ejecución automática de scripts.

- **telegram_api/**: Scripts para enviar notificaciones a un bot de Telegram.

### Instalación y Configuración

Para empezar con este proyecto, sigue los siguientes pasos:

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/mafortess/anomalyDetectionTFG.git
    ```

2. **Configurar y ejecutar Docker Compose**:
    ```bash
    cd docker
    docker-compose up -d
    ```

3. **Configurar Prometheus y AlertManager**:
    - Copiar `prometheus.yml` y `alertmanager.yml` a los directorios de configuración correspondientes.

4. **Desplegar la aplicación Django**:
    ```bash
    cd django_web
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    ```

5. **Configurar scripts y tareas cron**:
    - Instalar y configurar los scripts en la carpeta `scripts/`.
    - Configurar las tareas cron según las instrucciones en `scripts/cron_jobs.md`.

6. **Configurar el bot de Telegram**:
    - Configurar el script de la API de Telegram según las instrucciones en `telegram_api/telegram_bot.md`.

### Estado del Proyecto

Este proyecto está en una fase inicial y sirve como base para futuras ampliaciones y la incorporación de nuevas formas de monitorización y de otros sistemas.

### Contribuciones

Las contribuciones son bienvenidas. Por favor, lee las [normas de contribución](#) para más detalles.

### Licencia

Este proyecto está licenciado bajo la Licencia MIT. Mira el archivo [LICENSE](LICENSE) para más detalles.

### Contacto

Para cualquier consulta, por favor contacta a [tu nombre o tu email].
