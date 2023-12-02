from mongoengine import *
import datetime

class Checkpoint(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
    kilometers: MongoEngine float field, required, (checkpoint distance in kilometers),
		location: MongoEngine string field, optional, (checkpoint location name),
		open_time: MongoEngine datetime field, required, (checkpoint opening time),
		close_time: MongoEngine datetime field, required, (checkpoint closing time).
    miles: MongoEngine float field, required, (checkpoint distance in kilometers)
    """
    kilometers = FloatField(required = True)
    location = StringField()
    open = DateTimeField(required = True)
    close = DateTimeField(required = True)
    miles = FloatField()

class Brevet(Document):
    """
    A MongoEngine document containing:
		total_distance: MongoEngine float field, required
		start_time: MongoEngine datetime field, required
		control_data: MongoEngine list field of Checkpoints, required
    """
    total_distance = FloatField(required = True)
    date_time = DateTimeField(required = True)
    control_data = EmbeddedDocumentListField(Checkpoint, required = True)
