from event.views import *

urlconfs = [
    ('/events/all', FetchEvents),
    ('/events/(.+)/beacons', FetchBeaconsForEvent),
    ('/events/(.+)', SingleEvent),
    ('/addevent', AddEvent),
]
