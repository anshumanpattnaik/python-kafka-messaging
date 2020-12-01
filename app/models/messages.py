from .. import db

class Messages(db.Document):
    sender = db.StringField(required=True)
    receiver = db.StringField(required=True)
    participants = db.StringField(required=True)
    phone_no = db.StringField(required=True)
    message = db.StringField(required=True)
    timestamp = db.StringField(required=True)