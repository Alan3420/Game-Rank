from unittest.mock import patch, MagicMock
from app.services.favorite_services import (
    añadir_favorito,
    eliminar_favorito,
    es_favorito,
)


class TestAñadirFavorito:
    @patch('app.services.favorite_services.create_favorite')
    @patch('app.services.favorite_services.get_favorite')
    def test_exitoso(self, mock_get, mock_create):
        mock_get.return_value = None
        mock_fav = MagicMock()
        mock_create.return_value = mock_fav

        resultado = añadir_favorito(id_user=1, id_game=100)
        assert resultado == mock_fav

    @patch('app.services.favorite_services.get_favorite')
    def test_juego_ya_en_favoritos(self, mock_get):
        mock_get.return_value = MagicMock()

        resultado = añadir_favorito(id_user=1, id_game=100)
        assert resultado == "El juego ya está en favoritos"


class TestEliminarFavorito:
    @patch('app.services.favorite_services.delete_favorite')
    @patch('app.services.favorite_services.get_favorite')
    def test_exitoso(self, mock_get, mock_delete):
        mock_get.return_value = MagicMock()
        mock_delete.return_value = True

        resultado = eliminar_favorito(id_user=1, id_game=100)
        assert resultado is True

    @patch('app.services.favorite_services.get_favorite')
    def test_juego_no_en_favoritos(self, mock_get):
        mock_get.return_value = None

        resultado = eliminar_favorito(id_user=1, id_game=100)
        assert resultado == "El juego no está en favoritos"


class TestEsFavorito:
    @patch('app.services.favorite_services.get_favorite')
    def test_es_favorito(self, mock_get):
        mock_get.return_value = MagicMock()

        resultado = es_favorito(id_user=1, id_game=100)
        assert resultado is True

    @patch('app.services.favorite_services.get_favorite')
    def test_no_es_favorito(self, mock_get):
        mock_get.return_value = None

        resultado = es_favorito(id_user=1, id_game=100)
        assert resultado is False
