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