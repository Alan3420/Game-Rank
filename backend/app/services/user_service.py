from app.repositories import user_repo
from app.repositories.favorite_repo import contar_favoritos_por_usuario
from app.repositories.comment_repo import contar_comentarios_por_usuario
from app.repositories.rate_repo import obtener_calificaciones_por_usuario
from app.repositories.user_game_status_repo import obtener_conteo_estados_por_usuario
from app.models.User import User
import re


# Servicio que centraliza las validaciones y la logica de negocio de los
# usuarios. Las queries a la BD viven en user_repo.


# Lista blanca de dominios de correo aceptados. La replicamos en el frontend
# para que el usuario tenga el mismo aviso, pero la validacion seria vive aqui.
DOMINIOS_PERMITIDOS = {
    "gmail.com", "hotmail.com", "hotmail.es",
    "outlook.com", "outlook.es",
    "yahoo.com",  "yahoo.es",
    "icloud.com", "live.com",
}

# Expresion regular para nicknames: 3 a 30 caracteres, letras, numeros y
# guion bajo. Misma regla que el frontend.
_PATRON_NICKNAME = re.compile(r'^[a-zA-Z0-9_]{3,30}$')


def _dominio_valido(email: str) -> bool:
    # Comprueba que el email tenga formato "algo@dominio" y que el dominio
    # este en la lista blanca.
    partes = email.split("@")
    if len(partes) != 2:
        return False
    if partes[1].lower() in DOMINIOS_PERMITIDOS:
        return True
    return False


def _nickname_valido(nickname: str) -> bool:
    if _PATRON_NICKNAME.match(nickname):
        return True
    return False


def autenticar_usuario(email, contrasena) -> User | None:
    # Busca al usuario por email y comprueba la contrasena con bcrypt.
    # Devuelve el usuario si las credenciales son correctas, None si no.
    usuario = user_repo.obtener_usuario_por_email(email)

    if usuario and usuario.check_password(password=contrasena):
        return usuario

    return None


def registrar_usuario(nombre, apellido, nickname, email, contrasena) -> User | str:
    # Valida todos los campos uno a uno y, si todo es correcto, crea el
    # usuario. Si algo falla devuelve un string con el mensaje de error
    # (para que el route lo traduzca a una respuesta 409).

    if not nombre or len(nombre) < 1 or len(nombre) > 50:
        return "El nombre debe tener entre 1 y 50 caracteres"

    if not apellido or len(apellido) < 1 or len(apellido) > 50:
        return "El apellido debe tener entre 1 y 50 caracteres"

    if not nickname or not _nickname_valido(nickname):
        return "El nickname debe tener entre 3 y 30 caracteres y solo puede contener letras, números y guiones bajos"

    if not email or len(email) > 100:
        return "El email debe tener un máximo de 100 caracteres"

    if not _dominio_valido(email):
        return "Solo se aceptan correos de Gmail, Hotmail, Outlook, Yahoo o iCloud"

    if not contrasena or len(contrasena) < 8:
        return "La contraseña debe tener un mínimo de 8 caracteres"

    # Comprobamos unicidad de nickname y email antes de crear.
    if user_repo.obtener_usuario_por_nickname(nickname) is not None:
        return "Ese nickname ya está en uso"

    if user_repo.obtener_usuario_por_email(email) is not None:
        return "Existe un usuario registrado con ese email"

    nuevo_usuario = user_repo.crear_usuario(
        nombre=nombre,
        apellido=apellido,
        nickname=nickname,
        email=email,
        contrasena=contrasena
    )

    return nuevo_usuario


def obtener_lista_de_usuarios(excluir_id_usuario=None) -> list[User]:
    # Solo el admin la usa. Recibe el id del propio admin para que no
    # aparezca en la lista (por convencion del panel).
    return user_repo.obtener_todos_los_usuarios(excluir_id_usuario=excluir_id_usuario)


def actualizar_usuario(id_usuario, nombre, apellido, nickname, email, contrasena) -> User | str:
    # Reaplicamos las mismas reglas de validacion del registro, pero
    # adaptadas: aqui los campos son opcionales (solo se valida lo que
    # llega con valor).

    usuario = user_repo.obtener_usuario_por_id(id_usuario)

    if not usuario:
        return "Usuario no encontrado"

    if nombre and (len(nombre) < 1 or len(nombre) > 50):
        return "El nombre debe tener entre 1 y 50 caracteres"

    if apellido and (len(apellido) < 1 or len(apellido) > 50):
        return "El apellido debe tener entre 1 y 50 caracteres"

    if nickname:
        if not _nickname_valido(nickname):
            return "El nickname debe tener entre 3 y 30 caracteres y solo puede contener letras, números y guiones bajos"
        # Solo comprobamos unicidad si el nickname cambia (en mayus/minus
        # del usuario actual no cuenta como "cambio").
        nickname_actual = ""
        if usuario.nickname:
            nickname_actual = usuario.nickname.lower()
        if nickname.lower() != nickname_actual:
            if user_repo.obtener_usuario_por_nickname(nickname):
                return "Ese nickname ya está en uso"

    if email:
        if len(email) > 100:
            return "El email debe tener un máximo de 100 caracteres"
        if not _dominio_valido(email):
            return "Solo se aceptan correos de Gmail, Hotmail, Outlook, Yahoo o iCloud"
        if email != usuario.email:
            if user_repo.obtener_usuario_por_email(email):
                return "El correo electrónico ya está en uso por otro usuario"

    if contrasena and len(contrasena) < 8:
        return "La contraseña debe tener un mínimo de 8 caracteres"

    usuario_actualizado = user_repo.actualizar_usuario(
        id_usuario=id_usuario,
        nombre=nombre,
        apellido=apellido,
        nickname=nickname,
        email=email,
        contrasena=contrasena
    )

    return usuario_actualizado


def eliminar_usuario(id_usuario) -> bool | str:
    usuario = user_repo.obtener_usuario_por_id(id_usuario)

    if not usuario:
        return "Usuario no encontrado"

    resultado = user_repo.eliminar_usuario(id_usuario)
    return resultado


def cambiar_rol(id_usuario, nuevo_rol) -> User | str:
    # Solo el admin invoca esta funcion (lo refuerza el decorador
    # @admin_required de la ruta).
    usuario = user_repo.obtener_usuario_por_id(id_usuario)

    if not usuario:
        return "Usuario no encontrado"

    usuario_actualizado = user_repo.actualizar_rol_de_usuario(
        id_usuario=id_usuario,
        nuevo_rol=nuevo_rol
    )

    return usuario_actualizado


def obtener_usuario_por_id(id_usuario):
    # Wrapper para que las rutas no tengan que importar el repo directamente.
    return user_repo.obtener_usuario_por_id(id_usuario=id_usuario)


def cambiar_contrasena(id_usuario, contrasena_actual, contrasena_nueva) -> User | str:
    usuario = user_repo.obtener_usuario_por_id(id_usuario)

    if not usuario:
        return "Usuario no encontrado"

    # Comprobamos que la contrasena actual sea la correcta antes de cambiar.
    # Si no, podria pasar que alguien con la sesion abierta cambiara la
    # contrasena sin conocer la original.
    if not usuario.check_password(contrasena_actual):
        return "La contraseña actual es incorrecta"

    if len(contrasena_nueva) < 8:
        return "La contraseña debe tener un mínimo de 8 caracteres"

    if contrasena_actual == contrasena_nueva:
        return "La nueva contraseña debe ser diferente a la actual"

    usuario_actualizado = user_repo.actualizar_usuario(
        id_usuario=id_usuario,
        contrasena=contrasena_nueva
    )

    return usuario_actualizado


def obtener_estadisticas_usuario(id_usuario):
    # Estadisticas que pinta el perfil del usuario actual. Pedimos cada
    # pieza a su repo y armamos el dict final con la forma que espera
    # el frontend (no cambia respecto a la version anterior).

    estados = obtener_conteo_estados_por_usuario(id_usuario)
    estados_dict = {}
    for fila in estados:
        estados_dict[fila[0]] = fila[1]

    total_favoritos = contar_favoritos_por_usuario(id_usuario)
    total_comentarios = contar_comentarios_por_usuario(id_usuario)

    # Para la media nos basta con los valores de "rating". Pedimos la
    # lista entera al repo (devuelve modelos Rate) y la promediamos aqui.
    calificaciones = obtener_calificaciones_por_usuario(id_usuario)
    valores = []
    for calificacion in calificaciones:
        valores.append(calificacion.rating)

    rating_medio = None
    if valores:
        rating_medio = round(sum(valores) / len(valores), 1)

    return {
        "coleccion": {
            "total":      sum(estados_dict.values()),
            "completado": estados_dict.get("completado", 0),
            "jugando":    estados_dict.get("jugando", 0),
            "pendiente":  estados_dict.get("pendiente", 0),
            "pausado":    estados_dict.get("pausado", 0)
        },
        "favoritos":    total_favoritos,
        "comentarios":  total_comentarios,
        "valoraciones": len(valores),
        "rating_medio": rating_medio
    }
