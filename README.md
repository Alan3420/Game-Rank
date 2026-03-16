
# Fase 1 (Estructuracion del proyecto)

*   Organización del proyecto

        PROYECTO GAME-RANK/
        ├── backend/
        │   └── app/
        │       ├── database/
        │       ├── repositories/
        │       ├── models/
        │       ├── routes/
        │       └── services/
        └── frontend/
            ├── public/
            └── src/
                ├── assets/
                └── components/

* Extensiones extras en vsCode utilizadas:
    1. Mysql (Database Client)
    2. Docker
    3. Live Server 

* Comandos para inicializar el proyecto
    >Para arrancar el backend debes hacerlo desde la carpeta **/backend** y ejecutar el siguiente comando:

    1. python -m app.main

* Comandos que se utilizan siempre en docker

    1. `docker stop mi-mysql    # parar la base de datos`
    2. `docker start mi-mysql    # volver a arrancarla`
    3. `docker logs mi-mysql    # ver si hay errores`

    >Cada vez que inicies el proyecto ejecuta en la terminal `docker start mi-mysql `

