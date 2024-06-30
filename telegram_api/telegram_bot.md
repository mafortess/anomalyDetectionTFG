# Configuración del Bot de Telegram

## Obtener el Token del Bot

1. Abre Telegram y busca el bot llamado `BotFather`.

2. Inicia una conversación con `BotFather` y envía el comando `/newbot`.

3. Sigue las instrucciones para crear un nuevo bot. Recibirás un token de la API que será necesario para configurar tu bot.

## Configuración del Script del Bot

1. Abre el archivo del script del bot en la carpeta `telegram_api/`.

2. Configura el token de la API en el script:

    ```python
    # telegram_bot.py

    import telegram
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

    # Reemplaza 'YOUR_API_TOKEN' con tu token de la API
    API_TOKEN = 'YOUR_API_TOKEN'

    bot = telegram.Bot(token=API_TOKEN)
    updater = Updater(token=API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Definir comandos y manejadores aquí

    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy tu bot de Telegram.")

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    ```

3. Guarda el archivo y asegúrate de que tenga permisos de ejecución si es necesario:

    ```bash
    chmod +x telegram_bot.py
    ```

4. Ejecuta el script del bot para iniciar el bot:

    ```bash
    python3 telegram_bot.py
    ```

5. Verifica que el bot esté funcionando enviando el comando `/start` en Telegram al bot que has creado.

## Ejecutar el Bot como un Servicio

Para asegurarte de que el bot de Telegram esté siempre en funcionamiento, puedes configurarlo para que se ejecute como un servicio de sistema.

1. Crea un archivo de servicio de sistema:

    ```bash
    sudo nano /etc/systemd/system/telegram_bot.service
    ```

2. Añade la siguiente configuración al archivo:

    ```ini
    [Unit]
    Description=Bot de Telegram
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /ruta/a/telegram_api/telegram_bot.py
    WorkingDirectory=/ruta/a/telegram_api/
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    User=tu_usuario

    [Install]
    WantedBy=multi-user.target
    ```

    Asegúrate de reemplazar `/ruta/a/telegram_api/` con la ruta real a tu script y `tu_usuario` con tu nombre de usuario.

3. Guarda y cierra el archivo.

4. Recarga el demonio de systemd para aplicar los cambios:

    ```bash
    sudo systemctl daemon-reload
    ```

5. Inicia el servicio del bot de Telegram:

    ```bash
    sudo systemctl start telegram_bot.service
    ```

6. Habilita el servicio para que se inicie automáticamente al arrancar el sistema:

    ```bash
    sudo systemctl enable telegram_bot.service
    ```

Con estas instrucciones, deberías tener todo lo necesario para configurar las tareas cron y el bot de Telegram.
