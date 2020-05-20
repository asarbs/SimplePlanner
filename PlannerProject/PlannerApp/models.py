from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from enum import Enum
import datetime

from simple_history.models import HistoricalRecords

# Create your models here.


class Status(Enum):
    NEW = 1
    GROOMED = 2
    IN_PROGRESS = 3
    IN_TESTING = 4
    DONE = 5
    REJECTED = 6
    DEPLOYED = 7

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Team(models.Model):
    name = models.CharField(max_length=120)
    teamMembers = models.ManyToManyField(User, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Item(MPTTModel):
    name = models.CharField(max_length=500)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    priority = models.FloatField(max_length=25)
    assignment = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    planned_start_date = models.DateField(default=datetime.date.today,null=True, blank=True)
    planned_end_date = models.DateField(default=datetime.date.today,null=True, blank=True)
    status = models.IntegerField(choices=[(tag.value, tag.name) for tag in Status], default=Status.NEW ) 
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    @property
    def length(self):
        try:
            return (self.end_date - self.start_date).days
        except TypeError:
            return "0"


    @property
    def item_id(self):
        out = ""
        for parent in self.get_ancestors(include_self=True).all():
            out += str(parent.id) + "."
        return out[0:-1]

    @property
    def generation(self):
        return self.get_ancestors().count()
    

    class MPTTMeta:
        order_insertion_by = ['priority']

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name, blank=True, )

class Board(models.Model):
    name = models.CharField(max_length=120)
    Team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Project(models.Model):
    name = models.CharField(max_length=500)
    items = models.ManyToManyField(Item, null=True, blank=True)

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name)