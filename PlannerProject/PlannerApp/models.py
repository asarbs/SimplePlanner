from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from enum import Enum
import datetime

from simple_history.models import HistoricalRecords
from simple_history import register

# Create your models here.


class Status(Enum):
    IN_PROGRESS = 1
    IN_TESTING = 2
    NEW = 3
    GROOMED = 4
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
    wbs_id = models.CharField(max_length=50, default="0")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    priority = models.IntegerField(default=1)
    assignment = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    _planned_start_date = models.DateField(default=datetime.date.today,null=True, blank=True)
    _planned_end_date = models.DateField(default=datetime.date.today,null=True, blank=True)
    status = models.IntegerField(choices=[(tag.value, tag.name) for tag in Status], default=Status.NEW ) 
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    _progress = models.IntegerField(default = 0)
    history = HistoricalRecords()

    @property
    def length(self):
        try:
            return (self.end_date - self.start_date).days
        except TypeError:
            return "0"

    @property
    def effort_estimation(self):
        try:
            return (self._planned_end_date - self._planned_start_date).days
        except TypeError:
            return "0"

    @property
    def planned_start_date(self):
        dates = [self._planned_start_date]
        try:
            for sd in self.get_children():
                dates.append(sd._planned_start_date)
        except:
            pass
        return min(dates)

    @property
    def planned_end_date(self):
        dates = [self._planned_end_date]
        try:
            for sd in self.get_children():
                dates.append(sd._planned_end_date)
        except:
            pass
        return max(dates)

    @property
    def generation(self):
        return self.get_ancestors().count()

    @property
    def progress(self):
        if self.is_leaf_node():
            return self._progress

        progress = 0
        children_count = 0
        for ch in Item.objects.filter(parent=self):
            progress += ch.progress
            children_count += 1
        if children_count == 0:
            return 0
        progress = progress / children_count
        return round(progress)
    
    def getStatus(self):
        childrens = Item.objects.filter(parent=self)
        if childrens.count() == 0:
            return self.status
        else:
            child_status = []
            for children in childrens:
                child_status.append(children.getStatus())
            return min(child_status)

    def calc_priority(self):
        prio = []
        for a in self.get_ancestors():
            prio.append('{0:04d}'.format(a.priority))
        prio.append('{0:04d}'.format(self.priority))
        ss = '.'.join(prio)
        return ss



    class MPTTMeta:
        order_insertion_by = ['priority']

    def __str__(self):
        return u'{0} {1}'.format(self.wbs_id, self.name)

    def __unicode__(self):
        return u'{0} {1}'.format(self.wbs_id, self.name, blank=True, )

class Project(models.Model):
    name = models.CharField(max_length=500)
    items = models.ManyToManyField(Item, null=True, blank=True)

    @property
    def planned_start_date(self):
        dates = []

        for item in self.items.all():
            dates.append(item.planned_start_date)
        try:
            return min(dates)
        except:
            return '#'

    @property
    def planned_end_date(self):
        dates = []

        for item in self.items.all():
            dates.append(item.planned_end_date)
        try:
            return max(dates)
        except:
            return '#'

    @property
    def progress(self):
        progress = 0
        children_count = 0
        for ch in self.items.all():
            progress += ch.progress
            children_count += 1
        if children_count == 0:
            return 0
        progress = progress / children_count
        return round(progress)
    

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name)