from datetime import datetime, timedelta

from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages


class Building(messages.Enum):
    TT = 1
    SJT = 2


def get_building_str(building):
    if building == Building.TT:
        return "TT"
    elif building == Building.SJT:
        return "SJT"


def get_building_obj(building_str):
    if building_str == 'TT':
        return Building.TT
    elif building_str == 'SJT':
        return Building.SJT


class Event(ndb.Model):
    namespace = ndb.StringProperty()
    name = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    building = msgprop.EnumProperty(Building, required=True)

    def put(self, *args, **kwargs):
        self.namespace = "Event"
        super(Event, self).put()

    def _get_time(self):
        return self.time.strftime("%d/%m/%Y %H:%M:%S")

    get_time = property(_get_time)
