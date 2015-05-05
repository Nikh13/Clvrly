TRIGGER_IMMEDIATE = 0
TRIGGER_NEAR = 1
TRIGGER_FAR = 2
LINK_IMAGE = 0
LINK_VIDEO = 1
LINK_ADVERT = 2
LINK_COUPON = 3
SAMPLE_DATA = {
    'beacons':[
            {
                'uuid':'DE:54:21:58:C3:9C',
                'nickname':'Dark Blue',
                'description': 'desc 1'
            },
            {
                'uuid':'DA:94:8B:51:91:82',
                'nickname':'Green',
                'description': 'desc 2'
            },
            {
                'uuid':'F4:20:ED:E3:8F:FB',
                'nickname':'Light Blue',
                'description': 'desc 3'
            }
    ],
    'actions':[
        {
            'action_id': 1,
            'description': 'desc 1',
            'type': 0,
            'payload': 'hello there'
        },
        {
            'action_id': 2,
            'description': 'desc 1',
            'type': 1,
            'payload': 'good bye'
        }
    ],
    'rules': [
        {
            'rule_id': 1,
            'action_id': 1,
            'priority': 1,
            'rules': [
                        {
                            'uuid':'F4:20:ED:E3:8F:FB',
                            'distance': 1
                        },
                        {
                            'uuid':'DA:94:8B:51:91:82',
                            'distance': 0
                        }
            ]
        },
        {
            'rule_id': 2,
            'action_id': 2,
            'priority': 2,
            'rules': [
                        {
                            'uuid':'F4:20:ED:E3:8F:FB',
                            'distance': 1
                        },
                        {
                            'uuid':'DE:54:21:58:C3:9C',
                            'distance': 0
                        }
            ]
        }
    ]
}
