# Configuración de Tareas Cron

## Instalación de Scripts

1. Coloca todos los scripts necesarios en la carpeta `scripts/`.

2. Asegúrate de que los scripts tengan permisos de ejecución. Puedes hacerlo ejecutando el siguiente comando para cada script:

    ```bash
    chmod +x script_name.sh
    ```

## Configuración de Tareas Cron

1. Abre el archivo de configuración de cron para el usuario actual:

    ```bash
    crontab -e
    ```

2. Añade las siguientes líneas al archivo para programar la ejecución de los scripts:

    ```cron
    # Ejemplo de tarea cron para ejecutar un script cada hora
    0 * * * * /ruta/a/scripts/mi_script.sh >> /ruta/a/logs/mi_script.log 2>&1

    # Ejemplo de tarea cron para ejecutar un script diariamente a la medianoche
    0 0 * * * /ruta/a/scripts/otro_script.sh >> /ruta/a/logs/otro_script.log 2>&1
    ```

3. Guarda y cierra el archivo de configuración de cron.

4. Verifica que las tareas cron se hayan agregado correctamente:

    ```bash
    crontab -l
    ```

Asegúrate de reemplazar `/ruta/a/scripts/` con la ruta real donde están ubicados tus scripts, y `mi_script.sh` y `otro_script.sh` con los nombres reales de tus scripts.
