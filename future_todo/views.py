from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import simplejson
import datetime

from schedule.models import *

from todo.models import Item, List, Comment
from todo.forms import AddListForm, AddItemForm, EditItemForm, AddExternalItemForm, SearchForm
from todo.forms import AddItemEventForm

from pytz import timezone
from babel.dates import format_datetime
from django.conf import settings
from time import localtime

from t3p.forms import AddItemForm

from t3p.views import plugin_handler

tz = timezone(settings.TIME_ZONE)

@login_required
def ajax(request):
    #calendar = get_object_or_404(Calendar, pk=1)
    #calendar = Calendar.objects.get_or_creat
    try:
        calendar = Calendar.objects.all()[0]
    except:
        calendar = Calendar(name='calendar', slug='calendar')
        calendar.save()
        
    method = request.GET.get('cmd')
    get = request.GET.get

    if method == 'read':
        data = []
        for event in calendar.event_set.all():
            e = {'id': event.id,
                 'title': event.title,
                 'start': tz.localize(event.start).isoformat(),
                 'end': tz.localize(event.end).isoformat(),
                 'allDay': False,
                }
            data.append(e)
        json = simplejson.dumps(data)
        
    elif method == 'create':
        if get('itemId'):
            item = Item.objects.get(pk=get('itemId'))
        else:
            item = None
        e = Event(calendar=calendar,
                  creator=User.objects.get(pk=1),
                  start=datetime.datetime.fromtimestamp(int(get('start'))),
                  end=datetime.datetime.fromtimestamp(int(get('end'))),
                  title=get('title'),
                  item=item
        )
        e.save()
        data = e.id
        json = simplejson.dumps(data)
        
    elif method == 'updatePos':
        event = Event.objects.get(pk=get('id'))
        event.start = datetime.datetime.fromtimestamp(int(get('start')))
        event.end = datetime.datetime.fromtimestamp(int(get('end')))
        event.save()
        
        data = event.id
        json = simplejson.dumps(data)
    
    elif method == 'updateTitle':
        event = Event.objects.get(pk=get('id'))
        event.title = get('title')
        event.save()
        
        data = event.id
        json = simplejson.dumps(data)

    
    elif method == 'delete':
        event = Event.objects.get(pk=get('id'))
        event.delete()
        json = simplejson.dumps('')
    else:
        print request.GET
        print request.POST
    
    return HttpResponse(json, {})
    
@login_required
def task_add(request):
    if request.POST:
        add_item_form = AddItemForm(request.POST.copy())
        if add_item_form.is_valid():
            form = add_item_form.save(request.user)
            return HttpResponseRedirect('/#list-%s' % form.list.id)
    
@login_required
def index(request):
    items = Item.objects.filter(assigned_to=request.user, completed=0)
    
    item_event_form = AddItemEventForm()
    add_item_form = AddItemForm()
    
    
    context = {'items': items,
               'item_event_form': item_event_form,
               'add_item_form': add_item_form
              }
    return render_to_response('index.html', context, 
                              context_instance=RequestContext(request))
                              
def plugins(request):
    plugins_list = plugin_handler.get_plugins()
    lists = List.objects.all()
        
    context = {'plugins_list': plugins_list,
               'lists': lists}
    return render_to_response('plugins.html', context, 
                              context_instance=RequestContext(request))


def list_run(request, list_id):
    mylist = get_object_or_404(List, pk=list_id)
    
    output = 'No plugin with this name found. Expected: %s' % mylist.api_engine
    plugin_list = plugin_handler.get_plugins()
    
    for plugin in plugin_list:
        if plugin.name == mylist.api_engine:
            output = plugin(mylist).run()
    
    context = {'output': output}
    return render_to_response('list_run.html', context, 
                              context_instance=RequestContext(request))

    