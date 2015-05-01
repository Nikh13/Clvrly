from google.appengine.ext import ndb

from google.appengine.ext.ndb import msgprop
from protorpc import messages

from event.models import Building

class Beacon(ndb.Model):
    nickname = ndb.StringProperty(indexed=True)
    beaconuuid = ndb.StringProperty(indexed=True)
    groupids = ndb.IntegerProperty(repeated=True)
    description = ndb.TextProperty()


class Group(ndb.Model):
    nickname = ndb.StringProperty(indexed=True)
    triggerids = ndb.IntegerProperty(repeated=True)
    description = ndb.TextProperty()
    beaconids = ndb.IntegerProperty(repeated=True)
    building = msgprop.EnumProperty(Building,
                                required=True, indexed=True)


class Trigger(ndb.Model):
    nickname = ndb.StringProperty()
    # 0 for image, 1 for video,
    # 2 for advert, 3 for coupon
    linktype = ndb.IntegerProperty()
    description = ndb.StringProperty()
    triggerlink = ndb.StringProperty()
    # 0 for immediate, 1 for near
    # and 2 for far
    triggerwhen = ndb.IntegerProperty()
