from unittest.mock import patch, MagicMock
from app.services.user_game_status_service import (
    establecer_status,
    quitar_status,
    obtener_status_juego,
)


class TestEstablecerStatus:
    @patch('app.services.user_game_status_service.crear_status')
    @patch('app.services.user_game_status_service.obtener_status')
    def test_crea_status_nuevo(self, mock_get, mock_create):
        mock_get.return_value = None
        mock_status = MagicMock()
        mock_create.return_value = mock_status

        resultado = establecer_status(id_user=1, id_game=100, status="jugando")
        assert resultado == mock_status

    @patch('app.services.user_game_status_service.actualizar_status')
    @patch('app.services.user_game_status_service.obtener_status')
    def test_actualiza_status_existente(self, mock_get, mock_update):
        mock_get.return_value = MagicMock()
        mock_updated = MagicMock()
        mock_update.return_value = mock_updated

        resultado = establecer_status(id_user=1, id_game=100, status="completado")
        assert resultado == mock_updated

    def test_status_invalido(self):
        resultado = establecer_status(id_user=1, id_game=100, status="invalido")
        assert isinstance(resultado, str)
        assert "El status debe ser uno de" in resultado

    @patch('app.services.user_game_status_service.crear_status')
    @patch('app.services.user_game_status_service.obtener_status')
    def test_todos_los_status_validos(self, mock_get, mock_create):
        mock_get.return_value = None
        mock_create.return_value = MagicMock()

        for status in ["pendiente", "pausado", "jugando", "completado"]:
            resultado = establecer_status(id_user=1, id_game=100, status=status)
            assert not isinstance(resultado, str)


class TestQuitarStatus:
    @patch('app.services.user_game_status_service.eliminar_status')
    def test_exitoso(self, mock_delete):
        mock_delete.return_value = True

        resultado = quitar_status(id_user=1, id_game=100)
        assert resultado is True

    @patch('app.services.user_game_status_service.eliminar_status')
    def test_status_no_encontrado(self, mock_delete):
        mock_delete.return_value = None

        resultado = quitar_status(id_user=1, id_game=100)
        assert resultado == "Status no encontrado"


class TestObtenerStatusJuego:
    @patch('app.services.user_game_status_service.obtener_status')
    def test_retorna_status_existente(self, mock_get):
        mock_status = MagicMock()
        mock_get.return_value = mock_status

        resultado = obtener_status_juego(id_user=1, id_game=100)
        assert resultado == mock_status

    @patch('app.services.user_game_status_service.obtener_status')
    def test_retorna_none_si_no_existe(self, mock_get):
        mock_get.return_value = None

        resultado = obtener_status_juego(id_user=1, id_game=100)
        assert resultado is None
