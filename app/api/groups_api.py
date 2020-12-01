from kafka.admin import KafkaAdminClient, NewTopic
from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from werkzeug.exceptions import abort
from ..models.messages import Messages
from ..models.groups import Groups
from ..config import Config

groups_bp = Blueprint('groups', __name__)

# Fetch group conversations using group id
@groups_bp.route(Config.GROUP_MESSAGES, methods=['GET'])
@jwt_required
def receive_group_messages(phone_no, group_id):
    if get_jwt_identity() == phone_no:
        messages = Messages.objects(receiver=group_id)
        return make_response(jsonify({
            'messages': messages
        }), 200)
    else:
        abort(401)

# Create a group using Kafka create_topics
# Produce messages with subscribed consumers
@groups_bp.route(Config.CREATE_GROUPS, methods=['POST'])
@jwt_required
def create_group(phone_no):
    if get_jwt_identity() == phone_no:
        try:
            group_id = request.json['group_id']
            group_name = request.json['group_name']
            created_at = request.json['created_at']
            participants = request.json['participants']

            # Instantiate kafka admin client to create a topic
            client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id=phone_no)

            topics = []
            topics.append(NewTopic(name=group_id, num_partitions=1, replication_factor=1))
            client.create_topics(new_topics=topics, validate_only=False)

            group = Groups(group_id=group_id,
                           group_name=group_name,
                           created_at=created_at,
                           participants=participants)
            group.save()

            return make_response(jsonify({
                'success': 'Group created successfully'
            }), 200)
        except KeyError:
            abort(400)
    else:
        abort(401)


@groups_bp.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Invalid Request'}), 400)


@groups_bp.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized Access'}), 401)
