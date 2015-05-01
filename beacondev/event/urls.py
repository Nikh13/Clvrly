from event.views import *

urlconfs = [
    ('/events/all', FetchEvents),
    ('/event/(.+)/beacons', FetchBeaconsForEvent),
    ('/events/(.+)', SingleEvent),
    ('/addevent', AddEvent),
]
