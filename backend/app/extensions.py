"""MindSight AI — Flask extension instances.

Centralised extension objects that are initialised in the app factory
via ``init_app()`` to avoid circular imports.
"""

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cors = CORS()
