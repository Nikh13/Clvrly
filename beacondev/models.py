from google.apipengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages


class Beacon(ndb.Model):
    nickname = ndb.StringProperty()
    beaconuuid = ndb.StringProperty()
    groupids = ndb.ListProperty(int)
    description = ndb.TextProperty()


class Group(ndb.Model):
    nickname = ndb.StringProperty()
    triggerids = ndb.ListProperty(int)
    description = ndb.TextProperty()


class Trigger(ndb.Model):
    nickname = ndb.StringProperty()
    # 0 for image, 1 for video, 2 for advert, 3 for coupon
    linktype = ndb.IntegerProperty()
    description = ndb.StringProperty()
    triggerlink = ndb.StringProperty()
    # 0 for immediate, 1 for near and 2 for far
    triggerwhen = ndb.IntegerProperty()


class Buildings(messages.Enum):
    TT = 'Technology Tower'
    SJT = 'Silver Jubilee Tower'


class Event(ndb.Model):
    name = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    building = msgprop.EnumProperty(Buildings, required=True)
