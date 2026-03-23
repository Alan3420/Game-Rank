from flask import Blueprint, flash, jsonify

content_overview_bp = Blueprint('content_overview_route', __name__)

def get_content_overview():

    flash("Bienvenido a Game Rank, tu destino para descubrir y compartir tus experiencias de juego. Explora reseñas, calificaciones y recomendaciones personalizadas para encontrar tu próxima aventura gamer. ¡Únete a nuestra comunidad y comparte tu pasión por los videojuegos!")
    return jsonify({"message": "Mostrar el contenido principal de la pagina"}), 200