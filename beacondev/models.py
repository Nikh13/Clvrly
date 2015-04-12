from google.appengine.ext import db


class Beacon(db.Model):
    nickname = db.StringProperty()
    beaconuuid = db.StringProperty()
    groupids = db.ListProperty(int)
    description = db.TextProperty()


class Group(db.Model):
    nickname = db.StringProperty()
    triggerids = db.ListProperty(int)
    description = db.TextProperty()


class Trigger(db.Model):
    nickname = db.StringProperty()
    # 0 for image, 1 for video, 2 for advert, 3 for coupon
    linktype = db.IntegerProperty()
    description = db.StringProperty()
    triggerlink = db.StringProperty()
    # 0 for immediate, 1 for near and 2 for far
    triggerwhen = db.IntegerProperty()
