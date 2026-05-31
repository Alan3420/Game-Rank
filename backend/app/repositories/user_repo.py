from app.database.db import db
from app.models.User import User


def obtener_todos_los_usuarios(excluir_id_usuario=None) -> list[User]:
    if excluir_id_usuario:
        return User.query.filter(User.id_user != excluir_id_usuario).all()
    return User.query.all()


def obtener_usuario_por_id(id_usuario) -> User:
    return User.query.get(id_usuario)


def obtener_usuario_por_nickname(nickname) -> User:
    # ilike es case-insensitive, asi "JuanP" y "juanp" cuentan como el mismo
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
            usuario.set_password(contrasena)
        db.session.commit()

    return usuario


def eliminar_usuario(id_usuario) -> bool:
    # Borramos a mano los datos relacionados porque algunos drivers de MySQL
    # con Flask-SQLAlchemy no aplican el ON DELETE CASCADE de las FK
    usuario = obtener_usuario_por_id(id_usuario)

    if usuario:
        from app.models.Comment import Comment
        from app.models.AddFavorite import AddFavorite
        from app.models.Favorite import Favorite

        fav_ids = []
        for row in db.session.query(AddFavorite.fav_id).filter(AddFavorite.id_user == id_usuario).all():
            fav_ids.append(row.fav_id)

        db.session.query(Comment).filter(Comment.id_user == id_usuario).delete()
        db.session.query(AddFavorite).filter(AddFavorite.id_user == id_usuario).delete()

        if fav_ids:
            db.session.query(Favorite).filter(
                Favorite.fav_id.in_(fav_ids)
            ).delete(synchronize_session='fetch')

        db.session.delete(usuario)
        db.session.commit()
        return True

    return False


def actualizar_rol_de_usuario(id_usuario, nuevo_rol) -> User:
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
