from datetime import datetime
from nls import db

class Library(db.Document):
    name = db.StringField(max_length=80, unique=True)
    slug = db.StringField(max_length=80, unique=True)
    address = db.StringField(max_length=255)
    lnglat =  db.PointField()
    library_authority = db.StringField(max_length=80)
    accountable_councillor = db.StringField(max_length=80)
    image_file_name = db.StringField(max_length=80)

    meta = {'indexes': [
        {'fields': ['$name', '$address', '$library_authority'],
        'default_language': 'english',
        'weights': {'name': 30, 'library_authority': 10, 'address': 10}
        }
    ]}

class Event(db.Document):
    title = db.StringField(max_length=150)
    category = db.StringField(max_length=50)
    library = db.ReferenceField('Library')
    occurs_at = db.DateTimeField()

    meta = {'indexes': [
        {'fields': ['$title'],
        'default_language': 'english',
        'weights': {'title': 30}
        }
    ]}