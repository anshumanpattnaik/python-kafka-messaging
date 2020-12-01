from .. import db

class Participants(db.Document):
    full_name = db.StringField(required=True)
    phone_no = db.StringField(required=True)


class Groups(db.Document):
    group_id = db.StringField(required=True)
    group_name = db.StringField(required=True)
    created_at = db.StringField(required=True)
    participants = db.ListField(db.ReferenceField(Participants))