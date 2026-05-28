from unittest.mock import patch, MagicMock
from app.services import user_service


class TestRegistrarUsuario:
    @patch('app.services.user_service.user_repo')
    def test_exitoso(self, mock_repo):
        mock_repo.obtener_usuario_por_nickname.return_value = None
        mock_repo.obtener_usuario_por_email.return_value = None
        mock_user = MagicMock()
        mock_repo.crear_usuario.return_value = mock_user

        resultado = user_service.registrar_usuario(
            nombre="Juan", apellido="Pérez",
            nickname="juanp", email="juan@gmail.com", contrasena="password123"
        )
        assert resultado == mock_user

    def test_nombre_vacio(self):
        resultado = user_service.registrar_usuario(
            nombre="", apellido="Pérez",
            nickname="juanp", email="juan@gmail.com", contrasena="password123"
        )
        assert resultado == "El nombre debe tener entre 1 y 50 caracteres"

    def test_apellido_vacio(self):
        resultado = user_service.registrar_usuario(
            nombre="Juan", apellido="",
            nickname="juanp", email="juan@gmail.com", contrasena="password123"
        )
        assert resultado == "El apellido debe tener entre 1 y 50 caracteres"

    def test_nickname_invalido(self):
        resultado = user_service.registrar_usuario(
            nombre="Juan", apellido="Pérez",
            nickname="j!", email="juan@gmail.com", contrasena="password123"
        )
        assert "nickname" in resultado

    def test_email_dominio_no_permitido(self):
        resultado = user_service.registrar_usuario(
            nombre="Juan", apellido="Pérez",
            nickname="juanp", email="juan@dominioinvalido.com", contrasena="password123"
        )
        assert resultado == "Solo se aceptan correos de Gmail, Hotmail, Outlook, Yahoo o iCloud"

    def test_contraseña_corta(self):
        resultado = user_service.registrar_usuario(
            nombre="Juan", apellido="Pérez",
            nickname="juanp", email="juan@gmail.com", contrasena="123"
        )
        assert resultado == "La contraseña debe tener un mínimo de 8 caracteres"

    @patch('app.services.user_service.user_repo')
    def test_nickname_duplicado(self, mock_repo):
        mock_repo.obtener_usuario_por_nickname.return_value = MagicMock()

        resultado = user_service.registrar_usuario(
            nombre="Juan", apellido="Pérez",
            nickname="juanp", email="juan@gmail.com", contrasena="password123"
        )
        assert resultado == "Ese nickname ya está en uso"

    @patch('app.services.user_service.user_repo')
    def test_email_duplicado(self, mock_repo):
        mock_repo.obtener_usuario_por_nickname.return_value = None
        mock_repo.obtener_usuario_por_email.return_value = MagicMock()

        resultado = user_service.registrar_usuario(
            nombre="Juan", apellido="Pérez",
            nickname="juanp", email="juan@gmail.com", contrasena="password123"
        )
        assert resultado == "Existe un usuario registrado con ese email"


class TestAutenticarUsuario:
    @patch('app.services.user_service.user_repo')
    def test_exitosa(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_repo.obtener_usuario_por_email.return_value = mock_user

        resultado = user_service.autenticar_usuario(email="juan@gmail.com", contrasena="password123")
        assert resultado == mock_user

    @patch('app.services.user_service.user_repo')
    def test_contraseña_incorrecta(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = False
        mock_repo.obtener_usuario_por_email.return_value = mock_user

        resultado = user_service.autenticar_usuario(email="juan@gmail.com", contrasena="wrongpass")
        assert resultado is None

    @patch('app.services.user_service.user_repo')
    def test_usuario_no_existe(self, mock_repo):
        mock_repo.obtener_usuario_por_email.return_value = None

        resultado = user_service.autenticar_usuario(email="noexiste@gmail.com", contrasena="password123")
        assert resultado is None


class TestCambiarContrasena:
    @patch('app.services.user_service.user_repo')
    def test_exitoso(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_repo.obtener_usuario_por_id.return_value = mock_user
        mock_updated = MagicMock()
        mock_repo.actualizar_usuario.return_value = mock_updated

        resultado = user_service.cambiar_contrasena(
            id_usuario=1,
            contrasena_actual="password123",
            contrasena_nueva="nuevaPassword456"
        )
        assert resultado == mock_updated

    @patch('app.services.user_service.user_repo')
    def test_usuario_no_encontrado(self, mock_repo):
        mock_repo.obtener_usuario_por_id.return_value = None

        resultado = user_service.cambiar_contrasena(
            id_usuario=999,
            contrasena_actual="password123",
            contrasena_nueva="nuevaPassword456"
        )
        assert resultado == "Usuario no encontrado"

    @patch('app.services.user_service.user_repo')
    def test_contraseña_actual_incorrecta(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = False
        mock_repo.obtener_usuario_por_id.return_value = mock_user

        resultado = user_service.cambiar_contrasena(
            id_usuario=1,
            contrasena_actual="wrongpass",
            contrasena_nueva="nuevaPassword456"
        )
        assert resultado == "La contraseña actual es incorrecta"

    @patch('app.services.user_service.user_repo')
    def test_nueva_igual_a_actual(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_repo.obtener_usuario_por_id.return_value = mock_user

        resultado = user_service.cambiar_contrasena(
            id_usuario=1,
            contrasena_actual="password123",
            contrasena_nueva="password123"
        )
        assert resultado == "La nueva contraseña debe ser diferente a la actual"

    @patch('app.services.user_service.user_repo')
    def test_nueva_contraseña_muy_corta(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_repo.obtener_usuario_por_id.return_value = mock_user

        resultado = user_service.cambiar_contrasena(
            id_usuario=1,
            contrasena_actual="password123",
            contrasena_nueva="123"
        )
        assert resultado == "La contraseña debe tener un mínimo de 8 caracteres"


class TestEliminarUsuario:
    @patch('app.services.user_service.user_repo')
    def test_exitoso(self, mock_repo):
        mock_repo.obtener_usuario_por_id.return_value = MagicMock()
        mock_repo.eliminar_usuario.return_value = True

        resultado = user_service.eliminar_usuario(id_usuario=1)
        assert resultado is True

    @patch('app.services.user_service.user_repo')
    def test_usuario_no_encontrado(self, mock_repo):
        mock_repo.obtener_usuario_por_id.return_value = None

        resultado = user_service.eliminar_usuario(id_usuario=999)
        assert resultado == "Usuario no encontrado"
