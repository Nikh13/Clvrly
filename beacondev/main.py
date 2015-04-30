#######################################
#     Cleverly Beacon Backend     #
#######################################


import os

from os.path import dirname, join

from beacon.urls import urlconfs as beacon_urls
from event.urls import urlconfs as event_urls

from utils import JINJA_ENVIRONMENT

import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('base.html')
        ctx = {}
        self.response.write(template.render(ctx))


url_confs = [
    ('/', MainHandler),
]

url_confs.extend(beacon_urls)
url_confs.extend(event_urls)

app = webapp2.WSGIApplication(url_confs, debug=True)
