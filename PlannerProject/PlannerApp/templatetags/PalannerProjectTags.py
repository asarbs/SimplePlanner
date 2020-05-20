from PlannerApp.models import Item, Status, Team, Project
from PlannerApp.templatetags.item_tree_table import build_item_line
from django import template
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe

import logging
logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def build_tree(nodeItems, line=0):
    if nodeItems.count() == 0:
        return ""
    ss = """
<table class="content" border="0">
  <tr>
    <th>Item name</th>
    <th>Status</th>
    <th>Planned dates</th>
    <th>Execution dates</th>
    <th>Team</th>
    <th>Action</th>
</tr>
    """
    for nodeItem in nodeItems:
        ss += build_item_line(nodeItem, line)
        for ch in nodeItem.get_descendants():
            line += 1
            ss += build_item_line(ch, line)
        line += 1
    ss += "</table>"
    return mark_safe(ss)

@register.simple_tag
def build_item_table(nodeItems, line=0):
    if nodeItems.count() == 0:
        return ""
    ss = """
<table class="content" border="0">
  <tr>
    <th>Item name</th>
    <th>Status</th>
    <th>Planned dates</th>
    <th>Execution dates</th>
    <th>Team</th>
    <th>Action</th>
</tr>
    """
    for nodeItem in nodeItems:
        ss += build_item_line(nodeItem, line)
        line += 1
    ss += "</table>"
    return mark_safe(ss)

# TODO
@register.simple_tag
def project_progress(project):
    ss = ""
    project_items = []
    for project_item in project.items.all():
        project_items.append(project_item)
        for child in project_item.get_descendants(include_self=False):
            project_items.append(child)
    all_items = len(project_items)
    done_items = 0
    for item in project_items:
        if Status(item.status) == Status.DONE:
            done_items += 1
    ss = '{0}/{1}'.format(done_items, all_items)
    return mark_safe(ss)


@register.simple_tag
def build_item_affiliation(nodeItem):
    ss = ''
    project = Project.objects.get(items=nodeItem.get_root())
    ss += '<a href="' + reverse('project-details', args=(project.id,) ) + '">' + str(project) + '</a>'
    for item in nodeItem.get_ancestors():
        ss += " > "
        ss += '<a href="' + reverse('item-details', args=(item.id,) ) + '">' + str(item.name) + '</a>'


    return mark_safe(ss)


def build_data_chart_one_line(item, ansesstor="null"):
    item_planned_start_date_year = 0
    item_planned_start_date_month = 0
    item_planned_start_date_day = 0
    item_planned_end_date_year = 0
    item_planned_end_date_month = 0
    item_planned_end_date_day = 0
    try:

        item_planned_start_date_year = item.planned_start_date.year
        item_planned_start_date_month = item.planned_start_date.month -1
        item_planned_start_date_day = item.planned_start_date.day
        item_planned_end_date_year = item.planned_end_date.year
        item_planned_end_date_month = item.planned_end_date.month -1 
        item_planned_end_date_day = item.planned_end_date.day
    except AttributeError: 
        pass

    a = "null" if ansesstor == "null"  else "'" + ansesstor + "'"
    s =  "\t['{0}', '{1}', '{2}', new Date({3}, {4}, {5}), new Date({6}, {7}, {8}), null, 100, {9}]".format(
            item.item_id, 
            item, 
            item.team, 
            item_planned_start_date_year, 
            item_planned_start_date_month, 
            item_planned_start_date_day,
            item_planned_end_date_year, 
            item_planned_end_date_month, 
            item_planned_end_date_day,
            str(a)
            )
    return s

def foo(projectItems, ansesstor="null"):
    lines = []
    for item in projectItems:
        s = build_data_chart_one_line(item, ansesstor)
        lines.append(s)
        lines.extend(foo(item.get_children()))
    return lines

@register.simple_tag
def get_gnat_chart_data(projectItems):
    lines = []
    lines.extend(foo(projectItems))
    ss = '[\n' + ',\n'.join(lines) + "\n]"
    return mark_safe(ss)


@register.simple_tag
def status_translate(statusInt):
    return Status(statusInt)


def build_menu(menu_list):
    ss = '<ul class="menu">'
    for item in menu_list:
        ss += '<li><a href="{1}">{0}</a>'.format(item['name'], item['url_reverse'])
        if 'add_new' in item:
            ss += u'<a href="{0}" class="add_new">+</a>'.format(item['add_new']['url_reverse'])
        if 'url_edit' in item:
            ss += u'<a href="{0}" class="add_new">e</a>'.format(item['url_edit'])
        if 'children' in item:
            ss += build_menu(item['children'])
        ss += '</li>'
    ss += "</ul>"
    return ss

@register.simple_tag
def page_menu():

    page_menu = []
    page_menu.append({'name':'List of project', 'url_reverse': reverse('project-list'), 'children':[], 'add_new':{'url_reverse': reverse('project-create')} })
    projects = Project.objects.all()
    for project in projects:
        page_menu[-1]['children'].append({'name':project, 'url_reverse': reverse('project-details',args=(project.id,))})


    page_menu.append({'name':'My Tasks', 'url_reverse': reverse('my_tasks') })

    page_menu.append({'name':'Team List', 'url_reverse': reverse('team-list'), 'children':[], 'add_new':{ 'url_reverse': reverse('team-create')}})
    teams = Team.objects.all()
    for team in teams:
        page_menu[-1]['children'].append({'name':team, 'url_reverse': reverse('team-details',args=(team.id,)), 'url_edit': reverse('team-edit',args=(team.id,))})


    return mark_safe(build_menu(page_menu))