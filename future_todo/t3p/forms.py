from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User,Group
from todo.models import Item, List
import datetime

def _get_task_list():
    lists = []
    for li in List.objects.filter(api_url=""):
        print [li.api_url]
        lists.append((li.id, li.name))
    return lists

class AddItemForm(forms.Form):
    title = forms.CharField(
                widget=forms.widgets.TextInput(attrs={'size':35})
                )

    due_date = forms.DateField(
                    required=False,
                    widget=forms.DateTimeInput(attrs={'class':'due_date_picker'})
                    )
    list = forms.ChoiceField(choices=_get_task_list())
    
    def save(self,user):
        get = self.cleaned_data.get
        item = Item(title=get('title'),
                    due_date=get('due_date'),
                    list=List.objects.get(pk=get('list')),
                    created_by=user,
                    assigned_to=user,
                    )
        item.save()
        return item
