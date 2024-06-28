FROM node:14

# Instalar dependencias de sistema
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
     tshark -y \
     nano \
    stress-ng \
    cron \
    iperf3 \
   # busybox-suid \
    && apt-get clean

# Crear directorio de la aplicación
WORKDIR /usr/src/app

# Copiar archivos de la aplicación
COPY package*.json ./

# Instalar dependencias de la aplicación
RUN npm install

# Copiar el resto de la aplicación
COPY . .

# Copiar los scripts
COPY upload_to_cloudshark.sh /usr/local/bin/upload_to_cloudshark.sh
COPY stress-ng-script.sh /usr/local/bin/stress-ng-script.sh
COPY iperf3_script.sh /usr/local/bin/iperf3_script.sh

# Copiar el archivo crontab al contenedor
COPY crontab /etc/cron.d/my-cron-jobs

# Dar permisos correctos al archivo crontab
RUN chmod 0644 /etc/cron.d/my-cron-jobs

# Registrar el archivo crontab
RUN crontab /etc/cron.d/my-cron-jobs

# Crear los directorios de logs
RUN mkdir -p /var/log
# Dar permisos de ejecución a los scripts
RUN chmod +x /usr/local/bin/upload_to_cloudshark.sh /usr/local/bin/stress-ng-script.sh /usr/local/bin/iperf3_script.sh

# Exponer el puerto de la aplicación
EXPOSE 3000

# Iniciar cron y la aplicación
CMD ["sh", "-c", "cron && npm start"]
