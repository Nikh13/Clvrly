from event.views import *

urlconfs = [
    ('/api/events', FetchEvents),
    ('/events', ListEvents),
    ('/event/(.+)/beacons', FetchBeaconsForEvent),
    ('/events/(.+)', SingleEvent),
    ('/addevent', AddEvent),
]
