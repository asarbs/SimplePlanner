from django.urls import path
from dal import autocomplete
from django.contrib.auth.models import User

from PlannerApp import views
from PlannerApp.models import Item

urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'project-create', views.ProjectAdd.as_view(success_url=""), name="project-create"),
    path(r'project-details/<slug:pk>/', views.ProjectDetails.as_view(), name="project-details"),
    path(r'project-list', views.ProjectList, name="project-list"),
    path(r'item-create', views.ItemAdd.as_view(success_url=""), name="item-create"),
    path(r'item-details/<slug:pk>/', views.ItemDetails.as_view(), name="item-details"),
    path(r'item-start/<slug:pk>/', views.startItem, name="item-start"),
    path(r'item-end/<slug:pk>/', views.endItem, name="item-end"),
    path(r'item-edit/<slug:pk>/', views.ItemEdit.as_view(), name="item-edit"),
    path(r'my_tasks', views.MyTasksList.as_view(), name="my_tasks"),
    path(r'team-create', views.TeamAdd.as_view(success_url=""), name="team-create"),
    path(r'team-details/<slug:pk>/', views.TeamDetails.as_view(), name="team-details"),
    path(r'team-list', views.TeamList.as_view(), name="team-list"),
    path(r'ajax-start-item/<slug:pk>/', views.ajax_start_item, name="ajax-start-item"),
    path(r'ajax-close-item/<slug:pk>/', views.ajax_close_item, name="ajax-close-item"),
    path(r'ajax_set_team/<slug:pk>/<int:team_id>/', views.ajax_set_team, name="ajax_set_team"),
    path(r'test-autocomplete/', autocomplete.Select2QuerySetView.as_view(model=User, model_field_name='username'), name='select2_fk'),
]