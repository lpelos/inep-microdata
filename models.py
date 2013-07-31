from mongoengine import *

connect('inep-microdata')

class State(Document):
    code = StringField(required=True)
    acronym = StringField(required=True, max_length=50)

class City(Document):
    code = StringField(required=True)
    name = StringField(required=True, max_length=50)
    state = ReferenceField(State)

class School(Document):
    code = StringField(required=True)
    name = StringField(required=True, max_length=100)
    city = ReferenceField(City)
    state = ReferenceField(State)

class ScoreSheet(Document):
    year = IntField(required=True)
    fields = DictField()
    ref = GenericReferenceField()
