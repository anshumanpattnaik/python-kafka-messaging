import json
from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from werkzeug.exceptions import abort
from kafka import KafkaProducer
from ..models.messages import Messages
from ..config import Config

messages_bp = Blueprint('messages', __name__)

# Fetch messages for a particular consumer
@messages_bp.route(Config.RECEIVE_MESSAGE, methods=['GET'])
@jwt_required
def receive_message(phone_no, receiver):
    if get_jwt_identity() == phone_no:
        sender_message = Messages.objects(receiver=phone_no)
        receiver_message = Messages.objects(receiver=receiver)

        return make_response(jsonify({
            'sender_message': sender_message,
            'receiver_message': receiver_message
        }), 200)
    else:
        abort(401)

# Produce messages with the consumers using KafkaProducer
@messages_bp.route(Config.SEND_MESSAGE, methods=['POST'])
@jwt_required
def send_message(phone_no):
    if get_jwt_identity() == phone_no:
        try:
            message_obj = json.dumps(request.json).encode('utf-8')

            sender = request.json['sender']
            receiver = request.json['receiver']
            phone_no = request.json['phone_no']
            message = request.json['message']
            timestamp = request.json['timestamp']

            # Removed (+) operator as Kafka doesn't allow special characters
            receiver = receiver.replace("+", "")
            participants = '{}_{}'.format(phone_no, receiver)

            # Instantiate kafka producer to send message to a topic
            producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
            producer.send(receiver, message_obj)
            producer.flush()

            message = Messages(sender=sender,
                               receiver=receiver,
                               participants=participants,
                               phone_no=phone_no,
                               message=message,
                               timestamp=timestamp)
            message.save()

            return make_response(jsonify({'success': 'Message has been sent successfully'}), 200)
        except KeyError as e:
            print(e)
            abort(400)
    else:
        abort(401)


@messages_bp.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Invalid Request'}), 400)


@messages_bp.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized Access'}), 401)
