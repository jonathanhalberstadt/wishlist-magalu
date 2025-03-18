from flask import Flask
from api.infrastructure.config import Config
from api.routes import register_routes
from api.infrastructure.extensions import db, bcrypt, migrate

app = Flask(__name__)
def create_app():
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
