#######################################
#     Cleverly Beacon Backend     #
#######################################

import os

from google.appengine.ext.webapp import template

from models import Beacon, Group, Trigger

import webapp2


TRIGGER_IMMEDIATE = 0
TRIGGER_NEAR = 1
TRIGGER_FAR = 2
LINK_IMAGE = 0
LINK_VIDEO = 1
LINK_ADVERT = 2
LINK_COUPON = 3


def render_template(self, template_name, template_values):
    template_path = os.path.join(
        os.path.dirname(__file__),
        'templates',
        template_name
    )
    self.response.out.write(template.render(template_path, template_values))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Beacon Dev Backend')


class SingleBeacon(webapp2.RequestHandler):
    def get(self, key):
        if key != 'add':
            beacon = Beacon.get_by_id(int(key))
            if beacon:
                beaconjson = {
                    "valid": True,
                    "nickname": beacon.nickname,
                    "id": key,
                    "notnew": True,
                    "uuid": beacon.beaconuuid
                }
                groups = []
                for group in Group.all():
                    groupjson = {
                        "nickname": group.nickname,
                        "id": group.key().id()
                    }
                    if group.key().id() in beacon.groupids:
                        groupjson.update({"valid": True})
                    else:
                        groupjson.update({"valid": False})
                    groups.append(groupjson)
                beaconjson.update({"groups": groups})
        else:
            beaconjson = {
                "valid": True,
                "nickname": None,
                "groups": None,
                "notnew": False,
            }
        final = {"beacon": beaconjson}
        render_template(self, "single_beacon.html", final)


class SingleGroup(webapp2.RequestHandler):

    def get(self, key):
        if key != 'add':
            group = Group.get_by_id(int(key))
            if group:
                groupjson = {
                    "id": key,
                    "nickname": group.nickname,
                    "valid": True,
                    "notnew": True
                }
                triggers = []
                for trigger in Trigger.all():
                    triggerjson = {
                        "nickname": trigger.nickname,
                        "id": trigger.key().id(),
                    }
                    if trigger.key().id() in group.triggerids:
                        triggerjson.update({"valid": True})
                    else:
                        triggerjson.update({"valid": False})
                    triggers.append(triggerjson)
                groupjson.update({"triggers": triggers})
        else:
            groupjson = {
                "nickname": None,
                "triggers": None,
                "notnew": False,
                "valid": True,
            }
        final = {"group": groupjson}
        render_template(self, "single_group.html", final)


class SingleTrigger(webapp2.RequestHandler):
    def get(self, key):
        if key != 'add':
            trigger = Trigger.get_by_id(int(key))
            if trigger:
                triggerjson = {
                    "id": key,
                    "nickname": trigger.nickname,
                    "linktype": trigger.linktype,
                    "triggerlink": trigger.triggerlink,
                    "valid": True,
                    "notnew": True,
                }
                groups = []
                for group in Group.all():
                    groupjson = {
                        "nickname": group.nickname,
                        "id": group.key().id()
                    }
                    if key in group.triggerids:
                        groupjson.update({"valid": True})
                    else:
                        groupjson.update({"valid": False})
                    groups.append(groupjson)
                triggerjson.update({"groups": groups})
        else:
            triggerjson = {
                "nickname": None,
                "groups": None,
                "notnew": False,
                "valid": True,
            }
        final = {"trigger": triggerjson}
        render_template(self, "single_trigger.html", final)


class ListBeacons(webapp2.RequestHandler):
    def get(self):
        beacons = Beacon.all()
        beacondetails = []
        triggers = []
        for beacon in beacons:
            valuepair = {}
            valuepair.update({'nickname': beacon.nickname})
            valuepair.update({'beaconuuid': beacon.beaconuuid})
            gs = beacon.groupids
            groups = []
            for g in gs:
                group = {}
                gdb = Group.get_by_id(int(g))
                group.update({'nickname': gdb.nickname})
                group.update({'id': g})
                for t in gdb.triggerids:
                    tdb = Trigger.get_by_id(int(t))
                    trig = {}
                    trig.update({'nickname': tdb.nickname, 'id': t})
                    triggers.append(trig)
                groups.append(group)

            valuepair.update({'groups': groups})
            valuepair.update({'triggers': triggers})
            valuepair.update({'description': beacon.description})
            beacondetails.append(valuepair)
        final = {}
        final.update({'beacons': beacondetails})
        render_template(self, 'manage_beacons.html', final)


class AddBeacon(webapp2.RequestHandler):
    def post(self):
        beaconid = self.request.get("beaconid")
        nickname = self.request.get("nickname")
        beaconuuid = self.request.get("beaconuuid")
        groupid = self.request.get_all("groupid")
        groupids = []
        for g in groupid:
            groupids.append(int(g))
        description = self.request.get("description")
        try:
            keyid = int(beaconid)
            beacon = Beacon.get_by_id(keyid)
        except Exception:
            beacon = None
        if beacon is None:
            beacon = Beacon(
                nickname=nickname,
                beaconuuid=beaconuuid,
                groupids=groupids,
                description=description
            )
            beacon.put()
        else:
            beacon.nickname = nickname
            beacon.beaconuuid = beaconuuid
            beacon.groupids = groupids
            beacon.description = description
            beacon.put()
        self.redirect("/beacons")


class ListGroups(webapp2.RequestHandler):
    def get(self):
        groups = Group.all()
        groupdetails = []
        for group in groups:
            valuepair = {}
            valuepair.update(
                {
                    'nickname': group.nickname,
                    'description': group.description,
                    'groupid': group.key().id()
                }
            )
            beacons = Beacon.all()
            grpbea = []
            for beacon in beacons:
                if group.key().id() in beacon.groupids:
                    beavp = {}
                    beavp.update(
                        {
                            'id': beacon.key().id(),
                            'nickname': beacon.nickname
                        }
                    )
                    grpbea.append(beavp)
            grptri = []
            for grtri in group.triggerids:
                trigger = Trigger.get_by_id(grtri)
                trivp = {}
                trivp.update({'id': grtri, 'nickname': trigger.nickname})
                grptri.append(trivp)
            valuepair.update({'beacons': grpbea, 'triggers': grptri})
            groupdetails.append(valuepair)
        final = {'groups': groupdetails}
        render_template(self, 'manage_groups.html', final)


class AddGroup(webapp2.RequestHandler):
    def post(self):
        groupid = self.request.get("groupid")
        nickname = self.request.get("nickname")
        ts = self.request.get_all("triggerid")
        triggerids = []
        for t in ts:
            triggerids.append(int(t))
        description = self.request.get("description")
        try:
            keyid = int(groupid)
            group = Group.get_by_id(keyid)
        except Exception:
            group = None
        if group is None:
            group = Group(
                nickname=nickname,
                description=description,
                triggerids=triggerids
            )
            group.put()
        else:
            group.nickname = nickname
            group.triggerids = triggerids
            group.description = description
            group.put()
        self.redirect("/groups")


class ListTriggers(webapp2.RequestHandler):
    def get(self):
        triggers = Trigger.all()
        triggerdetails = []
        for trigger in triggers:
            valuepair = {}
            valuepair.update({
                'id': trigger.key().id(),
                'description': trigger.description,
                'nickname': trigger.nickname
            })
            groups = Group.all()
            trigrp = []
            for group in groups:
                if trigger.key().id() in group.triggerids:
                    grpvp = {
                        'id': group.key().id(),
                        'nickname': group.nickname
                    }
                    trigrp.append(grpvp)
            tribea = []
            beacons = Beacon.all()
            for beacon in beacons:
                for groupid in beacon.groupids:
                    if (trigger.key().id() in
                            Group.get_by_id(groupid).triggerids):
                        beavp = {
                            'id': beacon.key().id(),
                            'nickname': beacon.nickname,
                        }
                        tribea.append(beavp)
            valuepair.update({'groups': trigrp, 'beacons': tribea})
            triggerdetails.append(valuepair)
        final = {'triggers': triggerdetails}
        render_template(self, 'manage_triggersi.html', final)


class AddTrigger(webapp2.RequestHandler):
    def post(self):

        triggerid = self.request.get("triggerid")
        nickname = self.request.get("nickname")
        description = self.request.get("description")
        trigtype = self.request.get("linktype")
        triglink = self.request.get("link")
        trigwhen = self.request.get("triggerwhen")

        try:
            keyid = int(triggerid)
            trigger = Trigger.get_by_id(keyid)
        except Exception:
            trigger = None

        if trigger is None:
            trigger = Trigger(
                nickname=nickname,
                description=description,
                triggerlink=triglink,
                linktype=int(trigtype),
                triggerwhen=int(trigwhen)
            )
            trigger.put()
        else:
            trigger.nickname = nickname
            trigger.description = description
            trigger.triggertype = trigtype
            trigger.triggerlink = triglink
            trigger.triggerwhen = trigwhen
            trigger.put()

        self.redirect("/triggers")


class DumpData(webapp2.RequestHandler):
    def get(self):
        beacons = []
        for beacon in Beacon.all():
            beajson = {
                "id": beacon.beaconuuid,
                "groupids": beacon.groupids
            }
            beacons.append(beajson)
        groups = []
        for group in Group.all():
            groupjson = {
                "id": beacon.key().id(),
                "triggerids": group.triggerids
            }
            groups.append(groupjson)
        triggers = []
        for trigger in Trigger.all():
            trigjson = {
                "id": trigger.key().id(),
                "linktype": trigger.linktype,
                "triggerlink": trigger.triggerlink,
                "triggerwhen": trigger.triggerwhen
            }
            triggers.append(trigjson)
        data = {"beacons": beacons, "groups": groups, "triggers": triggers}
        self.response.write(data)


class TestTemplate(webapp2.RequestHandler):
    def get(self):
        values = {}
        groups = [
            {
                'id': '1213',
                'nickname': 'Fiction',
                'valid': False},
            {
                'id': '1431',
                'name': 'Entrance'
            }
        ]
        triggers = [
            {
                'id': '1213',
                'nickname': 'Discount'},
            {
                'id': '1213',
                'name': 'New Dan Brown'}
        ]
        beacons = [
            {
                'nickname': 'Awesome Beacon #1',
                'description': 'Some description here',
                'groups': groups,
                'grouptriggers': triggers
            },
            {
                'nickname': 'Awesome Beacon #2',
                'description': 'Some description here',
                'groups': triggers,
                'grouptriggers': groups
            }
        ]
        # values.update({
        #   'beacons':beacons
        #   })
        beacon = {
            'valid': True,
            'notnew': True,
            'nickname': 'beacon 1',
            'uuid': '1213123',
            'groups': groups,
            'id': 5136918324969472
        }
        values = {'beacon': beacon}
        render_template(self, 'single_beacon.html', values)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addtrigger', AddTrigger),
    ('/addgroup', AddGroup),
    ('/addbeacon', AddBeacon),
    ('/beacons/(.*)', SingleBeacon),
    ('/groups/(.*)', SingleGroup),
    ('/triggers/(.*)', SingleTrigger),
    ('/beacons', ListBeacons),
    ('/groups', ListGroups),
    ('/triggers', ListTriggers),
    ('/test', TestTemplate),
    ('/api/all', DumpData)
], debug=True)
