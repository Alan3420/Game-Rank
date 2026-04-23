
# Organización del proyecto

        PROYECTO GAME-RANK/
        ├── README.md
        ├── backend/
        │   
        │   ├── app/
        │   │   ├── database/
        │   │   ├── repositories/
        │   │   ├── models/
        │   │   ├── routes/
        │   │   └── services/
        │   ├── requirements.txt
        │   └── migrations/
        └── frontend/
            ├── package.json
            ├── public/
            ├── src/
            │   ├── assets/
            │   ├── components/
            │   │   ├── Content/
            │   │   ├── GameDetail/
            │   │   ├── Home/
            │   │   ├── LoginRegister/
            │   │   └── User/
            │   ├── router/
            │   │   └── index.js
            │   ├── services/
            │   └── store/

                

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

### Actualmente en desuso
```
    ### Comandos que se utilizan siempre en docker
    * Comando para crear y conectarse a la base de datos en docker:
        
        docker run -d --name game_rank_db -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=game_rank -p 3306:3306 mysql:8.0
```

* Comando para arrancar Vue
    1. npm run dev

    2. Si suceden problemas a la hora de arrancar el proyecto: 
        1. npm cache clean --force
        2. npm install
        3. npm run dev

### Como arrancar el proyecto

Antes de iniciar el proyecto, asegúrate de tener instaladas las dependencias necesarias. El proyecto puede ejecutarse de dos formas: utilizando Docker (recomendado) o de forma manual.

#### Prerrequisitos
- **Docker y Docker Compose**: Para ejecutar con contenedores (versión recomendada).
- **Python 3.x**: Para el backend (si se ejecuta manualmente).
- **Node.js y npm**: Para el frontend.
- **MySQL**: Base de datos (si se ejecuta manualmente, o se puede usar el contenedor de Docker).

#### Opción 1: Usando Docker (No se esta utilizando actualmente, pero se recomienda para evitar problemas de configuración)
Esta opción configura automáticamente el backend, frontend y la base de datos MySQL en contenedores.

1. Asegúrate de tener Docker y Docker Compose instalados.
2. Desde la raíz del proyecto, ejecuta:
   ```
   docker-compose up --build
   ```
3. El backend estará disponible en `http://localhost:8080` y el frontend en el puerto configurado por Vite (generalmente `http://localhost:5173`).

#### Opción 2: Ejecución Manual
Si prefieres ejecutar los servicios manualmente:

1. **Instalar dependencias**:
   - Para el backend (desde la carpeta `/backend`): `pip install -r requirements.txt`
   - Para el frontend (desde la carpeta `/frontend`): `npm install`

2. **Configurar la base de datos**:
   - Asegúrate de tener MySQL corriendo. Crea una base de datos llamada `game_rank` con usuario `root` y contraseña `root`.
   - O usa el comando Docker deprecated mencionado abajo para crear un contenedor MySQL.

3. **Iniciar el backend**:
   - Ve a la carpeta `/backend`.
   - Si la base de datos no está creada, ejecuta: `flask --app app.main db upgrade` para aplicar las migraciones.
   - Luego inicia el servidor: `python -m app.main`
   - El backend correrá en `http://localhost:8080`.

4. **Iniciar el frontend**:
   - Ve a la carpeta `/frontend`.
   - Ejecuta: `npm run dev`
   - El frontend estará disponible en `http://localhost:5173` (o el puerto que indique Vite).

Si encuentras problemas al iniciar el frontend, intenta:
- `npm cache clean --force`
- `npm install`
- `npm run dev`

