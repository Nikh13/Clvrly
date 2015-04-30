import json
import os

from datetime import datetime, timedelta

from google.appengine.ext.webapp import template

from beacon.models import Beacon, Group, Trigger
from event.models import Event, Building, get_building_obj
from utils import JINJA_ENVIRONMENT

import webapp2


# /events/all
class FetchEvents(webapp2.RequestHandler):
    def post(self):
        latitude = self.request.POST.get('latitiude')
        longitude = self.request.POST.get('longitude')
        events = Event.query()
        events = list(events)
        response_dict = json.loads({'events': events})
        self.response.headers['Content-Type'] = 'application/json'
        return self.response.out.write(resposne)

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
        name = self.request.POST.get('name')
        time = self.request.POST.get('datetime')
        building = self.request.POST.get('building')
        kwargs = {
            'name': name,
            'time': datetime.strptime(time, "%d/%m/%Y"),
            'building' : get_building_obj(building),
        }
        event = Event(**kwargs)
        event.put()
        self.redirect("/events/all")

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('add_event.html')
        ctx = {}
        self.response.write(template.render(ctx))
