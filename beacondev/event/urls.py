from beacon.views import *

urlconfs = [
    ('/events/all', FetchEvents),
    ('/events/(.+)/beacons', FetchBeaconsForEvent),
]
