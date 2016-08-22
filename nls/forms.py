from wtforms import Form, BooleanField, TextField, StringField, RadioField, HiddenField, TextAreaField, validators, ValidationError, FieldList, FormField, SelectField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField

class PledgeForm(Form):
    name = StringField('Name', [validators.Required()])
    email = EmailField('Email', [validators.Required()]) 
    activity = StringField('I want to ...', [validators.Required()], widget=TextArea(), description="eg start a reading group, learn 3D printing, join a discussion group")
    organise = BooleanField('I can help organise this')