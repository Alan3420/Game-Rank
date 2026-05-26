from unittest.mock import patch, MagicMock
from app.services.rate_services import (
    crear_calificacion,
    actualizar_calificacion,
    eliminar_calificacion,
    obtener_promedio_del_juego,
)


class TestCrearCalificacion:
    @patch('app.services.rate_services.rate_repo')
    def test_exitosa(self, mock_repo):
        mock_repo.obtener_calificacion_por_usuario_y_juego.return_value = None
        mock_rate = MagicMock()
        mock_repo.crear_calificacion.return_value = mock_rate

        resultado = crear_calificacion(id_usuario=1, id_juego=100, valor=4)
        assert resultado == mock_rate

    def test_rating_negativo(self):
        resultado = crear_calificacion(id_usuario=1, id_juego=100, valor=-1)
        assert resultado == "La valoración debe ser un número entero entre 0 y 5"

    def test_rating_mayor_que_cinco(self):
        resultado = crear_calificacion(id_usuario=1, id_juego=100, valor=6)
        assert resultado == "La valoración debe ser un número entero entre 0 y 5"

    def test_rating_no_entero(self):
        resultado = crear_calificacion(id_usuario=1, id_juego=100, valor="cuatro")
        assert resultado == "La valoración debe ser un número entero entre 0 y 5"

    @patch('app.services.rate_services.rate_repo')
    def test_valoracion_duplicada(self, mock_repo):
        mock_repo.obtener_calificacion_por_usuario_y_juego.return_value = MagicMock()

        resultado = crear_calificacion(id_usuario=1, id_juego=100, valor=3)
        assert resultado == "Ya has valorado este juego"


class TestActualizarCalificacion:
    @patch('app.services.rate_services.rate_repo')
    def test_exitosa(self, mock_repo):
        mock_rate = MagicMock()
        mock_repo.actualizar_calificacion.return_value = mock_rate

        resultado = actualizar_calificacion(id_usuario=1, id_juego=100, valor=5)
        assert resultado == mock_rate

    @patch('app.services.rate_services.rate_repo')
    def test_valoracion_no_encontrada(self, mock_repo):
        mock_repo.actualizar_calificacion.return_value = None

        resultado = actualizar_calificacion(id_usuario=1, id_juego=100, valor=3)
        assert resultado == "Valoración no encontrada"

    def test_rating_invalido(self):
        resultado = actualizar_calificacion(id_usuario=1, id_juego=100, valor=10)
        assert resultado == "La valoración debe ser un número entero entre 0 y 5"


class TestEliminarCalificacion:
    @patch('app.services.rate_services.rate_repo')
    def test_exitosa(self, mock_repo):
        mock_repo.eliminar_calificacion.return_value = True

        resultado = eliminar_calificacion(id_usuario=1, id_juego=100)
        assert resultado is True

    @patch('app.services.rate_services.rate_repo')
    def test_valoracion_no_encontrada(self, mock_repo):
        mock_repo.eliminar_calificacion.return_value = None

        resultado = eliminar_calificacion(id_usuario=1, id_juego=100)
        assert resultado == "Valoración no encontrada"


class TestObtenerPromedioDelJuego:
    @patch('app.services.rate_services.rate_repo')
    def test_con_valoraciones(self, mock_repo):
        r1 = MagicMock()
        r1.rating = 4
        r2 = MagicMock()
        r2.rating = 2
        mock_repo.obtener_calificaciones_por_juego.return_value = [r1, r2]

        resultado = obtener_promedio_del_juego(id_juego=100)
        assert resultado == 3.0

    @patch('app.services.rate_services.rate_repo')
    def test_sin_valoraciones(self, mock_repo):
        mock_repo.obtener_calificaciones_por_juego.return_value = []

        resultado = obtener_promedio_del_juego(id_juego=100)
        assert resultado == 0.0
