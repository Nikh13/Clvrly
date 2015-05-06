from google.appengine.ext import ndb

# from event.models import Building


# class DistanceBucket(messages.Enum):
#     NEAR = 0
#     FAR = 1
#     NEXT_TO = 2


distance_choices = {
    'NEXT_TO': 0,
    'NEAR': 1,
    'FAR': 2
}


class Beacon(ndb.Model):
    nickname = ndb.StringProperty(indexed=True)
    uuid = ndb.StringProperty(indexed=True)
    description = ndb.TextProperty()


class Action(ndb.Model):
    nickname = ndb.StringProperty()
    type = ndb.IntegerProperty()
    payload = ndb.StringProperty()
    description = ndb.TextProperty()


class SimpleRule(ndb.Model):
    beaconid = ndb.KeyProperty(Beacon, indexed=True)
    # 0 for immediate, 1 for near
    # and 2 for far
    distance = ndb.IntegerProperty()


class Rule(ndb.Model):
    nickname = ndb.StringProperty(indexed=True)
    actionid = ndb.KeyProperty(Action)
    rules = ndb.StructuredProperty(SimpleRule, repeated=True)
    description = ndb.TextProperty()


class JSONDump(ndb.Model):
    jsondata = ndb.StringProperty()


# class Group(ndb.Model):
#     nickname = ndb.StringProperty(indexed=True)
#     triggerids = ndb.IntegerProperty(repeated=True)
#     description = ndb.TextProperty()
#     beaconids = ndb.IntegerProperty(repeated=True)
#     building = msgprop.EnumProperty(Building,
#                                     required=True,
#                                     indexed=True)



# class Trigger(ndb.Model):
#     nickname = ndb.StringProperty()
#     # 0 for image, 1 for video,
#     # 2 for advert, 3 for coupon
#     linktype = ndb.IntegerProperty()
#     description = ndb.StringProperty()
#     triggerlink = ndb.StringProperty()
#     # 0 for immediate, 1 for near
#     # and 2 for far
#     triggerwhen = ndb.IntegerProperty()
