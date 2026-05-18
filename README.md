# Game Rank

Plataforma web para descubrir, valorar y organizar videojuegos. Los usuarios pueden explorar un catálogo extenso de juegos obtenido desde la API de RAWG, añadir juegos a favoritos, escribir comentarios, asignar valoraciones y gestionar su colección personal mediante estados de juego. El proyecto incluye un panel de administración para la gestión de usuarios y moderación de comentarios.

---

## Tecnologías

### Backend
| Tecnología | Versión |
|---|---|
| Python | 3.x |
| Flask | 3.1.3 |
| Flask-SQLAlchemy | 3.1.1 |
| Flask-JWT-Extended | 4.7.1 |
| Flask-Migrate | 4.1.0 |
| Flask-Limiter | 4.1.1 |
| Flask-CORS | 6.0.2 |
| PyMySQL | 1.1.2 |
| pytest | 9.0.3 |
| python-dotenv | 1.2.2 |

### Frontend
| Tecnología | Versión |
|---|---|
| Vue | 3.5.30 |
| Vite | 8.0 |
| Vue Router | 5.0.4 |
| PrimeVue | 4.5.5 |
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
        │   ├── Tendencias/
        │   └── User/
        ├── router/
        ├── services/
        ├── store/
        └── utils/
```

---

## Variables de entorno

Crea un archivo `.env` dentro de `backend/app/` con las siguientes variables:

```env
DB_URI=mysql+pymysql://usuario:contraseña@host:3306/game_rank
SECRET_KEY=tu_clave_secreta
RAWG_API_KEY=tu_api_key_de_rawg
FRONTEND_ORIGIN=http://localhost:5173
FLASK_DEBUG=true
```

| Variable | Descripción | Requerida |
|---|---|---|
| `DB_URI` | URI de conexión a MySQL | Sí |
| `SECRET_KEY` | Clave para JWT y sesiones Flask | Sí |
| `RAWG_API_KEY` | API key de RAWG para obtener datos de juegos | Sí |
| `FRONTEND_ORIGIN` | URL del frontend en producción | No |
| `FLASK_DEBUG` | Activa el modo debug de Flask (`true`/`false`) | No |

---

## Instalación y ejecución

### Prerrequisitos
- Python 3.x
- Node.js y npm
- MySQL corriendo con una base de datos llamada `game_rank`

### Backend

```bash
# Desde la carpeta backend/
pip install -r requirements.txt
```

Aplica las migraciones antes del primer arranque:
```bash
flask --app app.main db upgrade
```

Arranca el servidor:
```bash
python app/main.py
```

El backend queda disponible en `http://localhost:5000`.

### Frontend

```bash
# Desde la carpeta frontend/
npm install
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
# Desde la carpeta backend/

# Ejecutar solo los tests
python -m pytest tests/ -v

# Ejecutar con cobertura (recomendado)
python -m coverage run --source=app -m pytest

# Ver reporte de cobertura en consola
python -m coverage report

# Generar reporte HTML detallado (se crea en backend/htmlcov/index.html)
python -m coverage html
```

Los tests cubren los servicios principales: comentarios, valoraciones, favoritos, usuarios y estados de juego (43 tests en total).

---

## Migraciones de base de datos

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
