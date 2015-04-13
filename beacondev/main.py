#######################################
#     Cleverly Beacon Backend     #
#######################################


from beacon.urls import urlconfs as beacon_urls

import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Beacon Dev Backend')


url_confs = [
    ('/', MainHandler),
]

url_confs.extend(beacon_urls)

app = webapp2.WSGIApplication(url_confs, debug=True)
