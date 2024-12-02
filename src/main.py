from .extends import db, login_manager, migrate, bcrypt
from .routers.register import register
from .routers.login import login
from .config import Config
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(login)
    app.register_blueprint(register)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    run_app = create_app()
    run_app.run(host="192.168.0.111", port=6043, debug=True)
