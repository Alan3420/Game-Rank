from app.database.db import db
from app.models.User import User


# Capa de acceso a datos para la tabla "users".
# Solo contiene queries; toda la logica de negocio y validaciones vive
# en app/services/user_service.py.


def obtener_todos_los_usuarios(excluir_id_usuario=None) -> list[User]:
    # Si recibimos un id a excluir, devolvemos todos los usuarios MENOS ese.
    # Lo usamos en el panel de admin para no mostrar al propio admin en la lista.
    if excluir_id_usuario:
        return User.query.filter(User.id_user != excluir_id_usuario).all()
    return User.query.all()


def obtener_usuario_por_id(id_usuario) -> User:
    return User.query.get(id_usuario)


def obtener_usuario_por_nickname(nickname) -> User:
    # ilike = case-insensitive, asi "JuanP" y "juanp" se consideran iguales
    # para que no se puedan registrar nicknames que solo difieran en mayusculas.
    return User.query.filter(User.nickname.ilike(nickname)).first()


def obtener_usuario_por_email(email) -> User:
    return User.query.filter_by(email=email).first()


def crear_usuario(nombre, apellido, nickname, email, contrasena) -> User:
    nuevo_usuario = User(
        name=nombre,
        last_name=apellido,
        nickname=nickname,
        email=email,
        password=contrasena
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario


def actualizar_usuario(id_usuario, nombre=None, apellido=None, nickname=None,
                       email=None, contrasena=None) -> User:
    # Todos los campos son opcionales. Solo actualizamos los que vengan
    # con valor; los demas se quedan como estaban.
    usuario = obtener_usuario_por_id(id_usuario)

    if usuario:
        if nombre:
            usuario.name = nombre
        if apellido:
            usuario.last_name = apellido
        if nickname:
            usuario.nickname = nickname
        if email:
            usuario.email = email
        if contrasena:
            # set_password hashea la contrasena antes de guardarla.
            usuario.set_password(contrasena)
        db.session.commit()

    return usuario


def eliminar_usuario(id_usuario) -> bool:
    # Antes de borrar el usuario quitamos sus datos relacionados.
    # Aunque las FK estan declaradas con ON DELETE CASCADE, lo hacemos
    # tambien aqui para asegurar la limpieza si el motor no respeta la
    # cascada (algunos drivers de MySQL en Flask-SQLAlchemy no la aplican).
    usuario = obtener_usuario_por_id(id_usuario)

    if usuario:
        from app.models.Favorite import Favorite
        from app.models.Comment import Comment
        from app.models.Rate import Rate

        db.session.query(Favorite).filter(Favorite.user_id == id_usuario).delete()
        db.session.query(Comment).filter(Comment.id_user == id_usuario).delete()
        db.session.query(Rate).filter(Rate.id_user == id_usuario).delete()

        db.session.delete(usuario)
        db.session.commit()
        return True

    return False


def actualizar_rol_de_usuario(id_usuario, nuevo_rol) -> User:
    # Solo aceptamos roles dentro de la lista blanca. Cualquier otro
    # valor se considera un intento invalido y lanza ValueError.
    ROLES_PERMITIDOS = ['user', 'admin']

    usuario = obtener_usuario_por_id(id_usuario)
    if usuario:
        if nuevo_rol in ROLES_PERMITIDOS:
            usuario.role = nuevo_rol
            db.session.commit()
        else:
            raise ValueError(
                f"Rol invalido: {nuevo_rol}. Roles permitidos: user, admin"
            )

    return usuario
