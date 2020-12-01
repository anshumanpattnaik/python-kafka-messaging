from .. import db

class Users(db.Document):
    full_name = db.StringField(required=True)
    phone_no = db.StringField(required=True)
    photo_url = db.StringField(required=True)
    is_verify = db.BooleanField(request=True)