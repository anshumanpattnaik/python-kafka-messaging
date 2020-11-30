from .. import db

class Otp(db.Document):
    phone_no = db.StringField(required=True)
    otp = db.IntField(required=True)