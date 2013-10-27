#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import webapp2
from google.appengine.ext import db
import json
import os
from google.appengine.ext.webapp import template

TRIGGER_IMMEDIATE = 0
TRIGGER_NEAR = 1
TRIGGER_FAR = 2
LINK_IMAGE = 0
LINK_VIDEO = 1
LINK_ADVERT = 2
LINK_COUPON = 3


def render_template(self,template_name,template_values):
	path = os.path.join(os.path.dirname(__file__), template_name)
	self.response.out.write(template.render(path+'.html', template_values))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Beacon Dev Backend')

class Beacon(db.Model):
	nickname = db.StringProperty()
	beaconuuid = db.StringProperty()
	groupids = db.ListProperty(int)
	description = db.TextProperty()

class Group(db.Model):
	nickname = db.StringProperty()
	triggerids = db.ListProperty(int)
	description = db.TextProperty()
	triggertype = db.IntegerProperty() # 0 for immediate, 1 for near and 2 for far

class Trigger(db.Model):
	nickname = db.StringProperty()
	linktype = db.IntegerProperty() # 0 for image, 1 for video, 2 for advert, 3 for coupon
	description = db.StringProperty()
	triggerlink = db.StringProperty()

#class SingleBeacon(webapp2.RequestHandler):
	

#class SingleGroup(webapp2.RequestHandler):


#class SingleTrigger(webapp2.RequestHandler):
	

class ListBeacons(webapp2.RequestHandler):
	def get(self):
		beacons = Beacon.all()
		beacondetails = []
		triggers=[]
		for beacon in beacons:
			valuepair = {}
			valuepair.update({'nickname':beacon.nickname})
			valuepair.update({'beaconuuid':beacon.beaconuuid})
			gs=beacon.groupids
			groups=[]
			for g in gs:
				group={}
				gdb=Group.get_by_id(int(g))
				group.update({'nickname':gdb.nickname})
				group.update({'id':g})
				for t in gdb.triggerids:
					tdb=Trigger.get_by_id(int(t))
					trig={}
					trig.update({'nickname':tdb.nickname,'id':t})
					triggers.append(trig)
				groups.append(group)

			valuepair.update({'groups':groups})
			valuepair.update({'triggers':triggers})
			valuepair.update({'description':beacon.description})
			beacondetails.append(valuepair)
		final = {}
		final.update ({'beacons':beacondetails})
		render_template(self,'manage_beacons',final)

class AddBeacon(webapp2.RequestHandler):
	def post(self):
		beaconid = self.request.get("beaconid")
		nickname = self.request.get("nickname")
		beaconuuid= self.request.get("beaconuuid")
		groupid = self.request.get_all("groupid")
		groupids=[]
		for g in groupid:
			groupids.append(int(g))
		description = self.request.get("description")
		try:
			keyid=int(beaconid)
			beacon = Beacon.get_by_id(keyid)
		except Exception, e:
			beacon = None
		if beacon == None:
			beacon = Beacon(nickname = nickname, beaconuuid = beaconuuid, groupids = groupids, description = description)
			beacon.put()
		else:
			beacon.nickname=nickname
			beacon.beaconuuid=beaconuuid
			beacon.groupids=groupids
			beacon.description=description
			beacon.put()
		self.response.write("Success")

class ListGroups(webapp2.RequestHandler):
	def get(self):
		groups = Group.all()
		groupdetails=[]
		for group in groups:
			valuepair={}
			valuepair.update({'nickname':group.nickname,'description':group.description})
			beacons = Beacon.all()
			grpbea = []
			for beacon in beacons:
				if group.key().id() in beacon.groupids:
					beavp = {}
					beavp.update({'id':beacon.key().id(),'nickname':beacon.nickname})
					grpbea.append(beavp)
			grptri=[]
			for grtri in group.triggerids:
				trigger = Trigger.get_by_id(grtri)
				trivp={}
				trivp.update({'id':grtri,'nickname':trigger.nickname})
				grptri.append(trivp)
			valuepair.update({'beacons':grpbea,'triggers':grptri})
			groupdetails.append(valuepair)
		final = {'groups':groupdetails}
		render_template(self,'manage_groups',final)

					

class AddGroup(webapp2.RequestHandler):
	def post(self):
		groupid = self.request.get("groupid")
		nickname = self.request.get("nickname")
		ts = self.request.get_all("triggerid")
		beaconids=[]
		triggerids=[]
		for t in ts:
			triggerids.append(int(t))
		description = self.request.get("description")
		try:
			keyid=int(groupid)
			group = Group.get_by_id(keyid)
		except Exception, e:
			group = None
		if group == None:
			group = Group(nickname = nickname, description = description, triggerids=triggerids)
			group.put()
		else:
			group.nickname=nickname
			group.triggerids=triggerids
			group.description=description
			group.put()
		self.response.write("Success")


class ListTriggers(webapp2.RequestHandler):
	def get(self):
		triggers = Trigger.all()
		triggerdetails = []
		for trigger in triggers:
			valuepair = {}
			valuepair.update({'linktype':trigger.linktype})
			valuepair.update({'triggerlink':trigger.triggerlink})
			triggerdetails.append(json.dumps(valuepair))
		finaltriggerjson = {}
		finaltriggerjson.update ({'triggers':triggerdetails})
		self.response.write(finaltriggerjson)


class AddTrigger(webapp2.RequestHandler):
	def post(self):
		triggerid = self.request.get("triggerid")
		nickname = self.request.get("nickname")
		description = self.request.get("description")
		trigtype = self.request.get("type")
		triglink = self.request.get("link")
		try:
			keyid=int(triggerid)
			trigger = Trigger.get_by_id(keyid)
		except Exception, e:
			trigger = None
		if trigger == None:
			trigger = Trigger(nickname = nickname, description = description, triggerlink=triglink, triggertype=trigtype )
			trigger.put()
		else:
			trigger.nickname=nickname
			trigger.description=description
			trigger.triggertype=trigtype
			trigger.triggerlink=triglink
			trigger.put()
		self.response.write("Success")

class TestTemplate(webapp2.RequestHandler):
	def get(self):
		values={}
		groups=[{'id':'1213','nickname':'Fiction','valid':False},{'id':'1431','name':'Entrance'}]
		triggers=[{'id':'1213','nickname':'Discount'},{'id':'1213','name':'New Dan Brown'}]
		beacons=[{'nickname':'Awesome Beacon #1','description':'Some description here','groups':groups,'grouptriggers':triggers},
		{'nickname':'Awesome Beacon #2','description':'Some description here','groups':triggers,'grouptriggers':groups}]
		#values.update({
		#	'beacons':beacons
		#	})
		beacon={'valid':True,'notnew':True, 'nickname':'beacon 1','uuid':'1213123','groups':groups,'id':5136918324969472}
		values={'beacon':beacon}
		render_template(self,'single_beacon',values)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    #('/beacons/(.*)',SingleBeacon),
    #('/groups/(.*)',SingleGroup),
    #('/triggers/(.*)',SingleTrigger),
    ('/triggers/add',AddTrigger),
    ('/groups/add',AddGroup),
    ('/beacons/add',AddBeacon),
    ('/beacons',ListBeacons),
    ('/groups',ListGroups),
    ('/triggers',ListTriggers),
    ('/test',TestTemplate)
], debug=True)
