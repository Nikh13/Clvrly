import json
import os

from datetime import datetime, timedelta

from beacon.models import Beacon, Group, Trigger
from event.models import Event, Building, get_building_obj
from event.models import get_building_str
from utils import JINJA_ENVIRONMENT

import webapp2


# /events/all
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
        events = Event.query()
        events = list(events)
        template = JINJA_ENVIRONMENT.get_template('manage_events.html')
        ctx = {'events': events}
        self.response.write(template.render(ctx))


# /events/{event}/beacons
class FetchBeaconsForEvent(webapp2.RequestHandler):
    def get(self, event_slug):
        pass


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
            self.redirect("/events/all")
        else:
            event.name = name
            event.time = datetime.strptime(time, "%d/%m/%Y %H:%M:%S")
            event.building =  get_building_obj(building)
            event.put()
            self.redirect('/events/all')

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
