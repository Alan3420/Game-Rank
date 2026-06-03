# Game Rank

Plataforma web para descubrir, valorar y organizar videojuegos. Los usuarios pueden explorar un catálogo extenso de juegos obtenido desde la API de RAWG, añadir juegos a favoritos, escribir comentarios, asignar valoraciones y gestionar su colección personal mediante estados de juego. El proyecto incluye un panel de administración para la gestión de usuarios y moderación de comentarios.

Pagina web: https://gamerk.netlify.app/

---

## Tecnologías

### Backend
| Tecnología | Versión |
|---|---|
| Python | 3.13 |
| Flask | 3.1.3 |
| Flask-SQLAlchemy | 3.1.1 |
| SQLAlchemy | 2.0.48 |
| Flask-JWT-Extended | 4.7.1 |
| Flask-Migrate | 4.1.0 |
| Flask-Limiter | 4.1.1 |
| Flask-CORS | 6.0.2 |
| Werkzeug | 3.1.6 |
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
│   │   ├── autorizacion/
│   │   ├── client/
│   │   ├── database/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routes/
│   │   └── services/
│   ├── migrations/
│   └── tests/
└── frontend/
    └── src/
        ├── assets/
        ├── base/
        ├── components/
        │   ├── Admin/
        │   ├── Cards/
        │   ├── Content/
        │   ├── Filters/
        │   ├── GameDetail/
        │   ├── Home/
        │   ├── Image/
        │   ├── Legal/
        │   ├── Loader/
        │   ├── LoginRegister/
        │   ├── NotFound/
        │   ├── Notifications/
        │   ├── Pagination/
        │   ├── Tendencias/
        │   └── User/
        ├── router/
        ├── services/
        ├── store/
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
FLASK_DEBUG=true
```

| Variable | Descripción | Requerida |
|---|---|---|
| `DB_URI` | URI de conexión a MySQL. Formato: `mysql+pymysql://usuario:contraseña@host:puerto/nombre_bd` | Sí |
| `SECRET_KEY` | Clave arbitraria para firmar JWT y sesiones Flask. Usa una cadena larga y aleatoria. | Sí |
| `RAWG_API_KEY` | API key de RAWG. Obtenerla en [rawg.io/apidocs](https://rawg.io/apidocs) (registro gratuito). | Sí |
| `FRONTEND_ORIGIN` | URL del frontend en producción. En local no es necesaria. | No |
| `FLASK_DEBUG` | Activa el modo debug de Flask (`true`/`false`). Usar `false` en producción. | No |

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

**Paso 5 — Aplicar las migraciones** (crea las tablas en la BD):

```bash
flask --app app.main db upgrade
```

**Paso 6 — Cargar datos de prueba** (opcional):

```bash
flask --app app.main db-seed
```

**Paso 7 — Arrancar el servidor:**

```bash
python app.main.py
```

El backend queda disponible en `http://localhost:5000`.

> Si no ejecutas `db upgrade` antes del primer arranque, las rutas devolverán error porque las tablas no existen.

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

---

## Migraciones de base de datos

El proyecto utiliza Flask-Migrate para gestionar cambios en la estructura de la base de datos.

```bash
# Inicializar el sistema de migraciones (solo la primera vez)
flask --app app.main db init

# Crear una nueva migración
flask --app app.main db migrate -m "Descripción del cambio"

# Aplicar migraciones pendientes
flask --app app.main db upgrade
```

---

## Páginas disponibles

| Ruta | Acceso | Descripción |
|---|---|---|
| `/` | Público | Home con video de fondo dinámico |
| `/login` | Público | Inicio de sesión |
| `/register` | Público | Registro de usuario |
| `/terminos` | Público | Términos y condiciones |
| `/content/overview` | Autenticado | Catálogo de juegos con filtros |
| `/game/:id` | Autenticado | Detalle de juego |
| `/profile` | Autenticado | Perfil del usuario |
| `/tendencias` | Autenticado | Juegos en tendencia |
| `/admin/users` | Admin | Gestión de usuarios |
| `/admin/comments` | Admin | Moderación de comentarios |
