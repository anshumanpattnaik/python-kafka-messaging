from flask import Flask, redirect
from flask.helpers import send_from_directory
from .config import Config
from flask_mongoengine import MongoEngine
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager

db = MongoEngine()

app = Flask(__name__)

# Initialize jwt manager using the secret key
app.config['JWT_SECRET_KEY'] = 'python-kafka-messaging'
jwt = JWTManager(app)


@app.route('/')
def redirect_to_docs():
    return redirect(Config.BASE_URL+"/api/docs")

# Swagger api docs route
@app.route('/swagger/<path:path>')
def send_static(path):
    return send_from_directory('swagger', path)


def initialize_app():
    SWAGGER_URL = '/api/docs'
    API_URL = '/swagger/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Python Kafka Messaging"
        })
    app.register_blueprint(swaggerui_blueprint)

    app.config['MONGODB_SETTINGS'] = {
        'host': Config.MONGO_DB_CONNECTION,
    }
    db.init_app(app)

    from app.api.users_api import users_bp
    app.register_blueprint(users_bp)

    from app.api.kafka_message_api import messages_bp
    app.register_blueprint(messages_bp)

    from app.api.groups_api import groups_bp
    app.register_blueprint(groups_bp)

    return app
