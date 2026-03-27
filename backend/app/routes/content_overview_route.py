from flask import Blueprint, jsonify



content_overview_bp = Blueprint('content_overview_route', __name__)

@content_overview_bp.route('/overview')  
def get_content():

    temporal_message = "Hola, bienvenido a Game Rank, tu destino para descubrir y compartir tus experiencias de juego. Explora reseñas, calificaciones y recomendaciones personalizadas para encontrar tu próxima aventura gamer. ¡Únete a nuestra comunidad y comparte tu pasión por los videojuegos!"

    return jsonify({"message":temporal_message})