from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from werkzeug.exceptions import abort
from twilio.rest import Client
from random import randint
from ..models.users import Users
from ..models.otp import Otp
from ..config import Config

users_bp = Blueprint('users', __name__)


def twilio_msg_verify(phone_no):
    client = Client(Config.ACCOUNT_SID, Config.AUTH_TOKEN)

    random_no = randint(100000, 999999)
    message = '{} is your one time password (OTP)'.format(random_no)
    response = client.messages.create(to=phone_no, from_=Config.TWILIO_PHONE_NO,
                                      body=message)

    otp = Otp(phone_no=phone_no, otp=random_no)
    otp.save()

    return response


@users_bp.route(Config.USER_PROFILE, methods=['GET'])
@jwt_required
def user_profile(phone_no):
    if get_jwt_identity() == phone_no:
        user = Users.objects.get(phone_no=phone_no)
        return make_response(jsonify({
            'full_name': user.full_name,
            'photo_url': user.photo_url
        }), 200)
    else:
        abort(401)


# User can update their user profile based on their phone_no
@users_bp.route(Config.UPDATE_PROFILE, methods=['PUT'])
@jwt_required
def update_profile(phone_no):
    if get_jwt_identity() == phone_no:
        user = Users.objects(phone_no=phone_no).first()
        if 'full_name' in request.json:
            user.update(full_name=request.json['full_name'])

        if 'photo_url' in request.json:
            user.update(photo_url=request.json['photo_url'])

        return make_response(jsonify({
            'success': 'User profile updated successfully'
        }), 200)
    else:
        abort(401)


@users_bp.route(Config.SIGN_IN, methods=['POST'])
def sign_in():
    try:
        phone_no = request.json['phone_no']
        response = twilio_msg_verify(phone_no)

        if response:
            return make_response(jsonify({
                'success': "OTP is sent to your registered phone number"
            }), 200)

    except Users.DoesNotExist:
        return make_response(jsonify({
            'error': "Phone number you've entered is not registered"
        }), 401)


@users_bp.route(Config.SIGN_UP, methods=['POST'])
def sign_up():
    try:
        phone_no = request.json['phone_no']
        try:
            if Users.objects.get(phone_no=phone_no):
                return make_response(jsonify({"phone_no": phone_no+' already exists'}), 400)
        except Users.DoesNotExist:
            pass

        full_name = request.json['full_name']
        photo_url = request.json['photo_url']

        users = Users(full_name=full_name,
                      phone_no=phone_no,
                      photo_url=photo_url,
                      is_verify=False)
        users.save()

        response = twilio_msg_verify(phone_no)
        if response:
            return make_response(jsonify({
                'success': "OTP is sent to your registered phone number"
            }), 201)

    except KeyError:
        abort(400)


@users_bp.route(Config.OTP_VERIFY, methods=['POST'])
def account_verify():
    try:
        phone_no = request.json['phone_no']
        otp = request.json['otp']

        otp_obj = Otp.objects(phone_no=phone_no).first()
        if otp_obj == None:
            return make_response(jsonify({'error': 'User verification already completed'}), 200)

        if(otp_obj.otp == otp):
            otp_obj.delete()

            user = Users.objects(phone_no=phone_no).first()
            if(user.is_verify == True):
                access_token = create_access_token(identity=phone_no)

                return make_response(jsonify({
                    'access_token': access_token,
                    'full_name': user.full_name,
                    'photo_url': user.photo_url
                }), 200)
            else:
                user.update(is_verify=True)
                return make_response(jsonify({'message': 'User verification successful'}), 200)
        else:
            return make_response(jsonify({'error': 'Wrong One Time Password (OTP)'}), 200)
    except KeyError:
        abort(400)


@users_bp.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Invalid Request'}), 400)
