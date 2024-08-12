# __init__.py

from flask import Flask
from .models import Base, engine, Session

def create_app():
    app = Flask(__name__)

    # Database initialization
    Base.metadata.create_all(engine)

    # Register Blueprints or routes if needed
    from .main import register_routes
    register_routes(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        Session.remove()

    return app
