import json
import os

from datetime import datetime, timedelta

from beacon.models import Beacon, Group, Trigger
from event.models import Event, Building, get_building_obj
from event.models import get_building_str
from utils import JINJA_ENVIRONMENT
from utils import AJAX_OK, AJAX_ERROR

import webapp2


# /api/events/
class FetchEvents(webapp2.RequestHandler):
    def post(self):
        latitude = self.request.POST.get('latitiude')
        longitude = self.request.POST.get('longitude')
        events = Event.query()
        events = list(events)
        response_dict = json.dumps({'events': events})
        self.response.headers['Content-Type'] = 'application/json'
        return self.response.out.write(response_dict)

    def get(self):
        events = Event.query().fetch()
        ctx = {}
        events = map(lambda d: d.to_dict(), events)
        for event in events:
            event_time = event.pop('time').strftime("%d/%m/%Y %H:%M:%S")
            event_building = get_building_str(event.pop('building'))
            event['time'] = event_time
            event['building'] = get_building_str(event_building)

        ctx = {'events': events}
        self.response.headers['Content-Type'] = 'application/json'
        return self.response.out.write(json.dumps(ctx))


# /events
class ListEvents(webapp2.RequestHandler):
    def get(self):
        events = Event.query().fetch
        events = list(events)
        template = JINJA_ENVIRONMENT.get_template('manage_events.html')
        ctx = {'events': events}
        self.response.write(template.render(ctx))


# /events/{event}/beacons
class FetchBeaconsForEvent(webapp2.RequestHandler):
    def get(self, event_slug):
        print event_slug
        event = Event.query(Event.name == event_slug).fetch()
        event = event[0]
        ctx = {}
        if not event:
            ctx.update({
                'status': AJAX_ERROR,
            })
            response_dict = json.dumps(ctx)
            self.response.write(response_dict)
            return
        print event
        event_building = event.building

        # get all groups of beacons in the building.
        groups = Group.query(Group.building == event_building).fetch()

        # Map all the beacons according to the groups they belong
        groupids = map(lambda d: (d.key.id(), d.nickname), groups)
        groupid_dict = dict((x, y) for x, y in groupids)
        beacons = Beacon.query(Beacon.groupids.IN(groupid_dict.keys())).fetch()

        groups_dict = {}
        # Beacons store ids, hence such a complex proces.
        # Key Property would have solved the issue but nevertheless fuck it.
        for beacon in beacons:
            groups_of_beacon = beacon.groupids
            for id in groups_of_beacon:
                if not groups_dict.get(groupid_dict[id]):
                    groups_dict.update({
                        groupid_dict[id]: [beacon.to_dict()]
                    })
                else:
                    beacons_in_group = groups_dict[groupid_dict[id]]
                    beacons_in_group.append(beacon.to_dict())
                    groups_dict[groupid_dict[id]] = beacons_in_group
        event = event.to_dict()
        building = event.pop('building')
        event_building = get_building_str(building)
        event_time = event.pop('time')
        event_time = event_time.strftime("%d/%m/%Y %H:%M:%S")
        event['time'] = event_time,
        event['building'] = event_building
        ctx.update({
            'status': AJAX_OK,
            'groups_of_beacons': groups_dict,
            'event': event,
        })
        json_response = json.dumps(ctx)
        self.response.headers['Content-Type'] = 'application/json'
        return self.response.out.write(json_response)


class AddEvent(webapp2.RequestHandler):
    def post(self):
        eventid = self.request.POST.get('eventid')
        name = self.request.POST.get('name')
        time = self.request.POST.get('datetime')
        building = self.request.POST.get('building')
        kwargs = {
            'name': name,
            'time': datetime.strptime(time, "%d/%m/%Y %H:%M:%S"),
            'building': get_building_obj(building),
        }
        event = None
        if eventid:
            event = Event.get_by_id(int(eventid))
        if not event:
            event = Event(**kwargs)
            event.put()
            self.redirect("/events")
        else:
            event.name = name
            event.time = datetime.strptime(time, "%d/%m/%Y %H:%M:%S")
            event.building = get_building_obj(building)
            event.put()
            self.redirect('/events')

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('add_event.html')
        ctx = {}
        self.response.write(template.render(ctx))


class SingleEvent(webapp2.RequestHandler):
    def get(self, key):
        event = None
        if key and key != 'add':
            event = Event.get_by_id(int(key))
        if event:
            ctx = {
                'event': event,
            }
            building_str = get_building_str(event.building)
            ctx.update({building_str: True})
            template = JINJA_ENVIRONMENT.get_template('single_event.html')
            self.response.write(template.render(ctx))
        else:
            ctx = {}
            template = JINJA_ENVIRONMENT.get_template('404.html')
            self.response.write(template.render(ctx))
