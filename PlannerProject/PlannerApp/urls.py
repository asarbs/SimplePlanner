from django.urls import path
from dal import autocomplete

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
    path(r'item-history/<slug:pk>/', views.ItemHistory.as_view(), name="item-history"),
    path(r'my_tasks', views.MyTasksList.as_view(), name="my_tasks"),
    path(r'team-create', views.TeamAdd.as_view(success_url=""), name="team-create"),
    path(r'team-details/<slug:pk>/', views.TeamDetails.as_view(), name="team-details"),
    path(r'team-list', views.TeamList.as_view(), name="team-list"),
    path(r'team-edit/<slug:pk>/', views.TeamEdit.as_view(), name="team-edit"),
    path(r'ajax-start-item/<slug:pk>/', views.ajax_start_item, name="ajax-start-item"),
    path(r'ajax-close-item/<slug:pk>/', views.ajax_close_item, name="ajax-close-item"),
    path(r'ajax_set_team/<slug:pk>/<int:team_id>/', views.ajax_set_team, name="ajax_set_team"),
    path(r'user-autocomplete/', views.UserAutocomplete.as_view(), name='user-autocomplete'),
    path(r'reports-team-workload', views.report_team_workload, name="reports-team-workload")
]