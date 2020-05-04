from django.urls import path

from PlannerApp import views

urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'project-create', views.ProjectAdd.as_view(success_url=""), name="project-create"),
    path(r'project-details/<slug:pk>/', views.ProjectDetails.as_view(), name="project-details"),
    path(r'project-list', views.ProjectList, name="project-list"),
    path(r'item-create', views.ItemAdd.as_view(success_url=""), name="item-create"),
    path(r'item-details/<slug:pk>/', views.ItemDetails.as_view(), name="item-details"),
    path(r'item-start/<slug:pk>/', views.startItem, name="item-start"),
    path(r'item-end/<slug:pk>/', views.endItem, name="item-end"),
    path(r'my_tasks', views.MyTasksList.as_view(), name="my_tasks"),
    path(r'team-create', views.TeamAdd.as_view(success_url=""), name="team-create"),
    path(r'team-details/<slug:pk>/', views.TeamDetails.as_view(), name="team-details"),
    path(r'team-list', views.TeamList.as_view(), name="team-list"),
    path(r'sprint-details/<slug:pk>/', views.SprintDetails.as_view(), name="sprint-details"),
    path(r'ajax-start-item/<slug:pk>/', views.ajax_start_item, name="ajax-start-item"),
]