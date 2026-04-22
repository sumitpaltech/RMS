from flask import Flask
from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def create_app():
    app = Flask(__name__, template_folder="views/templates", static_folder="../static")
    app.config.from_object(Config)

    mysql.init_app(app)

    # Register routes (like Laravel's routes/web.php)
    from app.controllers.task_controller import task_bp
    from app.controllers.auth_controller import auth_bp

    app.register_blueprint(task_bp)
    app.register_blueprint(auth_bp)

    return app
