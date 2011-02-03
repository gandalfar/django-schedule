"""
Tracks (Doing Things Properly) - http://www.getontracks.org/ modul
for T3P / Future TODO.

Documentation: http://your-tracks-url.tld/integrations/rest_api

Return XML for Tracks 1.7 looks like this

<todos type="array">
  <todo>
    <completed-at type="datetime" nil="true"></completed-at>
    <context-id type="integer">6</context-id>
    <created-at type="datetime">2009-10-22T15:12:07+02:00</created-at>
    <description>Foobar</description>
    <due type="datetime" nil="true"></due>
    <id type="integer">23</id>
    <notes></notes>
    <project-id type="integer" nil="true"></project-id>
    <recurring-todo-id type="integer" nil="true"></recurring-todo-id>
    <show-from type="datetime" nil="true"></show-from>
    <state>active</state>
    <updated-at type="datetime">2010-08-27T14:15:00+02:00</updated-at>
  </todo>
  ...
</todos>
"""

__version__ = "0.0.1"
__authors__ = [
    "lowk3y",
]

from future_todo.t3p.views import plugin, plugin_handler
import string, datetime, os, sys
import httplib
import base64
import urllib
import urllib2
try:
    from elementtree import ElementTree as ET
except:
    import xml.etree.ElementTree as ET


##sys.path.append('../../')
##sys.path.append('../')
##os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

"""
HINT: be sure to have in localsettings something like:

import os
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
DATABASE_NAME = here('project_sample.db') 


"""
##os.environ['DJANGO_SETTINGS_MODULE'] = 'future_todo.localsettings'

from django.conf import settings
from django.db import models
from django.forms.models import ModelForm
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User,Group
from todo.models import Item, User, List, Comment, Effort


class tracksplugin(plugin):
    """Concrete class for foo plugin."""

        
    def getFeed(self,list):
        url = "%s/todos.xml" % (list.api_url)
        # debug
        print "URL:%s" % url
        
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, list.api_username, list.api_password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        feed = urllib2.urlopen(url)
        return feed
        
    def getExternalTasks(self,feed):
        tree = ET.parse(feed)
        Tasks = tree.findall("todo")
        # debug
        print "Found %s tasks" % len(Tasks)
        return Tasks
    
    #def getDate(self, 
    #    
    
    def updateItem(self, item):
        pass
        
    def MatchItems(self,list):
        Tasks = self.getExternalTasks(self.getFeed(list))
        for task in Tasks:
            """ http://www.djangoproject.com/documentation/models/get_or_create/ """
            #item = Item.objects.get(list=list, ext_id=task.find("id").text)
            if Item.objects.filter(list=list, ext_id=task.find("id").text).count() > 0:
                print "%s %s objekt obstaja" % (task.find("id").text, task.find("description").text)
                """ let's update objects """
                self.updateItem(Item.objects.get(list=list, ext_id=task.find("id").text))
            else:
                print "%s %s ne obstaja" % (task.find("id").text, task.find("description").text)
                ## FIXME!! FIXME!! FIXME!!
                #task.find("due").text
                #created_date=task.find("created-at").text,
                #
                #
                
                """     
                FIXME: This is borken way, just pr0f of concept; that's why we expect
                auth.user with username = "a". Workaround will be needed
                    
                TODO: at the moment inseting
                
                due_date=task.find("due").text into new objects
                    
                brakes smtg, because of br0ken string in source or
                smtg.
                """
                
                user = User.objects.all().order_by('id')[0]
                
                ##print "%s %s" % (task.find("id").text, task.find("due").text)
                ##print task.find("due").text
                
                """
                FIXME:  Need to parse original dates from XML into django/pyhon
                        format, just when it's needed.
                """
                
                if task.find("due").text == "":
                    new = Item(title=task.find("description").text,list=list,
                    ext_id=task.find("id").text,
                    created_date=task.find("created-at").text, created_by=user, 
                    assigned_to=user, priority=999)
                else:
                    new = Item(title=task.find("description").text,list=list,
                    ext_id=task.find("id").text,
                    created_date=task.find("created-at").text, created_by=user, 
                    assigned_to=user, priority=999)
                
                ## Some debugging about date
                self.log.append("0: %s  <br>" % (new.title))
                self.log.append("1: %s  %s<br>" % (task.find("due").text, new.due_date))
                self.log.append("2: %s  %s<br>" % (task.find("created-at").text, new.created_date))
                
                """ 
                FIXME:  when saved create_date will be changed to now(), since
                default self.save method is defined that way. In future we might 
                need a workaround
                """
                
                #new.altsave()
                new.save() 
                
    def __init__(self, list):
        print "Initializing Tracks plugin"
        self.list = list
        self.log = []
        
    def run(self):
        #do something here
        list = self.list
        self.MatchItems(list)
        self.log.append("You called me with: %s, %s, %s, %s" % (list.api_url, list.api_username, list.api_password, list.api_token))
        return self.log
        
    name = "tracks"
    description = "Plugin for Tracks 1.7.x (http://www.getontracks.org/)"

plugin_handler.register_plugin(tracksplugin)
