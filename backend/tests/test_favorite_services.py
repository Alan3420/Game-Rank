from unittest.mock import patch, MagicMock
from app.services.favorite_services import (
    agregar_favorito,
    eliminar_favorito,
    es_favorito,
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
