# Game Rank

Plataforma web para descubrir, valorar y organizar videojuegos. Los usuarios pueden explorar un catálogo extenso de juegos obtenido desde la API de RAWG, añadir juegos a favoritos, escribir comentarios, asignar valoraciones y gestionar su colección personal mediante estados de juego. El proyecto incluye un panel de administración para la gestión de usuarios y moderación de comentarios.

Pagina web: https://game-rank-2h1.pages.dev/

---

## Tecnologías

### Backend
| Tecnología | Versión |
|---|---|
| Python | 3.13 |
| FastAPI | 0.142.2 |
| Uvicorn | 0.54.0 |
| Pydantic | 2.13.5 |
| SQLAlchemy | 2.0.48 |
| Alembic | 1.18.4 |
| PyJWT | 2.12.1 |
| SlowAPI | 0.1.10 |
| Werkzeug (hash de contraseñas) | 3.1.6 |
| PyMySQL | 1.1.2 |
| pytest | 9.0.3 |
| python-dotenv | 1.2.2 |

### Frontend
| Tecnología | Versión |
|---|---|
| Vue | 3.5.30 |
| Vite | 8.0.0 |
| Vue Router | 5.0.4 |
| PrimeVue | 4.5.5 |
| PrimeIcons | 7.0.0 |
| Axios | 1.15.2 |
| DOMPurify | 3.4.3 |

### Base de datos
- MySQL

### API externa
- [RAWG Video Games Database](https://rawg.io/apidocs)

---

## Organización del proyecto

```
Game-Rank/
├── README.md
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── main.py            # aplicación FastAPI (middlewares, CORS, routers)
│   │   ├── cli.py             # crear-tablas y seed
│   │   ├── api/
│   │   │   ├── routers/       # endpoints: acceso, contenido, cuenta, comentarios, favoritos, tendencias
│   │   │   ├── esquemas.py    # cuerpos de las peticiones (Pydantic)
│   │   │   ├── seguridad.py   # tokens JWT y permisos de admin
│   │   │   ├── limites.py     # límite de peticiones (SlowAPI)
│   │   │   └── respuestas.py  # formato JSON de las respuestas
│   │   ├── client/            # cliente de RAWG con caché
│   │   ├── database/          # motor, sesión y seed (SQLAlchemy)
│   │   ├── models/
│   │   ├── repositories/
│   │   └── services/
│   ├── migrations/            # Alembic
│   ├── tests/                 # tests unitarios de servicios
│   └── tests_contrato/        # tests de contrato de la API
└── frontend/
    └── src/
        ├── assets/            # imágenes; brand/ con el logo y sus variantes
        ├── base/              # App.vue: cabecera, menú y pie
        ├── components/
        │   ├── Admin/
        │   ├── CardWorld/     # MiniCard e iconos de estado (StatusIcon)
        │   ├── Cards/         # menú de estado
        │   ├── Confirm/
        │   ├── Content/       # catálogo
        │   ├── Filters/
        │   ├── GameDetail/
        │   ├── Home/
        │   ├── Image/
        │   ├── Legal/
        │   ├── LoginRegister/
        │   ├── NotFound/
        │   ├── Notifications/
        │   ├── Pagination/
        │   ├── Skeleton/
        │   ├── Tendencias/
        │   └── User/          # perfil
        ├── router/
        ├── services/
        ├── store/
        ├── styles/            # card-world.css: tokens del sistema de diseño
        └── utils/
```

---

## Variables de entorno

El backend necesita un archivo `.env` para funcionar. Sin él, el servidor no arranca.

**Ubicación exacta:** `backend/app/.env`

```
Game-Rank/
└── backend/
    └── app/
        └── .env
```

Crea el archivo con el siguiente contenido y rellena cada valor:

```env
DB_URI=mysql+pymysql://usuario:contraseña@host:3306/game_rank
SECRET_KEY=tu_clave_secreta
RAWG_API_KEY=tu_api_key_de_rawg
FRONTEND_ORIGIN=http://localhost:5173
RECARGA=true
```

| Variable | Descripción | Requerida |
|---|---|---|
| `DB_URI` | URI de conexión a MySQL. Formato: `mysql+pymysql://usuario:contraseña@host:puerto/nombre_bd` | Sí |
| `SECRET_KEY` | Clave para firmar los tokens JWT. Usa una cadena larga y aleatoria. | Sí |
| `RAWG_API_KEY` | API key de RAWG. Obtenerla en [rawg.io/apidocs](https://rawg.io/apidocs) (registro gratuito). | Sí |
| `FRONTEND_ORIGIN` | URL del frontend en producción. En local no es necesaria. | No |
| `RECARGA` | Reinicia el servidor al guardar cambios al arrancar con `python -m app.main` (`true`/`false`). Solo para desarrollo. | No |
| `MOSTRAR_DOCS` | Publica la documentación interactiva de la API en `/docs` y `/redoc` (`true` por defecto; `false` para ocultarla). | No |
| `PORT` / `WEB_CONCURRENCY` | Puerto y número de workers de uvicorn en el contenedor (por defecto 5000 y 2). | No |
| `DB_SSL` | Fuerza (`true`) o desactiva (`false`) el certificado `ca.pem` en la conexión a MySQL. Sin ella se usa solo con servidores remotos como Aiven. | No |

El archivo `.env` está en `.gitignore` y nunca debe subirse al repositorio.

---

## Instalación y ejecución

### Prerrequisitos
- Python 3.13
- Node.js 18 o superior y npm
- MySQL con una base de datos creada llamada `game_rank`
- API key de RAWG (ver Variables de entorno)

### Backend

Desde la carpeta `backend/`:

> **Importante:** antes de instalar las dependencias debes crear un entorno virtual. Si instalas todo directamente en el sistema Python global puedes romper otras herramientas instaladas y tendrás conflictos de versiones. No te saltes este paso.

**Paso 1 — Crear el entorno virtual** (solo la primera vez):

```bash
python -m venv .venv
```

Esto crea una carpeta `.venv/` dentro de `backend/`. Ahí se instalarán todas las dependencias del proyecto de forma aislada.

**Paso 2 — Activar el entorno virtual** (cada vez que abras una terminal nueva):

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Sabrás que está activo porque el prompt de la terminal mostrará `(.venv)` al principio.

**Paso 3 — Instalar dependencias:**

```bash
pip install -r requirements.txt
```

**Paso 4 — Crear `backend/app/.env`** con las variables de entorno (ver sección anterior). Sin este archivo el servidor no arranca.

**Paso 5 — Crear las tablas.**

En una base que ya existe (por ejemplo la de producción), aplica las migraciones pendientes:

```bash
alembic -c migrations/alembic.ini upgrade head
```

En una base **nueva y vacía** crea el esquema desde los modelos y márcalo como actualizado. La cadena histórica de migraciones no se puede aplicar desde cero: la migración `2008b9a14636` falla en MySQL 8 con un error de columna autoincremental, y ya fallaba igual con Flask-Migrate.

```bash
python -m app.cli crear-tablas
alembic -c migrations/alembic.ini stamp head
```

**Paso 6 — Cargar datos de prueba** (opcional):

```bash
python -m app.cli seed
```

**Paso 7 — Arrancar el servidor:**

```bash
python -m app.main
```

El backend queda disponible en `http://localhost:5000` y la documentación interactiva de la API en `http://localhost:5000/docs`.

> Si no aplicas las migraciones antes del primer arranque, las rutas devolverán error porque las tablas no existen.

### Frontend

Desde la carpeta `frontend/`:

```bash
# 1. Instalar dependencias
npm install

# 2. Arrancar el servidor de desarrollo
npm run dev
```

El frontend queda disponible en `http://localhost:5173`.

Si encuentras problemas al arrancar:

```bash
npm cache clean --force
npm install
npm run dev
```

---

## Tests unitarios

Ejecuta los tests antes de arrancar el backend para verificar que todo funciona correctamente:

```bash
# Desde la carpeta backend/ (con el entorno virtual activo)

# Ejecutar solo los tests
python -m pytest tests/ -v

# Ejecutar con cobertura (recomendado)
python -m coverage run --source=app -m pytest

# Ver reporte de cobertura en consola
python -m coverage report

# Generar reporte HTML detallado (se crea en backend/htmlcov/index.html)
python -m coverage html
```

Los tests cubren los servicios principales: comentarios, favoritos y usuarios (48 tests en total).

### Tests de contrato de la API

`backend/tests_contrato/` recorre las 35 rutas con una base SQLite temporal y RAWG simulado, y compara cada respuesta (código, cuerpo y formato de fechas) con las referencias de `tests_contrato/referencias/`, grabadas desde la versión Flask antes de migrar a FastAPI. Garantizan que el frontend recibe exactamente lo mismo.

```bash
# SQLite temporal (no toca ninguna base real)
python -m pytest tests_contrato -q

# Contra MySQL (por ejemplo, el contenedor de docker-compose)
CONTRATO_DB_URI=mysql+pymysql://root:rootpassword@localhost:3307/game_rank python -m pytest tests_contrato -q
```

Si un cambio de la API es intencionado, las referencias se regraban con `CONTRATO_GRABAR=1`.

---

## Migraciones de base de datos

El proyecto utiliza Alembic para gestionar cambios en la estructura de la base de datos.

```bash
# Crear una nueva migración a partir de los modelos
alembic -c migrations/alembic.ini revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones pendientes
alembic -c migrations/alembic.ini upgrade head

# Ver la versión aplicada
alembic -c migrations/alembic.ini current
```

---

## Despliegue

| Parte | Dónde | URL |
|---|---|---|
| Frontend | Cloudflare Pages (proyecto `game-rank`) | https://game-rank-2h1.pages.dev |
| Backend | Google Cloud Run (`game-rank-api`, región `europe-west4`, junto a la base de Aiven en Ámsterdam) | https://game-rank-api-931293666046.europe-west4.run.app |
| Base de datos | Aiven MySQL | — |

### Backend (Cloud Run)

Requisitos: [Google Cloud SDK](https://cloud.google.com/sdk) con sesión iniciada (`gcloud auth login`) y el proyecto activo (`gcloud config set project game-rank-91173`).

```powershell
# desde backend/
powershell -ExecutionPolicy Bypass -File scripts\desplegar-cloudrun.ps1
```

El script lee `DB_URI`, `SECRET_KEY` y `RAWG_API_KEY` de `backend/app/.env` (nunca se suben al repositorio; `.gcloudignore` también los excluye), construye la imagen con el `Dockerfile` y la publica. Cloud Run escala a cero sin tráfico: la primera petición tras un rato sin uso tarda unos segundos en arrancar el contenedor. Para que no se apague nunca: `gcloud run services update game-rank-api --region europe-west4 --min-instances 1` (tiene coste).

- **Variables opcionales:** `FRONTEND_ORIGIN` (orígenes permitidos por CORS, separados por comas), `MOSTRAR_DOCS=false` para ocultar `/docs`, `WEB_CONCURRENCY` (workers de uvicorn).
- **Base de datos:** con Aiven se usa el certificado `backend/app/ca.pem` automáticamente; con una MySQL local (por ejemplo la del `docker-compose`) no. `DB_SSL=true|false` lo fuerza.
- **Sesiones:** los tokens emitidos por la versión anterior (Flask) siguen siendo válidos, así que desplegar no cierra la sesión de nadie.

### Frontend (Cloudflare Pages)

La URL del backend está en `frontend/.env.production` (`VITE_API_URL`). Desde `frontend/`:

```bash
pnpm deploy
```

Compila con Vite y publica `dist` con `wrangler pages deploy` (la primera vez pide iniciar sesión en Cloudflare). Las rutas de la SPA (`/game/123`, `/terminos`...) funcionan al recargar sin configuración extra.

### Local con Docker

Con `docker-compose up` se levantan juntos MySQL y el backend en `http://localhost:5000`.

---

## Páginas disponibles

| Ruta | Acceso | Descripción |
|---|---|---|
| `/` | Público | Home. Invitado: tráiler de un juego y prueba de los estados. Con sesión: Discover (juegos que aún no tienes), resumen del álbum, listas del año y del mes, tendencias y próximos lanzamientos |
| `/login` | Público | Inicio de sesión |
| `/register` | Público | Registro de usuario |
| `/terminos` | Público | Términos y condiciones |
| `/content/overview` | Autenticado | Catálogo de juegos con filtros |
| `/game/:id` | Autenticado | Detalle de juego |
| `/profile` | Autenticado | Perfil del usuario |
| `/tendencias` | Autenticado | Juegos en tendencia |
| `/admin/users` | Admin | Gestión de usuarios |
| `/admin/comments` | Admin | Moderación de comentarios |
