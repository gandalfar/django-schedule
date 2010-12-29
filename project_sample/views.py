from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.models import User

import simplejson
from schedule.models import *
import datetime

def ajax(request):
    calendar = get_object_or_404(Calendar, slug='example')
    method = request.GET.get('method')
    get = request.POST.get
    
    if method == 'list':
        data = []
        for event in calendar.event_set.all():
            e = [event.id,
                 event.title,
                 event.start.strftime("%m/%d/%Y %H:%M"),
                 event.end.strftime("%m/%d/%Y %H:%M"),
                 0,
                 0,
                 0,
                 8,
                 1,
                 'somewhere',
                 event.description
            ]
            data.append(e)
    
        json = simplejson.dumps({'events': data})
    elif method == 'add':
        # {u'CalendarEndTime': [u'12/29/2010 10:30'], u'IsAllDayEvent': [u'0'], u'CalendarStartTime': [u'12/29/2010 10:00'], 
        #  u'CalendarTitle': [u'test'], u'timezone': [u'1']
        e = Event(calendar=calendar,
                  creator=User.objects.get(pk=1),
                  start=datetime.datetime.strptime(get('CalendarStartTime'), '%m/%d/%Y %H:%M'),
                  end=datetime.datetime.strptime(get('CalendarEndTime'), '%m/%d/%Y %H:%M'),
                  title=get('CalendarTitle')
        )
        e.save()
        data = {'IsSuccess': True,
                'Msg': 'add success',
                'Data': e.id
               }
        json = simplejson.dumps(data)
    elif method == 'update':
        event = Event.objects.get(pk=get('calendarId'))
        event.start = datetime.datetime.strptime(get('CalendarStartTime'), '%m/%d/%Y %H:%M')
        event.end = datetime.datetime.strptime(get('CalendarEndTime'), '%m/%d/%Y %H:%M')
        event.save()
        
        data = {'IsSuccess': True,
                'Msg': 'update was successful',
                }
        json = simplejson.dumps(data)
    elif method == 'remove':
        event = Event.objects.get(pk=get('calendarId'))
        event.delete()
        data = {'IsSuccess': True,
        'Msg': 'removed!',
        }
        json = simplejson.dumps(data)
    else:
        print request.GET
        print request.POST
    
    return HttpResponse(json, {})