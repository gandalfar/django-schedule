#!/usr/bin/python -w
''''
Example
 
In list
 api_url = http://tracks.frubsd.org
 api_username = XXXX
 api_password = YYYY

'''

import string, datetime, os, sys
import httplib
import base64
import urllib
import urllib2

try:
    from elementtree import ElementTree as ET
except:
    import xml.etree.ElementTree as ET

sys.path.append('../../')
sys.path.append('../')
##os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

"""
HINT: be sure to have in localsettings something like:

import os
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
DATABASE_NAME = here('project_sample.db') 


"""
os.environ['DJANGO_SETTINGS_MODULE'] = 'future_todo.localsettings'

from django.conf import settings
from django.db import models
from django.forms.models import ModelForm
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User,Group
from todo.models import Item, User, List, Comment, Effort


""" Method that gets the XML feed via API
    FIXME: This need to be unifed 
"""
def getFeed(workingList):
    url = "%s/todos.xml" % (workingList.api_url)
    
    # debug
    print "URL:%s" % url
    
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # this creates a password manager
    passman.add_password(None, url, workingList.api_username, workingList.api_password)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which `theurl` is a super-url

    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler

    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    # All calls to urllib2.urlopen will now use our handler
    # Make sure not to include the protocol in with the URL, or
    # HTTPPasswordMgrWithDefaultRealm will be very confused.
    # You must (of course) use it when fetching the page though.

    feed = urllib2.urlopen(url)
    # authentication is now handled automatically for us
    return feed
    
"""
Get tasks out of XML feed. Basic TODO XML for tracks looks like this

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

def getExternalTasks(feed):
    tree = ET.parse(feed)
    Tasks = tree.findall("todo")
    # debug
    print "Found %s tasks" % len(Tasks)
    return Tasks
    
def MatchItems(workingList):
    Tasks = getExternalTasks(getFeed(workingList))
    for task in Tasks:
        """ http://www.djangoproject.com/documentation/models/get_or_create/ """
        #item = Item.objects.get(list=workingList, ext_id=task.find("id").text)
        if Item.objects.filter(list=workingList, ext_id=task.find("id").text).count() > 0:
            #print "%s %s objekt obstaja"
            """ let's update objects """
            update(Item.objects.get(list=workingList, ext_id=task.find("id").text))
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
            
            new = Item(title=task.find("description").text,list = workingList, 
                       created_date=task.find("created-at").text, created_by=user, 
                       assigned_to=user, priority=999)
            
            ## Some debugging about date
            print "0: %s " % (new.title)
            print "1: %s\t\t%s" % (task.find("due").text, new.due_date)
            print "2: %s\t\t%s" % (task.find("created-at").text, new.created_date)
            
            """ 
            FIXME:  when saved create_date will be changed to now(), since
            default self.save method is defined that way. In future we might 
            need a workaround
            """
            
            new.save()
            


for seznam in List.objects.all():
    print seznam
    MatchItems(seznam)


def updateItem(item):
    ''' TODO '''
    pass

