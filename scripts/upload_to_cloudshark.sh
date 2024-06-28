#!/bin/bash

# Variables
HOST_IP=$(hostname -I | awk '{print $1}')
TIMESTAMP=$(date +%Y%m%d%H%M%S)
FILENAME="/tmp/capture_${HOST_IP}_${TIMESTAMP}.pcap"
API_KEY="c19b717398e4cbb2bc3b5d1fecd99770"
UPLOAD_URL="https://www.cloudshark.org/api/v1/$API_KEY/upload"

# Ejecutar tshark y guardar la captura
tshark -a duration:60 -w $FILENAME

# Subir la captura a CloudShark
curl -F "file=@${FILENAME}" $UPLOAD_URL    # Lo mismo que: curl -H "https://www.cloudshark.org/api/v1/?token=c19b717398e4cbb2bc3b5d1fecd99770/upload"

# Usando Token para autenticación
#curl -H "Authorization: Token c19b717398e4cbb2bc3b5d1fecd99770" -F "file=@${CAPTURE_DIR}/capture_${TIMESTAMP}.pcap" https://www.cloudshark.org/api/v1/upload -o /home/user/curl_response.txt
