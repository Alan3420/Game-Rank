
# Organización del proyecto

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
            ├── src/
            │    ├── assets/
            │    ├── components/
            │    ├── router/
            │    ├── services/
            │    ├── view/
            │    ├── App.vue
            │    ├── main.js
            │    └── styles.css
            ├── index.html
            └── package.json

                

* Extensiones extras en vsCode utilizadas:
    1. Mysql (Database Client)
    2. Docker
    3. Live Server 

* Comandos para instalar dependencias:
    1. Para el back: `pip install -r requirements.txt`
    2. Para el front: `npm install`

* Comandos para hacer migraciones:
    1. Inicializar el sistema de migraciones: `flask --app app.main db init`
    2. Crear una nueva migración: `flask --app app.main db migrate -m "Mensaje de la migración"`
    3. Aplicar las migraciones a la base de datos: `flask --app app.main db upgrade`

### Comandos que se utilizan siempre en docker
* Comando para crear y conectarse a la base de datos en docker:
    
        docker run -d --name game_rank_db -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=game_rank -p 3306:3306 mysql:8.0

* Comando para arrancar Vue
    1. npm run dev

    2. Si suceden problemas a la hora de arrancar el proyecto: 
        1. npm cache clean --force
        2. npm install
        3. npm run dev

### Como arrancar el proyecto
* Depues de haber instalado las dependencias tanto de back `pip install -r requirements.txt` y front `npm install` y todo salio correctamente:

    1. Inicializar primero el back creando la BD e insertando datos inmediatamente (estando en la carpeta /backend): `flask --app app.main db-reset` luego `python -m app.main`

    2. Inicializar por ultimo el front que se conecta al back (estando en la carpeta /frontend): `npm run dev`

