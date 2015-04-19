import json
import os

from google.appengine.ext.webapp import template

from beacon.models import Beacon, Group, Trigger

from event.models import Event

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

# /events/{event}/beacons
class FetchBeaconsForEvent(webapp2.RequestHandler):
    def get(self, event_slug):
        pass
