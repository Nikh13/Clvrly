from beacon.views import *

urlconfs = [
    # ('/addtrigger', AddTrigger),
    # ('/addgroup', AddGroup),
    ('/beacon/(.*)', SingleBeacon),
    ('/action/(.*)', SingleAction),
    ('/rule/(.*)', SingleRule),
    # ('/groups/(.*)', SingleGroup),
    # ('/triggers/(.*)', SingleTrigger),
    ('/beacons', ListBeacons),
    ('/actions', ListActions),
    ('/rules', ListRules),
    # ('/groups', ListGroups),
    # ('/triggers', ListTriggers),
    ('/test', TestTemplate),
    ('/api/all', DumpData),
    ('/api/sample', SampleData),
    ('/jsonrule', rulesJSON)
]
