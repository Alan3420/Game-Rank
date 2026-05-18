from unittest.mock import patch, MagicMock
from app.services import user_service


class TestUserRegistration:
    @patch('app.services.user_service.user_repo')
    def test_exitoso(self, mock_repo):
        mock_repo.get_user_by_nickname.return_value = None
        mock_repo.get_user_by_email.return_value = None
        mock_user = MagicMock()
        mock_repo.create_user.return_value = mock_user

        resultado = user_service.user_registration(
            name="Juan", last_name="Pérez",
            nickname="juanp", email="juan@gmail.com", passwd="password123"
        )
        assert resultado == mock_user

    def test_nombre_vacio(self):
        resultado = user_service.user_registration(
            name="", last_name="Pérez",
            nickname="juanp", email="juan@gmail.com", passwd="password123"
        )
        assert resultado == "El nombre debe tener entre 1 y 50 caracteres"

    def test_apellido_vacio(self):
        resultado = user_service.user_registration(
            name="Juan", last_name="",
            nickname="juanp", email="juan@gmail.com", passwd="password123"
        )
        assert resultado == "El apellido debe tener entre 1 y 50 caracteres"

    def test_nickname_invalido(self):
        resultado = user_service.user_registration(
            name="Juan", last_name="Pérez",
            nickname="j!", email="juan@gmail.com", passwd="password123"
        )
        assert "nickname" in resultado

    def test_email_dominio_no_permitido(self):
        resultado = user_service.user_registration(
            name="Juan", last_name="Pérez",
            nickname="juanp", email="juan@dominioinvalido.com", passwd="password123"
        )
        assert resultado == "Solo se aceptan correos de Gmail, Hotmail, Outlook, Yahoo o iCloud"

    def test_contraseña_corta(self):
        resultado = user_service.user_registration(
            name="Juan", last_name="Pérez",
            nickname="juanp", email="juan@gmail.com", passwd="123"
        )
        assert resultado == "La contraseña debe tener un mínimo de 8 caracteres"

    @patch('app.services.user_service.user_repo')
    def test_nickname_duplicado(self, mock_repo):
        mock_repo.get_user_by_nickname.return_value = MagicMock()

        resultado = user_service.user_registration(
            name="Juan", last_name="Pérez",
            nickname="juanp", email="juan@gmail.com", passwd="password123"
        )
        assert resultado == "Ese nickname ya está en uso"

    @patch('app.services.user_service.user_repo')
    def test_email_duplicado(self, mock_repo):
        mock_repo.get_user_by_nickname.return_value = None
        mock_repo.get_user_by_email.return_value = MagicMock()

        resultado = user_service.user_registration(
            name="Juan", last_name="Pérez",
            nickname="juanp", email="juan@gmail.com", passwd="password123"
        )
        assert resultado == "Existe un usuario registrado con ese email"


class TestUserAuthentication:
    @patch('app.services.user_service.user_repo')
    def test_exitosa(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_repo.get_user_by_email.return_value = mock_user

        resultado = user_service.user_authentication(email="juan@gmail.com", passwd="password123")
        assert resultado == mock_user

    @patch('app.services.user_service.user_repo')
    def test_contraseña_incorrecta(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = False
        mock_repo.get_user_by_email.return_value = mock_user

        resultado = user_service.user_authentication(email="juan@gmail.com", passwd="wrongpass")
        assert resultado is None

    @patch('app.services.user_service.user_repo')
    def test_usuario_no_existe(self, mock_repo):
        mock_repo.get_user_by_email.return_value = None

        resultado = user_service.user_authentication(email="noexiste@gmail.com", passwd="password123")
        assert resultado is None


class TestChangePassword:
    @patch('app.services.user_service.user_repo')
    def test_exitoso(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_repo.get_user_by_id.return_value = mock_user
        mock_updated = MagicMock()
        mock_repo.update_user.return_value = mock_updated

        resultado = user_service.change_password(
            user_id=1,
            contraseña_actual="password123",
            contraseña_nueva="nuevaPassword456"
        )
        assert resultado == mock_updated

    @patch('app.services.user_service.user_repo')
    def test_usuario_no_encontrado(self, mock_repo):
        mock_repo.get_user_by_id.return_value = None

        resultado = user_service.change_password(
            user_id=999,
            contraseña_actual="password123",
            contraseña_nueva="nuevaPassword456"
        )
        assert resultado == "Usuario no encontrado"

    @patch('app.services.user_service.user_repo')
    def test_contraseña_actual_incorrecta(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = False
        mock_repo.get_user_by_id.return_value = mock_user

        resultado = user_service.change_password(
            user_id=1,
            contraseña_actual="wrongpass",
            contraseña_nueva="nuevaPassword456"
        )
        assert resultado == "La contraseña actual es incorrecta"

    @patch('app.services.user_service.user_repo')
    def test_nueva_igual_a_actual(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_repo.get_user_by_id.return_value = mock_user

        resultado = user_service.change_password(
            user_id=1,
            contraseña_actual="password123",
            contraseña_nueva="password123"
        )
        assert resultado == "La nueva contraseña debe ser diferente a la actual"

    @patch('app.services.user_service.user_repo')
    def test_nueva_contraseña_muy_corta(self, mock_repo):
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_repo.get_user_by_id.return_value = mock_user

        resultado = user_service.change_password(
            user_id=1,
            contraseña_actual="password123",
            contraseña_nueva="123"
        )
        assert resultado == "La contraseña debe tener un mínimo de 8 caracteres"


class TestUserDelete:
    @patch('app.services.user_service.user_repo')
    def test_exitoso(self, mock_repo):
        mock_repo.get_user_by_id.return_value = MagicMock()
        mock_repo.delete_user.return_value = True

        resultado = user_service.user_delete(user_id=1)
        assert resultado is True

    @patch('app.services.user_service.user_repo')
    def test_usuario_no_encontrado(self, mock_repo):
        mock_repo.get_user_by_id.return_value = None

        resultado = user_service.user_delete(user_id=999)
        assert resultado == "Usuario no encontrado"
