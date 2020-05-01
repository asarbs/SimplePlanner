from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from PlannerApp.models import Project
from PlannerApp.models import Item

from PlannerApp.forms import NewProjectForm
from PlannerApp.forms import NewItemForm

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
        self.id = item.id
        return super(ItemAdd, self).form_valid(form)

    def get_success_url(self):
        return reverse("item-details", args=(self.id,))


class MyTasksList(ListView):
    model = Item
    template_name = "PlannerApp/MyTasksList.html"
    context_object_name = 'my_task_list'
    
    def get_queryset(self):
        queryset = super(MyTasksList, self).get_queryset()
        queryset = queryset.filter(assignment=self.request.user)
        print(queryset)
        return queryset