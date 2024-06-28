#!/bin/bash

# Generar parámetros aleatorios para iperf3
PORT=$((RANDOM % 1000 + 5000))         # Puerto aleatorio entre 5000 y 6000
BANDWIDTH=$((RANDOM % 100 + 1))        # Ancho de banda aleatorio entre 1Mbps y 100Mbps
TIMEOUT=$((RANDOM % 120 + 30))         # Tiempo aleatorio entre 30 y 150 segundos

# Ejecutar iperf3 con los parámetros aleatorios
iperf3 -c iperf3-server -p $PORT -b ${BANDWIDTH}M -t $TIMEOUT
