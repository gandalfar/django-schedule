from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User,Group
from todo.models import Item, List
import datetime

from schedule.models.events import Event
from schedule.models.calendars import Calendar

class AddItemEventForm(forms.Form):
    event_start = forms.DateField(required=True,
                                  widget=forms.DateTimeInput(attrs={'class':'due_date_picker'})
                  )
                  
                  
    def save(self, *args, **kwargs):
        get = self.cleaned_data.get
        print get('event_start')
        
        item = Item.objects.get(pk=kwargs['task_id'])
        
        calendar = Calendar.objects.get(slug='example')
        
        d = get('event_start')
        start_date = datetime.datetime(d.year, d.month, d.day, 8)
        end_date = datetime.datetime(d.year, d.month, d.day, 9)
        e = Event(calendar=calendar,
          creator=User.objects.get(pk=1),
          start=start_date,
          end=end_date,
          title=item.title,
          item=item
        )
        e.save()

class AddListForm(ModelForm):    
    # The picklist showing allowable groups to which a new list can be added
    # determines which groups the user belongs to. This queries the form object
    # to derive that list.
    def __init__(self, user, *args, **kwargs):
        super(AddListForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(user=user)

    class Meta:
        model = List
        
 
        
class AddItemForm(ModelForm):
    
    # The picklist showing the users to which a new task can be assigned
    # must find other members of the groups the current list belongs to.
    def __init__(self, task_list, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        # print dir(self.fields['list'])
        # print self.fields['list'].initial
        self.fields['assigned_to'].queryset = User.objects.filter(groups__in=[task_list.group])
            
    due_date = forms.DateField(
                    required=False,
                    widget=forms.DateTimeInput(attrs={'class':'due_date_picker'})
                    )
                    
    title = forms.CharField(
                    widget=forms.widgets.TextInput(attrs={'size':35})
                    ) 

    class Meta:
        model = Item
        


class EditItemForm(ModelForm):

    # The picklist showing the users to which a new task can be assigned
    # must find other members of the groups the current list belongs to.
    def __init__(self,  *args, **kwargs):
        super(EditItemForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(groups__in=[self.instance.list.group])

    class Meta:
        model = Item
        exclude = ('created_date','created_by',)             
        

        
class AddExternalItemForm(ModelForm):
    """Form to allow users who are not part of the GTD system to file a ticket."""

    title = forms.CharField(
                    widget=forms.widgets.TextInput(attrs={'size':35})
                    ) 
    note = forms.CharField (
        widget=forms.widgets.Textarea(),
        help_text='Foo',
        )
    
    class Meta:
        model = Item
        exclude = ('list','created_date','due_date','created_by','assigned_to',)
        


class SearchForm(ModelForm):
    """Search."""

    q = forms.CharField(
                    widget=forms.widgets.TextInput(attrs={'size':35})
                    ) 


