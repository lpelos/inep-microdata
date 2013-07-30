from mongoengine import *

connect('inep-microdata')

class Field(EmbeddedDocument):
    name = StringField(required=True, max_length=50)
    scores = ListField(IntField(min_value=0))

class Year(EmbeddedDocument):
    year = IntField(required=True)
    fields = ListField(EmbeddedDocumentField(Field))

class State(Document):
    code = StringField(required=True)
    acronym = StringField(required=True, max_length=50)
    years = ListField(EmbeddedDocumentField(Year))

class City(Document):
    code = StringField(required=True)
    name = StringField(required=True, max_length=50)
    state = ReferenceField(State)
    years = ListField(EmbeddedDocumentField(Year))

class School(Document):
    code = StringField(required=True)
    name = StringField(required=True, max_length=100)
    city = ReferenceField(City)
    state = ReferenceField(State)
    years = ListField(EmbeddedDocumentField(Year))
