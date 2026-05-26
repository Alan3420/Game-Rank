from unittest.mock import patch, MagicMock
from app.services.comment_services import (
    crear_comentario,
    actualizar_comentario,
    eliminar_comentario,
)


class TestCrearComentario:
    @patch('app.services.comment_services.comment_repo')
    def test_exitoso(self, mock_repo):
        mock_repo.obtener_comentarios_por_juego.return_value = []
        mock_comentario = MagicMock()
        mock_repo.crear_comentario.return_value = mock_comentario

        resultado = crear_comentario(id_usuario=1, id_juego=100, descripcion="Buen juego")

        assert resultado == mock_comentario

    def test_descripcion_vacia(self):
        resultado = crear_comentario(id_usuario=1, id_juego=100, descripcion="")
        assert resultado == "La descripción debe tener entre 1 y 255 caracteres"

    def test_descripcion_supera_255_caracteres(self):
        resultado = crear_comentario(id_usuario=1, id_juego=100, descripcion="a" * 256)
        assert resultado == "La descripción debe tener entre 1 y 255 caracteres"

    @patch('app.services.comment_services.comment_repo')
    def test_usuario_ya_comento(self, mock_repo):
        comentario_existente = MagicMock()
        comentario_existente.id_user = 1
        mock_repo.obtener_comentarios_por_juego.return_value = [comentario_existente]

        resultado = crear_comentario(id_usuario=1, id_juego=100, descripcion="Buen juego")
        assert resultado == "Ya has comentado este juego"


class TestActualizarComentario:
    @patch('app.services.comment_services.comment_repo')
    def test_exitoso(self, mock_repo):
        mock_comentario = MagicMock()
        mock_repo.actualizar_comentario.return_value = mock_comentario

        resultado = actualizar_comentario(id_comentario=1, descripcion="Actualizado", id_usuario=1)
        assert resultado == mock_comentario

    @patch('app.services.comment_services.comment_repo')
    def test_comentario_no_encontrado(self, mock_repo):
        mock_repo.actualizar_comentario.return_value = None

        resultado = actualizar_comentario(id_comentario=999, descripcion="Texto", id_usuario=1)
        assert resultado == "Comentario no encontrado"

    def test_descripcion_supera_255_caracteres(self):
        resultado = actualizar_comentario(id_comentario=1, descripcion="a" * 256, id_usuario=1)
        assert resultado == "La descripción debe tener entre 1 y 255 caracteres"


class TestEliminarComentario:
    @patch('app.services.comment_services.comment_repo')
    def test_exitoso(self, mock_repo):
        mock_repo.eliminar_comentario.return_value = True

        resultado = eliminar_comentario(id_comentario=1, id_usuario=1)
        assert resultado is True

    @patch('app.services.comment_services.comment_repo')
    def test_comentario_no_encontrado(self, mock_repo):
        mock_repo.eliminar_comentario.return_value = None

        resultado = eliminar_comentario(id_comentario=999, id_usuario=1)
        assert resultado == "Comentario no encontrado"
