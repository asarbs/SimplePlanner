from django.urls import reverse

def show_page_menu(context):
    page_menu = {
        'List of project': reverse('project-list'),
        'Create new project': reverse('project-create'),
        "My Tasks": reverse('my_tasks'),
        "Team List": reverse('team-list'),
        "Creat new team": reverse('team-create'),
    }

    return {'page_menu': page_menu}