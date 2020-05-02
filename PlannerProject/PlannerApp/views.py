from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

from PlannerApp.models import Project
from PlannerApp.models import Item
from PlannerApp.models import Team
from PlannerApp.models import Sprint
from PlannerApp.models import Status

from PlannerApp.forms import NewProjectForm
from PlannerApp.forms import NewItemForm
from PlannerApp.forms import NewTeamForm

# Create your views here.

def index(request):
    data = {}
    return render(request, 'main.html', data)


class ProjectAdd(CreateView):
    model = Project

    form_class = NewProjectForm

    def form_valid(self, form):
        project = form.save()
        project.save()
        self.id = project.id
        project.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("project-details", args=(self.id,))


class ProjectDetails(DetailView):
    model = Project

    def get_object(self, queryset=None):
        # Call the superclass
        project = super(ProjectDetails, self).get_object(queryset)
        return project


def ProjectList(request):
    projects = Project.objects.all()
    return render(request,"PlannerApp/project_list.html", context={'projects':projects})


class ItemDetails(DetailView):
    model = Item

    def get_object(self, queryset=None):
        item = super(ItemDetails, self).get_object(queryset)
        return item


class ItemAdd(CreateView):
    model = Item
    form_class = NewItemForm

    def get_form_kwargs(self):
        kwargs = super(ItemAdd, self).get_form_kwargs()
        if self.request.GET:
            kwargs['pid'] = self.request.GET.get('pid', "-1")
            kwargs['iid'] = self.request.GET.get('iid', "-1")
        return kwargs

    def form_valid(self, form):
        item = form.save(commit=False)
        if form.cleaned_data['project_id'] is not -1:
            item.save()
            project = Project.objects.get(id=form.cleaned_data['project_id'])
            project.items.add(item)
            project.save()
        elif form.cleaned_data['item_id'] is not -1:
            parent = Item.objects.get(id=form.cleaned_data['item_id'])
            item.insert_at(target=parent, position='last-child', save=True)
            item.save()
        print(item.planned_start_date == item.planned_end_date)
        if item.planned_start_date == item.planned_end_date:
            item.planned_end_date += timedelta(days=1)
            item.save()
        self.id = item.id
        return super(ItemAdd, self).form_valid(form)

    def get_success_url(self):
        return reverse("item-details", args=(self.id,))

def startItem(request, pk=None): 
    item = Item.objects.get(id=pk)
    item.status = Status.IN_PROGRESS.value
    item.start_date = datetime.now()
    item.assignment = request.user
    item.save()
    return HttpResponseRedirect(reverse("item-details", args=(pk,)))

def endItem(request, pk=None): 
    item = Item.objects.get(id=pk)
    item.status = Status.DONE.value
    item.end_date = datetime.now()
    item.save()
    return HttpResponseRedirect(reverse("item-details", args=(pk,)))


class MyTasksList(ListView):
    model = Item
    template_name = "PlannerApp/MyTasksList.html"
    context_object_name = 'my_task_list'
    
    def get_queryset(self):
        queryset = super(MyTasksList, self).get_queryset()
        queryset = queryset.filter(assignment=self.request.user)
        logger.debug(queryset)
        return queryset

class TeamAdd(CreateView):
    model = Team
    form_class = NewTeamForm

    def form_valid(self, form):
        team = form.save()
        team.save()
        self.id = team.id
        team.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("team-details", args=(self.id,))

class TeamDetails(DetailView):
    model = Team

    def get_object(self, queryset=None):
        team = super(TeamDetails, self).get_object(queryset)
        return team

class TeamList(ListView):
    model = Team
    template_name = "PlannerApp/team_list.html"
    context_object_name = 'teams'

    def get_queryset(self):
        queryset = super(TeamList, self).get_queryset()
        return queryset


class SprintDetails(DetailView):
    model = Sprint
    template_name = "PlannerApp/sprint_details.html"
    context_object_name = 'sprint'

    def get_queryset(self):
        queryset = super(DetailView, self).get_queryset()
        return queryset
