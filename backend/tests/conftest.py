import sys
from unittest.mock import MagicMock

_modulos_a_mockear = [
    'dotenv',
    'sqlalchemy',
    'sqlalchemy.orm',
    'app.database',
    'app.database.db',
    'app.database.seed',
    'app.models',
    'app.models.User',
    'app.models.Comment',
    'app.models.Favorite',
    'app.models.AddFavorite',
    'app.repositories',
    'app.repositories.comment_repo',
    'app.repositories.favorite_repo',
    'app.repositories.user_repo',
    'app.client',
    'app.client.clientRAWG',
    'app.services.adapter',
]

for nombre in _modulos_a_mockear:
    if nombre not in sys.modules:
        sys.modules[nombre] = MagicMock()
