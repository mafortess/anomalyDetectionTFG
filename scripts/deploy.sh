#!/bin/bash

#Si no se ejecuta este bash, usar comando "chmod +x ./app.sh" para otorgar permisos de ejecución

# Función para iniciar un servicio especificando la ruta y el nombre del ejecutable
start_service() {
    echo "Iniciando $2 en el puerto $3..."
    xterm -e "/bin/bash -c 'cd \"$1\" && ./$2; '" &
   #xterm -e "/bin/bash -c 'cd \"$1\" && ./\"$2\" 2> error_log.txt; read'" # SOLO DESCOMENTAR PARA DEBUG

    #Esperamos un breve momento para que el servicio intente iniciarse
    sleep 1

    # El servicio escribe en un archivo de log así que lo chequeamos
	echo "Probando puerto $3"
    if curl -s "http://localhost:$3" > /dev/null; then
    #if netstat -tulpen | grep ':$3' &> /dev/null; then
        echo "$2 iniciado correctamente."
    else
        echo "Fallo al iniciar $2."
    fi
	echo "--------------------------"
}

# Función para iniciar servicios que requieren systemctl
start_systemctl_service() {
    echo "Iniciando $1 en el puerto $2 ..."
    xterm -e "/bin/bash -c 'sudo systemctl start $1; '" &
    #xterm -e "/bin/bash -c 'sudo systemctl start \"$1\" 2> error_log.txt  echo 'Presione Enter para cerrar...'; read" # SOLO DESCOMENTAR PARA DEBUG
    sleep 4
  echo "Probando puerto $2"
    if curl -s "http://localhost:$2" > /dev/null; then
    #if netstat -tulpen | grep ':$2' &> /dev/null; then
        echo "$2 iniciado correctamente."
    	xterm -e "/bin/bash -c 'echo \"Finalizar Grafana con el comando sudo systemctl stop grafana-server: \"; exec /bin/bash '" &
    else
        echo "Fallo al iniciar $2."
    fi
	echo "--------------------------"
} 

start_python_app() {
    echo "Iniciando $2 en el puerto $3..."
#    xterm -e "/bin/bash  -c 'cd $1 && pip install -r requirements.txt && python $2; exec /bin/bash'" &
xterm -e "/bin/bash  -c 'cd $1 && python $2; exec /bin/bash'" &


sleep 4
    if curl -s "http://localhost:$3" > /dev/null; then
    #if netstat -tulpen | grep ':$3' &> /dev/null; then
        echo "$2 iniciado correctamente."
    else
        echo "Fallo al iniciar $2."
    fi
        echo "--------------------------"

}
# Función para abrir una URL en el navegador predeterminado
open_in_browser() {
    sleep 1
    echo "Abriendo $3 en el navegador..."
    xdg-open "$1:$2/$4" &> /dev/null
	#xdg-open
   # if [ $? -eq 0 ]; then #comprueba si el comando se ejecuto sin errores
	#if pgrep -x "chrome" > /dev/null; then #comprueba si el navegador responde o no
         #   echo "El navegador se abrió correctamente."
    	#else
         #   echo "Hubo un error al abrir el navegador."
	#fi
   # fi
}

start_cadvisor() {
    echo "Iniciando cAdvisor en el puerto $1 ..."
    # Verifica si el contenedor existe y está detenido
    if [ $(docker ps -q -a -f name=cadvisor) ]; then
        echo "cAdvisor existe pero está detenido. Iniciándolo..."
	docker start cadvisor
        sleep 1
	if curl -s "http://192.168.1.138:$1" > /dev/null; then
	    xterm -e "/bin/bash -c 'echo \"Finalizar CAdvisor con el comando docker stop cadvisor: \"; exec /bin/bash '" & 
            echo "$2 iniciado correctamente."
	    echo "--------------------------"
	fi
    elif [ ! $(docker ps -aq -f name=cadvisor) ]; then
        # Si el contenedor no existe, crea uno nuevo
        echo "Creando y ejecutando un nuevo contenedor..."
        # Ejecuta el contenedor cAdvisor
        docker run \
            --name=cadvisor \
            --volume=/:/rootfs:ro \
	    --volume=/var/run:/var/run:rw \
            --volume=/sys:/sys:ro \
            --volume=/var/lib/docker/:/var/lib/docker:ro \
            --publish=$1:8080 \
            --detach=true \
            --privileged=true \
            gcr.io/cadvisor/cadvisor:latest
        echo "$2 iniciado correctamente"
        xterm -e "/bin/bash -c 'echo \"Finalizar CAdvisor con el comando docker stop cadvisor: \"; exec /bin/bash '" &
	echo "-------------------------"
    else
        # Si el contenedor ya está en ejecución
        echo "El contenedor CAdvisor ya está en ejecución."
        echo "-------------------------"
    fi
}

# Iniciar cada servicio con su respectiva ruta
start_service node_exporter-1.8.1.linux-amd64 node_exporter 9100
#start_service pushgateway-1.8.0.linux-amd64 pushgateway 9091
start_service alertmanager-0.27.0.linux-amd64 alertmanager 9093
#start_service promlens-0.3.0.linux-amd64 promlens 8080
start_service prometheus-2.52.0.linux-amd64 prometheus 9090
start_cadvisor 8081
start_python_app alertmanager-0.27.0.linux-amd64 api.py 5001
start_systemctl_service grafana-server 3000
#start_service /ruta/a/tu_base_de_datos tu_base_de_datos 
echo "Todos los servicios han sido iniciados correctamente."

# Abrir interfaces web en el navegador
#open_in_browser http://192.168.1.138 9100 Node_Exporter  # node_exporter
sleep 1
#open_in_browser http://localhost 9091 Pushgateway # pushgateway 
#open_in_browser http://localhost 8080 Promlens # promlens 
open_in_browser http://localhost 9093 AlertManager # alertManager
open_in_browser http://localhost 9090 Prometheus /targets # Prometheus
#open_in_browser http://localhost 8081 CAdvisor #CAdvisor
open_in_browser http://localhost 3000 Grafana dashboards  # Grafana
