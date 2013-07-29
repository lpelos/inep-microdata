from mongoengine import *

connect('inep-microdata')

class Field(EmbeddedDocument):
    name = StringField(required=True, max_length=50)
    scores = ListField(IntField(min_value=0))

class Year(EmbeddedDocument):
    year = IntField(required=True)
    fields = ListField(EmbeddedDocumentField(Field))

class State(Document):
    id = StringField(required=True)
    name = StringField(required=True, max_length=50)
    years = ListField(EmbeddedDocumentField(Year))

class City(Document):
    id = StringField(required=True)
    name = StringField(required=True, max_length=50)
    state = ReferenceField(State)
    years = ListField(EmbeddedDocumentField(Year))

class School(Document):
    id = StringField(required=True)
    name = StringField(required=True, max_length=50)
    city = ReferenceField(City)
    years = ListField(EmbeddedDocumentField(Year))
