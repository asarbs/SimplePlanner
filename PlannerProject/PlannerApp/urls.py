from django.urls import path

from PlannerApp import views

urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'project-create', views.ProjectAdd.as_view(success_url=""), name="project-create"),
    path(r'project-details/<slug:pk>/', views.ProjectDetails.as_view(), name="project-details"),
    path(r'project-list', views.ProjectList, name="project-list"),
    path(r'item-create', views.ItemAdd.as_view(success_url=""), name="item-create"),
    path(r'item-details/<slug:pk>/', views.ItemDetails.as_view(), name="item-details"),
    path(r'my_tasks', views.MyTasksList.as_view(), name="my_tasks"),
]