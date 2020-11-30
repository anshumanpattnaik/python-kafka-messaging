import os

class Config:
    # Mongo db connection url
    MONGO_DB_CONNECTION = 'mongodb://127.0.0.1:27017/whatsapp'

    # Twilio Credentials
    ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    TWILIO_PHONE_NO = os.environ.get('TWILIO_PHONE_NO')

    # API Configs
    API_PATH = '/api/'
    API_VERSION = 'v1'
    BASE_URL = 'http://127.0.0.1:5000'

    # User API endpoint
    SIGN_IN = API_PATH+API_VERSION+'/sign_in'
    SIGN_UP = API_PATH+API_VERSION+'/sign_up'
    OTP_VERIFY = API_PATH+API_VERSION+'/otp_verify'
    USER_PROFILE = API_PATH+API_VERSION+'/profile/<string:phone_no>'
    UPDATE_PROFILE = API_PATH+API_VERSION+'/update_profile/<string:phone_no>'