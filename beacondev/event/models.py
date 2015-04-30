from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages


class Buildings(messages.Enum):
    TT = 1
    SJT = 2


class Event(ndb.Model):
    namespace = ndb.StringProperty()
    name = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    building = msgprop.EnumProperty(Buildings, required=True)

    def save(self, *args, **kwargs):
        self.namespace = "Event"
        super(Event, self).save()
