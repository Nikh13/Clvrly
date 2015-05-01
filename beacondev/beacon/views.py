import os

from os.path import dirname

from google.appengine.ext.webapp import template

from beacon.models import Beacon, Group, Trigger


import webapp2

from utils import JINJA_ENVIRONMENT


def render_template(self, template_name, template_values):
    template_path = os.path.join(
        dirname(dirname(__file__)),
        'templates',
        template_name
    )
    self.response.out.write(template.render(template_path, template_values))


class SingleBeacon(webapp2.RequestHandler):
    def get(self, key):
        beacon = None
        if key and key != 'add':
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
            for group in Group.query():
                groupjson = {
                    "nickname": group.nickname,
                    "id": group.key.id()
                }
                if group.key.id() in beacon.groupids:
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
        template = JINJA_ENVIRONMENT.get_template('single_beacon.html')
        self.response.write(template.render(final))


class SingleGroup(webapp2.RequestHandler):

    def get(self, key):
        # Preempt cycles
        from event.models import get_building_str
        group = None
        if key:
            group = Group.get_by_id(int(key))
        if group:
            groupjson = {
                "id": key,
                "nickname": group.nickname,
                "valid": True,
                "notnew": True
            }
            building_str = get_building_str(group.building)
            groupjson.update({building_str: True})
            triggers = []
            for trigger in Trigger.query():
                triggerjson = {
                    "nickname": trigger.nickname,
                    "id": trigger.key.id(),
                }
                if trigger.key.id() in group.triggerids:
                    triggerjson.update({"valid": True})
                else:
                    triggerjson.update({"valid": False})
                triggers.append(triggerjson)
            groupjson.update({"triggers": triggers})
            final = {"group": groupjson}
            template = JINJA_ENVIRONMENT.get_template('single_group.html')
            self.response.write(template.render(final))
        else:
            final = {}
            template = JINJA_ENVIRONMENT.get_template('404.html')
            self.response.write(template.render(final))


class SingleTrigger(webapp2.RequestHandler):
    def get(self, key):
        trigger = None
        if key and key != 'add':
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
            for group in Group.query():
                groupjson = {
                    "nickname": group.nickname,
                    "id": group.key.id()
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
        template = JINJA_ENVIRONMENT.get_template('single_trigger.html')
        self.response.write(template.render(final))


class ListBeacons(webapp2.RequestHandler):
    def get(self):
        beacons = Beacon.query()
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
        template = JINJA_ENVIRONMENT.get_template('manage_beacons.html')
        self.response.write(template.render(final))


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
        groups = Group.query()
        groupdetails = []
        for group in groups:
            valuepair = {}
            valuepair.update(
                {
                    'nickname': group.nickname,
                    'description': group.description,
                    'groupid': group.key.id()
                }
            )
            beacons = Beacon.query()
            grpbea = []
            for beacon in beacons:
                if group.key.id() in beacon.groupids:
                    beavp = {}
                    beavp.update(
                        {
                            'id': beacon.key.id(),
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
        template = JINJA_ENVIRONMENT.get_template('manage_groups.html')
        self.response.write(template.render(final))


class AddGroup(webapp2.RequestHandler):
    def post(self):
        from event.models import get_building_obj

        groupid = self.request.POST.get("groupid")
        nickname = self.request.POST.get("nickname")
        ts = self.request.get_all("triggerid")
        building_str = self.request.POST.get("building")
        building = get_building_obj(building_str)

        triggerids = []
        for t in ts:
            triggerids.append(int(t))
        description = self.request.get("description")

        group = None
        if groupid:
            keyid = int(groupid)
            group = Group.get_by_id(keyid)

        if group:
            group.nickname = nickname
            group.triggerids = triggerids
            group.description = description
            group.building = building
            group.put()
        else:
            group = Group(
                nickname=nickname,
                description=description,
                triggerids=triggerids,
                building=building,
            )
            group.put()
        self.redirect("/groups")

    def get(self):
        groupjson = {
            "nickname": None,
            'building': None,
            "triggers": None,
            "notnew": False,
            "valid": True,
        }
        final = {"group": groupjson}

        template = JINJA_ENVIRONMENT.get_template('single_group.html')
        self.response.write(template.render(final))


class ListTriggers(webapp2.RequestHandler):
    def get(self):
        triggers = Trigger.query()
        triggerdetails = []
        for trigger in triggers:
            valuepair = {}
            valuepair.update({
                'id': trigger.key.id(),
                'description': trigger.description,
                'nickname': trigger.nickname
            })
            groups = Group.query()
            trigrp = []
            for group in groups:
                if trigger.key.id() in group.triggerids:
                    grpvp = {
                        'id': group.key.id(),
                        'nickname': group.nickname
                    }
                    trigrp.append(grpvp)
            tribea = []
            beacons = Beacon.query()
            for beacon in beacons:
                for groupid in beacon.groupids:
                    if (trigger.key.id() in
                            Group.get_by_id(groupid).triggerids):
                        beavp = {
                            'id': beacon.key.id(),
                            'nickname': beacon.nickname,
                        }
                        tribea.append(beavp)
            valuepair.update({'groups': trigrp, 'beacons': tribea})
            triggerdetails.append(valuepair)
        final = {'triggers': triggerdetails}
        template = JINJA_ENVIRONMENT.get_template('manage_triggers.html')
        self.response.write(template.render(final))


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
        """
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
        """
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


class DumpData(webapp2.RequestHandler):
    def get(self):
        beacons = []
        for beacon in Beacon.query():
            beajson = {
                "id": beacon.beaconuuid,
                "groupids": beacon.groupids
            }
            beacons.append(beajson)
        groups = []
        for group in Group.query():
            groupjson = {
                "id": beacon.key.id(),
                "triggerids": group.triggerids
            }
            groups.append(groupjson)
        triggers = []
        for trigger in Trigger.query():
            trigjson = {
                "id": trigger.key.id(),
                "linktype": trigger.linktype,
                "triggerlink": trigger.triggerlink,
                "triggerwhen": trigger.triggerwhen
            }
            triggers.append(trigjson)
        data = {"beacons": beacons, "groups": groups, "triggers": triggers}
        self.response.write(data)
