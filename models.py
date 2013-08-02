import os
from mongoengine import *

connect("inep-microdata", host=os.environ.get("MONGOHQ_URL", "localhost"))

class ScoreSheet(EmbeddedDocument):
    fields = DictField()

class State(Document):
    code = StringField(required=True)
    acronym = StringField(required=True, max_length=50)
    score_sheets = MapField(field=EmbeddedDocumentField(ScoreSheet))

class City(Document):
    code = StringField(required=True)
    name = StringField(required=True, max_length=50)
    state = ReferenceField(State)
    score_sheets = MapField(field=EmbeddedDocumentField(ScoreSheet))

class School(Document):
    code = StringField(required=True)
    name = StringField(required=True, max_length=100)
    city = ReferenceField(City)
    state = ReferenceField(State)
    score_sheets = MapField(field=EmbeddedDocumentField(ScoreSheet))
