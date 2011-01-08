from django.db import models
from django.forms.models import ModelForm
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User,Group
import string, datetime
from django.template.defaultfilters import slugify

class List(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60,editable=False)
    # slug = models.SlugField(max_length=60)
        
    # Users in same group can see same lists
    group = models.ForeignKey(Group)
    
    # Owner of the list (the one can change settings)
    owner = models.ForeignKey(User)
    
    # API Engine (at the moment engines are stored as interger values
    # but we need to figure it out, how this field can be more optimized
    # in future use.
    api_engine = models.IntegerField(blank=True, null=True)
    api_url = models.CharField(max_length=60, blank=True, null=True )
    api_username = models.CharField(max_length=60, blank=True, null=True)
    api_password = models.CharField(max_length=60, blank=True, null=True)
    api_token = models.CharField(max_length=60, blank=True, null=True)
    
    # Cross URL works same as interwiki urls - to simple redict
    # tasks to customers IT. 
    # ex. http://tracks.frubsd.org/?$id
    cross_url = models.CharField(max_length=60, blank=True, null=True)
    list_colour = models.CommaSeparatedIntegerField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(List, self).save(*args, **kwargs)

    

    def __unicode__(self):
        return self.name
        
    # Custom manager lets us do things like Item.completed_tasks.all()
    objects = models.Manager()
    
    def incomplete_tasks(self):
        # Count all incomplete tasks on the current list instance
        return Item.objects.filter(list=self,completed=0)
        
    class Meta:
        ordering = ["name"]        
        verbose_name_plural = "Lists"
        
        # Prevents (at the database level) creation of two lists with the same name in the same group
        unique_together = ("group", "slug")
        
        


        
class Item(models.Model):
    title = models.CharField(max_length=140)
    
    # For tracking external ID of task in external tasks tracking
    # application
    ext_id = models.IntegerField(blank=True, null=True)
    
    # Projects / Que
    """
    TODO - needs external list with projects/que names connect
           with foreign keys.
    """
    project = models.IntegerField(blank=True, null=True)
    
    list = models.ForeignKey(List)
    created_date = models.DateField()    
    due_date = models.DateField(blank=True,null=True,)
    completed = models.BooleanField()
    completed_date = models.DateField(blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='created_by')
    assigned_to = models.ForeignKey(User, related_name='todo_assigned_to')
    note = models.TextField(blank=True,null=True)
    priority = models.PositiveIntegerField(max_length=3)    
    
    # Model method: Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the item's due date has passed or not."
        if datetime.date.today() > self.due_date :
            return 1

    def __unicode__(self):
        return self.title
        
    # Auto-set the item creation / completed date
    def save(self):
        # Set datetime on initial item save 
        if not self.id:
            self.created_date = datetime.datetime.now()
            
        # If Item is being marked complete, set the completed_date
        if self.completed :
            self.completed_date = datetime.datetime.now()
        super(Item, self).save()


    class Meta:
        ordering = ["priority"]        
        

class Comment(models.Model):    
	"""
	Not using Django's built-in comments becase we want to be able to save 
	a comment and change task details at the same time. Rolling our own since it's easy.
	"""
	author = models.ForeignKey(User)
	task = models.ForeignKey(Item)
	date = models.DateTimeField(default=datetime.datetime.now)
	body = models.TextField(blank=True)
	
	def __unicode__(self):        
		return '%s - %s' % (
			self.author, 
			self.date, 
			)        

class Effort(models.Model):
	"""
	Effort tracking for specific item
	TODO
	"""
	author = models.ForeignKey(User)
	task = models.ForeignKey(Item)
	date = models.DateTimeField(default=datetime.datetime.now)
	body = models.TextField(blank=True)
    # Adds effort in time
	duration = models.IntegerField(blank=False, null=False)
    
    
	def __unicode__(self):        
		return '%s - %s' % (
			self.author, 
			self.date,
			self.effort,
			)
