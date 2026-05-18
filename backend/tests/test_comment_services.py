from unittest.mock import patch, MagicMock
from app.services.comment_services import (
    crear_comentario,
    actualizar_comentario,
    eliminar_comentario,
)


class TestCrearComentario:
    @patch('app.services.comment_services.create_comment')
    @patch('app.services.comment_services.get_comments_by_game')
    def test_exitoso(self, mock_get, mock_create):
        mock_get.return_value = []
        mock_comment = MagicMock()
        mock_create.return_value = mock_comment

        resultado = crear_comentario(id_user=1, id_game=100, description="Buen juego")

        assert resultado == mock_comment

    def test_descripcion_vacia(self):
        resultado = crear_comentario(id_user=1, id_game=100, description="")
        assert resultado == "La descripción debe tener entre 1 y 255 caracteres"

    def test_descripcion_supera_255_caracteres(self):
        resultado = crear_comentario(id_user=1, id_game=100, description="a" * 256)
        assert resultado == "La descripción debe tener entre 1 y 255 caracteres"

    @patch('app.services.comment_services.get_comments_by_game')
    def test_usuario_ya_comento(self, mock_get):
        comentario_existente = MagicMock()
        comentario_existente.id_user = 1
        mock_get.return_value = [comentario_existente]

        resultado = crear_comentario(id_user=1, id_game=100, description="Buen juego")
        assert resultado == "Ya has comentado este juego"


class TestActualizarComentario:
    @patch('app.services.comment_services.update_comment')
    def test_exitoso(self, mock_update):
        mock_comment = MagicMock()
        mock_update.return_value = mock_comment

        resultado = actualizar_comentario(comment_id=1, description="Actualizado", user_id=1)
        assert resultado == mock_comment

    @patch('app.services.comment_services.update_comment')
    def test_comentario_no_encontrado(self, mock_update):
        mock_update.return_value = None

        resultado = actualizar_comentario(comment_id=999, description="Texto", user_id=1)
        assert resultado == "Comentario no encontrado"

    def test_descripcion_supera_255_caracteres(self):
        resultado = actualizar_comentario(comment_id=1, description="a" * 256, user_id=1)
        assert resultado == "La descripción debe tener entre 1 y 255 caracteres"


class TestEliminarComentario:
    @patch('app.services.comment_services.delete_comment')
    def test_exitoso(self, mock_delete):
        mock_delete.return_value = True

        resultado = eliminar_comentario(comment_id=1, user_id=1)
        assert resultado is True

    @patch('app.services.comment_services.delete_comment')
    def test_comentario_no_encontrado(self, mock_delete):
        mock_delete.return_value = None

        resultado = eliminar_comentario(comment_id=999, user_id=1)
        assert resultado == "Comentario no encontrado"
