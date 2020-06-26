from datetime import datetime, timedelta
import json
import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User

from dal import autocomplete

from PlannerApp.models import Item
from PlannerApp.models import Project
from PlannerApp.models import Status
from PlannerApp.models import Team

from PlannerApp.forms import NewItemForm
from PlannerApp.forms import NewProjectForm
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


def update_date(item, new_date):
    if item is None:
        return
    duration = item.planned_end_date - item.planned_start_date
    item._planned_start_date = new_date
    item._planned_end_date = new_date + duration
    item.save()
    update_date(item.next_item, item.planned_end_date)

    logger.debug(u'{0} -> {2} - {1} {3}'.format(item, new_date, item.next_item, duration))


def project_recalculate(request, pk):
    project = Project.objects.get(id=pk)
    for item in project.items.all():
        update_date(item.next_item, item.planned_end_date)

    return HttpResponseRedirect(reverse("project-details", args=(pk,)))

class ItemDetails(DetailView):
    model = Item

    def get_object(self, queryset=None):
        item = super(ItemDetails, self).get_object(queryset)
        return item

class ItemHistory(DetailView):
    model = Item
    template_name = "PlannerApp/ItemHistory.html"
    
    def get_object(self, queryset=None):
        item = super(ItemHistory, self).get_object(queryset)
        return item

    def get_context_data(self, **kwargs):
        context = super(ItemHistory, self).get_context_data(**kwargs)
        item = self.get_object()
        context['history'] = item.history.all()
        return context

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

        if item.planned_end_date < item.planned_start_date:
            form.add_error('planned_end_date', 'End date must be later than start date.')
            return self.form_invalid(form)

        if form.cleaned_data['project_id'] is not -1:
            item.save()
            project = Project.objects.get(id=form.cleaned_data['project_id'])
            project.items.add(item)
            children_num = project.items.count()
            item.wbs_id = '{0}'.format(children_num)
            project.save()
        elif form.cleaned_data['item_id'] is not -1:
            parent = Item.objects.get(id=form.cleaned_data['item_id'])
            item.insert_at(target=parent, position='last-child', save=True)
            children_num = parent.get_children().count()
            item.wbs_id = '{0}.{1}'.format(parent.wbs_id, children_num)
            item.save()
        if item._planned_start_date == item._planned_end_date:
            item._planned_end_date += timedelta(days=1)
            item.save()
        self.id = item.id
        return super(ItemAdd, self).form_valid(form)

    def get_success_url(self):
        return reverse("item-details", args=(self.id,))

class ItemEdit(UpdateView):
    model = Item
    form_class = NewItemForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        item = form.save(commit=False)
        logger.debug('{0} {1} {2}'.format(item, item.planned_start_date, item.planned_end_date))
        if item.planned_end_date < item.planned_start_date:
            form.add_error('planned_end_date', 'End date must be later than start date.')
            return self.form_invalid(form)

        if item.planned_start_date is not None or item.planned_end_date is not None:
            if (item.planned_start_date == item.planned_end_date):
                item.planned_end_date += timedelta(days=1)

        if item.next_item is not None:
            item.next_item.predecessor_item = item
            item.next_item.save()

        item.save()
        return super(ItemEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse("item-details", args=(self.object.id,))


def setItemStatus(request, pk, status):
    item = Item.objects.get(id=pk)
    item.status = status.value
    if status == Status.IN_PROGRESS:
        item.start_date = datetime.now()
    elif status == Status.DONE:
        item.end_date = datetime.now()
    item.assignment = request.user
    item.save()
    out = [item]
    for ancestor in item.get_ancestors():
        out.extend( setItemStatus(request, ancestor.pk, status) )
    return out

def startItem(request, pk=None): 
    setItemStatus(request, pk, Status.IN_PROGRESS)
    return HttpResponseRedirect(reverse("item-details", args=(pk,)))
def endItem(request, pk=None): 
    setItemStatus(request, pk, Status.DONE)
    return HttpResponseRedirect(reverse("item-details", args=(pk,)))


class MyTasksList(ListView):
    model = Item
    template_name = "PlannerApp/MyTasksList.html"
    context_object_name = 'my_task_list'
    
    def get_queryset(self):
        queryset = super(MyTasksList, self).get_queryset()
        queryset = queryset.filter(assignment=self.request.user)
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

    def get_context_data(self, **kwargs):
        context = super(TeamDetails, self).get_context_data(**kwargs)
        context['team_tasks'] = Item.objects.filter(team=self.object)
        return context

class TeamList(ListView):
    model = Team
    template_name = "PlannerApp/team_list.html"
    context_object_name = 'teams'

    def get_queryset(self):
        queryset = super(TeamList, self).get_queryset()
        return queryset

class TeamEdit(UpdateView):
    model = Team
    form_class = NewTeamForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        return super(TeamEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse("team-details", args=(self.object.id,))


def ajax_start_item(request, pk):
    if request.method == "GET" and request.is_ajax():
        changed_items = setItemStatus(request, pk, Status.IN_PROGRESS)
        d = {'status': "OK", 'items': [] }
        for item in changed_items:
            d['items'].append(
                {'item_id': item.id,
                'newState': str(Status(item.getStatus())),
                'start_date': item.start_date.strftime("%m/%d/%Y") if item.start_date is not None else '-#-',
                'end_date': item.end_date.strftime("%m/%d/%Y") if item.end_date is not None else '-#-',
                }
            )
        return HttpResponse(json.dumps(d), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': "NOK"}), content_type="application/json")

def ajax_close_item(request, pk):
    if request.method == "GET" and request.is_ajax():
        changed_items = setItemStatus(request, pk, Status.DONE)
        d = {'status': "OK", 'items': [] }
        for item in changed_items:
            d['items'].append(
                {'item_id': item.id,
                'newState': str(Status(item.getStatus())),
                'start_date': item.start_date.strftime("%m/%d/%Y") if item.start_date is not None else '-#-',
                'end_date': item.end_date.strftime("%m/%d/%Y") if item.end_date is not None else '-#-',
                }
            )

        return HttpResponse(json.dumps(d), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': "NOK"}), content_type="application/json")

def ajax_set_team(request, pk, team_id):
    if request.method == "GET" and request.is_ajax():
        item = Item.objects.get(id=pk)
        try:
            item.team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            item.team = None
        item.save()
        return HttpResponse(json.dumps({'status': "OK"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': "NOK"}), content_type="application/json")

def ajax_item_change_progress(request, pk, progress):
    if request.method == "GET" and request.is_ajax():
        item = Item.objects.get(id=pk)
        item._progress = progress 
        item.save()
        return HttpResponse(json.dumps({'status': "OK"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': "NOK"}), content_type="application/json")

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.mone()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        return qs

def report_team_workload(request):
    teams = Team.objects.all()
    for team in teams:
        team.work_planned = 0
        items = Item.objects.filter(team=team, status__in=[Status.NEW.value, Status.GROOMED.value, Status.IN_PROGRESS.value, Status.IN_TESTING.value]).order_by('_planned_end_date')
        for item in items:
            team.work_planned += item.effort_estimation
            team.last_planned_item = item
        work_weeks = team.work_planned / 5
        team.landing_date = datetime.now() + timedelta(weeks=work_weeks)


    return render(request, 'PlannerApp/report_team_workload.html', {'teams': teams})
