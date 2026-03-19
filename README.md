
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

### Comandos que se utilizan siempre en docker
* Comando para crear y conectarse a la base de datos en docker:
    
        docker run -d --name game_rank_db -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=game_rank -p 3306:3306 mysql:8.0

* Comando para arrancar Vue
    1. npm run dev

    2. Si suceden problemas a la hora de arrancar el proyecto: 
        1. npm cache clean --force
        2. npm install
        3. npm run dev

