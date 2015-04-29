from google.appengine.ext import ndb


class Beacon(ndb.Model):
    nickname = ndb.StringProperty()
    beaconuuid = ndb.StringProperty()
    groupids = ndb.IntegerProperty(repeated=True)
    description = ndb.TextProperty()


class Group(ndb.Model):
    nickname = ndb.StringProperty()
    triggerids = ndb.IntegerProperty(repeated=True)
    description = ndb.TextProperty()


class Trigger(ndb.Model):
    nickname = ndb.StringProperty()
    # 0 for image, 1 for video, 2 for advert, 3 for coupon
    linktype = ndb.IntegerProperty()
    description = ndb.StringProperty()
    triggerlink = ndb.StringProperty()
    # 0 for immediate, 1 for near and 2 for far
    triggerwhen = ndb.IntegerProperty()
