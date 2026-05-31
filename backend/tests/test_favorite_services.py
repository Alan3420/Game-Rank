from unittest.mock import patch, MagicMock
from app.services.favorite_services import (
    agregar_favorito,
    eliminar_favorito,
    es_favorito,
    actualizar_status,
    quitar_status,
    listar_favoritos_con_status,
    listar_favoritos_completos,
)


class TestAgregarFavorito:
    @patch('app.services.favorite_services.favorite_repo')
    def test_exitoso(self, mock_repo):
        mock_repo.obtener_favorito.return_value = None
        mock_fav = MagicMock()
        mock_repo.crear_favorito.return_value = mock_fav

        resultado = agregar_favorito(id_usuario=1, id_juego=100)
        assert resultado == mock_fav

    @patch('app.services.favorite_services.favorite_repo')
    def test_juego_ya_en_favoritos(self, mock_repo):
        mock_repo.obtener_favorito.return_value = MagicMock()

        resultado = agregar_favorito(id_usuario=1, id_juego=100)
        assert resultado == "El juego ya está en favoritos"

    @patch('app.services.favorite_services.favorite_repo')
    def test_status_invalido(self, mock_repo):
        mock_repo.obtener_favorito.return_value = None

        resultado = agregar_favorito(id_usuario=1, id_juego=100, status="inexistente")
        assert "status" in resultado.lower()
        mock_repo.crear_favorito.assert_not_called()


class TestEliminarFavorito:
    @patch('app.services.favorite_services.favorite_repo')
    def test_exitoso(self, mock_repo):
        mock_repo.obtener_favorito.return_value = MagicMock()
        mock_repo.eliminar_favorito.return_value = True

        resultado = eliminar_favorito(id_usuario=1, id_juego=100)
        assert resultado is True

    @patch('app.services.favorite_services.favorite_repo')
    def test_juego_no_en_favoritos(self, mock_repo):
        mock_repo.obtener_favorito.return_value = None

        resultado = eliminar_favorito(id_usuario=1, id_juego=100)
        assert resultado == "El juego no está en favoritos"


class TestEsFavorito:
    @patch('app.services.favorite_services.favorite_repo')
    def test_es_favorito(self, mock_repo):
        mock_repo.obtener_favorito.return_value = MagicMock()

        resultado = es_favorito(id_usuario=1, id_juego=100)
        assert resultado is True

    @patch('app.services.favorite_services.favorite_repo')
    def test_no_es_favorito(self, mock_repo):
        mock_repo.obtener_favorito.return_value = None

        resultado = es_favorito(id_usuario=1, id_juego=100)
        assert resultado is False


class TestActualizarStatus:
    @patch('app.services.favorite_services.favorite_repo')
    def test_status_valido(self, mock_repo):
        mock_fav = MagicMock()
        mock_repo.actualizar_status.return_value = mock_fav

        resultado = actualizar_status(id_usuario=1, id_juego=100, nuevo_status="jugando")
        assert resultado == mock_fav

    @patch('app.services.favorite_services.favorite_repo')
    def test_status_invalido(self, mock_repo):
        resultado = actualizar_status(id_usuario=1, id_juego=100, nuevo_status="inexistente")
        assert "status" in resultado.lower()
        mock_repo.actualizar_status.assert_not_called()

    @patch('app.services.favorite_services.favorite_repo')
    def test_favorito_no_existe(self, mock_repo):
        mock_repo.actualizar_status.return_value = None

        resultado = actualizar_status(id_usuario=1, id_juego=100, nuevo_status="jugando")
        assert resultado == "El juego no está en favoritos"


class TestQuitarStatus:
    @patch('app.services.favorite_services.favorite_repo')
    def test_exitoso(self, mock_repo):
        mock_fav = MagicMock()
        mock_fav.status = "jugando"
        mock_repo.obtener_favorito.return_value = mock_fav

        resultado = quitar_status(id_usuario=1, id_juego=100)

        assert resultado is True
        assert mock_fav.status is None

    @patch('app.services.favorite_services.favorite_repo')
    def test_favorito_no_existe(self, mock_repo):
        mock_repo.obtener_favorito.return_value = None

        resultado = quitar_status(id_usuario=1, id_juego=100)
        assert resultado == "El juego no está en favoritos"


class TestListarFavoritosConStatus:
    @patch('app.services.favorite_services.favorite_repo')
    def test_devuelve_solo_con_status(self, mock_repo):
        fav_con = MagicMock()
        fav_con.status = "jugando"
        fav_con.to_dict.return_value = {"id_game_api": 1, "status": "jugando"}

        fav_sin = MagicMock()
        fav_sin.status = None

        mock_repo.obtener_favoritos_por_usuario.return_value = [fav_con, fav_sin]

        resultado = listar_favoritos_con_status(id_usuario=1)
        assert len(resultado) == 1
        assert resultado[0]["status"] == "jugando"

    @patch('app.services.favorite_services.favorite_repo')
    def test_lista_vacia_si_ninguno_tiene_status(self, mock_repo):
        fav = MagicMock()
        fav.status = None
        mock_repo.obtener_favoritos_por_usuario.return_value = [fav]

        resultado = listar_favoritos_con_status(id_usuario=1)
        assert resultado == []


class TestListarFavoritosCompletos:
    @patch('app.services.favorite_services.get_game_by_id_api')
    @patch('app.services.favorite_services.formatear_resumen_juego')
    @patch('app.services.favorite_services.favorite_repo')
    def test_devuelve_juegos_con_status(self, mock_repo, mock_format, mock_api):
        fav = MagicMock()
        fav.status = "completado"
        fav.id_game_api = 3328
        mock_repo.obtener_favoritos_por_usuario.return_value = [fav]
        mock_api.return_value = {"id": 3328}
        mock_format.return_value = {"id": 3328, "name": "The Witcher 3"}

        resultado = listar_favoritos_completos(id_usuario=1)
        assert len(resultado) == 1
        assert resultado[0]["status"] == "completado"
        assert resultado[0]["game"]["name"] == "The Witcher 3"

    @patch('app.services.favorite_services.favorite_repo')
    def test_filtra_sin_status(self, mock_repo):
        fav = MagicMock()
        fav.status = None
        mock_repo.obtener_favoritos_por_usuario.return_value = [fav]

        resultado = listar_favoritos_completos(id_usuario=1)
        assert resultado == []
