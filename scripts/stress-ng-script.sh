#!/bin/bash

# Generar parámetros aleatorios para stress-ng
CPU_LOAD=$((RANDOM % 8 + 1))           # Número aleatorio entre 1 y 8 para la carga de CPU
VM_LOAD=$((RANDOM % 1024 + 512))       # Número aleatorio entre 512MB y 1536MB para la carga de RAM
IO_LOAD=$((RANDOM % 4 + 1))            # Número aleatorio entre 1 y 4 para la carga de disco
TIMEOUT=$((RANDOM % 120 + 30))         # Tiempo aleatorio entre 30 y 150 segundos

# Ejecutar stress-ng con los parámetros aleatorios
stress-ng --cpu $CPU_LOAD --vm 1 --vm-bytes ${VM_LOAD}M --hdd $IO_LOAD --timeout ${TIMEOUT}s
