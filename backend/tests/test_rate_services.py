from unittest.mock import patch, MagicMock
from app.services.rate_services import (
    crear_valoracion,
    actualizar_valoracion,
    eliminar_valoracion,
    get_media_juego,
)


class TestCrearValoracion:
    @patch('app.services.rate_services.create_rate')
    @patch('app.services.rate_services.get_rate_by_user_and_game')
    def test_exitosa(self, mock_get, mock_create):
        mock_get.return_value = None
        mock_rate = MagicMock()
        mock_create.return_value = mock_rate

        resultado = crear_valoracion(id_user=1, id_game=100, rating=4)
        assert resultado == mock_rate

    def test_rating_negativo(self):
        resultado = crear_valoracion(id_user=1, id_game=100, rating=-1)
        assert resultado == "La valoración debe ser un número entero entre 0 y 5"

    def test_rating_mayor_que_cinco(self):
        resultado = crear_valoracion(id_user=1, id_game=100, rating=6)
        assert resultado == "La valoración debe ser un número entero entre 0 y 5"

    def test_rating_no_entero(self):
        resultado = crear_valoracion(id_user=1, id_game=100, rating="cuatro")
        assert resultado == "La valoración debe ser un número entero entre 0 y 5"

    @patch('app.services.rate_services.get_rate_by_user_and_game')
    def test_valoracion_duplicada(self, mock_get):
        mock_get.return_value = MagicMock()

        resultado = crear_valoracion(id_user=1, id_game=100, rating=3)
        assert resultado == "Ya has valorado este juego"


class TestActualizarValoracion:
    @patch('app.services.rate_services.update_rate')
    def test_exitosa(self, mock_update):
        mock_rate = MagicMock()
        mock_update.return_value = mock_rate

        resultado = actualizar_valoracion(id_user=1, id_game=100, rating=5)
        assert resultado == mock_rate

    @patch('app.services.rate_services.update_rate')
    def test_valoracion_no_encontrada(self, mock_update):
        mock_update.return_value = None

        resultado = actualizar_valoracion(id_user=1, id_game=100, rating=3)
        assert resultado == "Valoración no encontrada"

    def test_rating_invalido(self):
        resultado = actualizar_valoracion(id_user=1, id_game=100, rating=10)
        assert resultado == "La valoración debe ser un número entero entre 0 y 5"


class TestEliminarValoracion:
    @patch('app.services.rate_services.delete_rate')
    def test_exitosa(self, mock_delete):
        mock_delete.return_value = True

        resultado = eliminar_valoracion(id_user=1, id_game=100)
        assert resultado is True

    @patch('app.services.rate_services.delete_rate')
    def test_valoracion_no_encontrada(self, mock_delete):
        mock_delete.return_value = None

        resultado = eliminar_valoracion(id_user=1, id_game=100)
        assert resultado == "Valoración no encontrada"


class TestGetMediaJuego:
    @patch('app.services.rate_services.get_rates_by_game')
    def test_con_valoraciones(self, mock_get):
        r1 = MagicMock()
        r1.rating = 4
        r2 = MagicMock()
        r2.rating = 2
        mock_get.return_value = [r1, r2]

        resultado = get_media_juego(id_game=100)
        assert resultado == 3.0

    @patch('app.services.rate_services.get_rates_by_game')
    def test_sin_valoraciones(self, mock_get):
        mock_get.return_value = []

        resultado = get_media_juego(id_game=100)
        assert resultado == 0.0
