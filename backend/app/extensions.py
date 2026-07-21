"""MindSight AI — Flask extension instances.

Centralised extension objects that are initialised in the app factory
via ``init_app()`` to avoid circular imports.
"""

from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cors = CORS()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)
