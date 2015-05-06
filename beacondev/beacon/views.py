import os
import json

from os.path import dirname

from google.appengine.ext.webapp import template

from beacon.models import Beacon, Action, Rule, JSONDump
import beacon.constants as beacon_constants


import webapp2

from utils import JINJA_ENVIRONMENT


def render_template(self, template_name, template_values):
    template_path = os.path.join(
        dirname(dirname(__file__)),
        'templates',
        template_name
    )
    self.response.out.write(template.render(template_path, template_values))

# class SingleGroup(webapp2.RequestHandler):

#     def get(self, key):
#         # Preempt cycles
#         from event.models import get_building_str
#         group = None
#         if key and key != 'add':
#             group = Group.get_by_id(int(key))
#         if group:
#             groupjson = {
#                 "id": key,
#                 "nickname": group.nickname,
#                 "valid": True,
#                 "notnew": True
#             }
#             building_str = get_building_str(group.building)
#             groupjson.update({building_str: True})
#             triggers = []
#             for trigger in Trigger.query():
#                 triggerjson = {
#                     "nickname": trigger.nickname,
#                     "id": trigger.key.id(),
#                 }
#                 if trigger.key.id() in group.triggerids:
#                     triggerjson.update({"valid": True})
#                 else:
#                     triggerjson.update({"valid": False})
#                 triggers.append(triggerjson)
#             groupjson.update({"triggers": triggers})
#             final = {"group": groupjson}
#             template = JINJA_ENVIRONMENT.get_template('single_group.html')
#             self.response.write(template.render(final))
#         else:
#             final = {}
#             template = JINJA_ENVIRONMENT.get_template('404.html')
#             self.response.write(template.render(final))


# class SingleTrigger(webapp2.RequestHandler):
#     def get(self, key):
#         trigger = None
#         if key and key != 'add':
#             trigger = Trigger.get_by_id(int(key))
#         if trigger:
#             triggerjson = {
#                 "id": key,
#                 "nickname": trigger.nickname,
#                 "linktype": trigger.linktype,
#                 "triggerlink": trigger.triggerlink,
#                 "valid": True,
#                 "notnew": True,
#             }
#             groups = []
#             for group in Group.query():
#                 groupjson = {
#                     "nickname": group.nickname,
#                     "id": group.key.id()
#                 }
#                 if key in group.triggerids:
#                     groupjson.update({"valid": True})
#                 else:
#                     groupjson.update({"valid": False})
#                 groups.append(groupjson)
#             triggerjson.update({"groups": groups})
#         else:
#             triggerjson = {
#                 "nickname": None,
#                 "groups": None,
#                 "notnew": False,
#                 "valid": True,
#             }
#         final = {"trigger": triggerjson}
#         template = JINJA_ENVIRONMENT.get_template('single_trigger.html')
#         self.response.write(template.render(final))


class SingleAction(webapp2.RequestHandler):
    def post(self, key):
        actionid = self.request.get("id")
        nickname = self.request.get("nickname")
        type = self.request.get("type")
        description = self.request.get("description")
        payload = self.request.get("payload")
        try:
            keyid = int(actionid)
            action = Action.get_by_id(keyid)
        except Exception:
            action = None
        if action is None:
            action = Action(
                nickname=nickname,
                type=int(type),
                description=description,
                payload=payload
            )
            action.put()
        else:
            action.nickname = nickname
            action.type = int(type)
            action.description = description
            action.put()
        self.redirect("/actions")

    def get(self, key):
        action = None
        if key and key != 'add':
            try:
                action = Action.get_by_id(int(key))
            except:
                action = None
                self.redirect("/actions")
                return

        if action:
            rules = Rule.query(Rule.actionid == action.key)
            actionjson = {
                "nickname": action.nickname,
                "id": key,
                "type": action.type,
                "payload": action.payload,
                "description": action.description,
                "rules": rules
            }
        else:
            actionjson = {
                "nickname": None,
                "id": None,
                "type": None,
                "payload": None,
                "description": None,
                "rules": None
            }
        template = JINJA_ENVIRONMENT.get_template('single_action.html')
        self.response.write(template.render({'action': actionjson}))


class SingleRule(webapp2.RequestHandler):
    def post(self):
        pass

    def get(self, key):
        pass


class rulesJSON(webapp2.RequestHandler):
    def get(self):
        jsons = JSONDump.query()
        final = {}
        flag = True
        if jsons:
            for js in jsons:
                flag = False
                final = json.loads(js.jsondata)
        if flag:
            js = JSONDump(jsondata="[]")
            js.put()
            final = json.loads(js.jsondata)
        self.response.write(json.dumps(final))


class SingleBeacon(webapp2.RequestHandler):
    def get(self, key):
        beacon = None
        if key and key != 'add':
            try:
                beacon = Beacon.get_by_id(int(key))
            except:
                beacon = None
                self.redirect("/beacons")
                return

        if beacon:
            rules = []
            for rule in Rule.query():
                for sr in rule.rules:
                    if sr.beaconid == key:
                        rules.append(rule)
                        break
            beaconjson = {
                "nickname": beacon.nickname,
                "id": key,
                "uuid": beacon.uuid,
                "description": beacon.description,
                "rules": rules
            }
        else:
            beaconjson = {
                "nickname": None,
                "id": None,
                "uuid": None,
                "description": None,
                "rules": None
            }
        template = JINJA_ENVIRONMENT.get_template('single_beacon.html')
        self.response.write(template.render({'beacon': beaconjson}))

    def post(self, key):
        beaconid = self.request.get("id")
        nickname = self.request.get("nickname")
        beaconuuid = self.request.get("uuid")
        description = self.request.get("description")
        try:
            keyid = int(beaconid)
            beacon = Beacon.get_by_id(keyid)
        except Exception:
            beacon = None
        if beacon is None:
            beacon = Beacon(
                nickname=nickname,
                uuid=beaconuuid,
                description=description
            )
            beacon.put()
        else:
            beacon.nickname = nickname
            beacon.uuid = beaconuuid
            beacon.description = description
            beacon.put()
        self.redirect("/beacons")


class ListActions(webapp2.RequestHandler):
    def get(self):
        actions = Action.query()
        data = []
        for action in actions:
            rules = Rule.query().filter(Rule.actionid == action.key)
            beacons = []
            for rule in rules:
                for simplerule in rule.rules:
                    beacons.append(Beacon.query(key=simplerule.beaconid))
            data.append({
                'id': action.key.id(),
                'nickname': action.nickname,
                'type': action.type,
                'payload': action.payload,
                'description': action.description,
                'rules': rules,
                'beacons': beacons
                })

        template = JINJA_ENVIRONMENT.get_template('manage_actions.html')
        self.response.write(template.render({'actions': data}))


class ListRules(webapp2.RequestHandler):
    def get(self):

        # rules = Rule.query()
        rules = []
        [
            {
                'rule_id': 1,
                'action_id': 1,
                'priority': 1,
                'rules': [
                    {
                        'uuid': 'F4:20:ED:E3:8F:FB',
                        'distance': 1
                    },
                    {
                        'uuid': 'DA:94:8B:51:91:82',
                        'distance': 0
                    }
                ]
            },
            {
                'rule_id': 2,
                'action_id': 2,
                'priority': 2,
                'rules': [
                    {
                        'uuid': 'F4:20:ED:E3:8F:FB',
                        'distance': 1
                    },
                    {
                        'uuid': 'DE:54:21:58:C3:9C',
                        'distanc e': 0
                    }
                ]
            }
        ]
        data = []
        for rule in rules:
            data.append({
                'id': rule.key.id(),
                'nickname': rule.nickname,
                'description': rule.description,
                'rules': rule.rules
                })

        template = JINJA_ENVIRONMENT.get_template('manage_rules.html')
        self.response.write(template.render({'rules': data}))


class ListBeacons(webapp2.RequestHandler):
    def get(self):
        beacons = Beacon.query()
        beacondetails = []
        for beacon in beacons:
            valuepair = {'beaconid': beacon.key.id()}
            valuepair.update({'nickname': beacon.nickname})
            valuepair.update({'uuid': beacon.uuid})
            valuepair.update({'description': beacon.description})
            beacondetails.append(valuepair)
        final = {}
        final.update({'beacons': beacondetails})
        template = JINJA_ENVIRONMENT.get_template('manage_beacons.html')
        self.response.write(template.render(final))


# class AddBeacon(webapp2.RequestHandler):
#     def post(self):
#         beaconid = self.request.get("beaconid")
#         nickname = self.request.get("nickname")
#         beaconuuid = self.request.get("beaconuuid")
#         description = self.request.get("description")
#         try:
#             keyid = int(beaconid)
#             beacon = Beacon.get_by_id(keyid)
#         except Exception:
#             beacon = None
#         if beacon is None:
#             beacon = Beacon(
#                 nickname=nickname,
#                 uuid=beaconuuid,
#                 description=description
#             )
#             beacon.put()
#         else:
#             beacon.nickname = nickname
#             beacon.uuid = beaconuuid
#             beacon.description = description
#             beacon.put()
#         self.redirect("/beacons")

#     def get(self):
#         beaconjson = {
#             "valid": True,
#             "nickname": None,
#             "groups": None,
#             "notnew": False,
#         }
#         final = {"beacon": beaconjson}
#         template = JINJA_ENVIRONMENT.get_template('single_beacon.html')
#         self.response.write(template.render(final))


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
            beacons.append({
                "id": beacon.uuid,
                "nickname": beacon.nickname,
                "description": beacon.description
            })
        actions = []
        for action in Action.query():
            actions.append({
                "nickname": action.nickname,
                "description": action.description,
                "payload": action.payload,
                "type": action.type,
                "id": action.key.id()
                })
        rules = []
        jsons = JSONDump.query()
        for js in jsons:
            rules = json.loads(js.jsondata)
        data = {"beacons": beacons, "actions": actions, "rules": rules.rules}
        self.response.write(json.dumps(data))


class SampleData(webapp2.RequestHandler):
    def get(self):
        data = beacon_constants.SAMPLE_DATA
        json_data = json.dumps(data)
        self.response.write(json_data)
