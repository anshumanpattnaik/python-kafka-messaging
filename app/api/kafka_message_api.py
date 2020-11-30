import json
from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from werkzeug.exceptions import abort
from kafka import KafkaProducer
from ..models.messages import Messages
from ..config import Config

messages_bp = Blueprint('messages', __name__)


@messages_bp.route(Config.SEND_MESSAGE, methods=['POST'])
@jwt_required
def send_message(phone_no):
    if get_jwt_identity() == phone_no:
        message_obj=json.dumps(request.json).encode('utf-8')

        producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
        producer.send(Config.KAFKA_TOPIC_NAME, message_obj)
        producer.flush()

        return make_response(jsonify({'success': 'Message has been sent successfully'}), 200)
    else:
        abort(401)


@messages_bp.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized Access'}), 401)
