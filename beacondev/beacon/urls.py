from views import *

urlconfs = [
    ('/addtrigger', AddTrigger),
    ('/addgroup', AddGroup),
    ('/addbeacon', AddBeacon),
    ('/beacons/(.*)', SingleBeacon),
    ('/groups/(.*)', SingleGroup),
    ('/triggers/(.*)', SingleTrigger),
    ('/beacons', ListBeacons),
    ('/groups', ListGroups),
    ('/triggers', ListTriggers),
    ('/test', TestTemplate),
    ('/api/all', DumpData)
]
