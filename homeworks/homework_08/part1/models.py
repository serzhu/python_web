from mongoengine import  Document
from mongoengine.fields import ReferenceField, StringField

class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    author = ReferenceField(Author)
    quote = StringField()
    meta = {'allow_inheritance': True}

class Tag(Document):
    quote = ReferenceField(Quote)
    tag = StringField()
    meta = {'allow_inheritance': True}