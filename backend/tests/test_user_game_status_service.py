from unittest.mock import patch, MagicMock
from app.services.user_game_status_service import (
    establecer_estado,
    quitar_estado,
    obtener_estado_del_juego,
)


class TestEstablecerEstado:
    @patch('app.services.user_game_status_service.user_game_status_repo')
    def test_crea_estado_nuevo(self, mock_repo):
        mock_repo.obtener_estado.return_value = None
        mock_estado = MagicMock()
        mock_repo.crear_estado.return_value = mock_estado

        resultado = establecer_estado(id_usuario=1, id_juego=100, estado="jugando")
        assert resultado == mock_estado

    @patch('app.services.user_game_status_service.user_game_status_repo')
    def test_actualiza_estado_existente(self, mock_repo):
        mock_repo.obtener_estado.return_value = MagicMock()
        mock_actualizado = MagicMock()
        mock_repo.actualizar_estado.return_value = mock_actualizado

        resultado = establecer_estado(id_usuario=1, id_juego=100, estado="completado")
        assert resultado == mock_actualizado

    def test_estado_invalido(self):
        resultado = establecer_estado(id_usuario=1, id_juego=100, estado="invalido")
        assert isinstance(resultado, str)
        assert "El status debe ser uno de" in resultado

    @patch('app.services.user_game_status_service.user_game_status_repo')
    def test_todos_los_estados_validos(self, mock_repo):
        mock_repo.obtener_estado.return_value = None
        mock_repo.crear_estado.return_value = MagicMock()

        for estado in ["pendiente", "pausado", "jugando", "completado"]:
            resultado = establecer_estado(id_usuario=1, id_juego=100, estado=estado)
            assert not isinstance(resultado, str)


class TestQuitarEstado:
    @patch('app.services.user_game_status_service.user_game_status_repo')
    def test_exitoso(self, mock_repo):
        mock_repo.eliminar_estado.return_value = True

        resultado = quitar_estado(id_usuario=1, id_juego=100)
        assert resultado is True

    @patch('app.services.user_game_status_service.user_game_status_repo')
    def test_estado_no_encontrado(self, mock_repo):
        mock_repo.eliminar_estado.return_value = None

        resultado = quitar_estado(id_usuario=1, id_juego=100)
        assert resultado == "Status no encontrado"


class TestObtenerEstadoDelJuego:
    @patch('app.services.user_game_status_service.user_game_status_repo')
    def test_retorna_estado_existente(self, mock_repo):
        mock_estado = MagicMock()
        mock_repo.obtener_estado.return_value = mock_estado

        resultado = obtener_estado_del_juego(id_usuario=1, id_juego=100)
        assert resultado == mock_estado

    @patch('app.services.user_game_status_service.user_game_status_repo')
    def test_retorna_none_si_no_existe(self, mock_repo):
        mock_repo.obtener_estado.return_value = None

        resultado = obtener_estado_del_juego(id_usuario=1, id_juego=100)
        assert resultado is None
