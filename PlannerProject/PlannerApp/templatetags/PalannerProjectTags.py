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
    <th>Progress</th>
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
    <th>Progress</th>
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

def build_org_chart_line(projectItem, parent=''):
    lines = ["['{0}','{1}']".format(projectItem, parent)]
    for pitem in projectItem.get_children():
         lines.extend(build_org_chart_line(pitem, projectItem))
    return lines

@register.simple_tag
def get_org_chart(projectItems, project):
    lines = []
    for pitem in projectItems:
        lines.extend(build_org_chart_line(pitem, project))

    ss = '[\n' + ',\n'.join(lines) + "\n]"
    return mark_safe(ss)


def build_gantt_chart_line(item):
    item_planned_start_date_year = 0
    item_planned_start_date_month = 0
    item_planned_start_date_day = 0
    item_planned_end_date_year = 0
    item_planned_end_date_month = 0
    item_planned_end_date_day = 0
    try:
        item_planned_start_date_year = item._planned_start_date.year
        item_planned_start_date_month = item._planned_start_date.month -1
        item_planned_start_date_day = item._planned_start_date.day
        item_planned_end_date_year = item._planned_end_date.year
        item_planned_end_date_month = item._planned_end_date.month -1 
        item_planned_end_date_day = item._planned_end_date.day
    except AttributeError: 
        pass

    #a = "null" if ansesstor == "null"  else "'" + ansesstor + "'"
    a = ""
    s =  "\t['{0}', '{1}', new Date({2}, {3}, {4}), new Date({5}, {6}, {7}), null,  {8},  {9}]".format(
            item.wbs_id, 
            item, 
            item_planned_start_date_year, 
            item_planned_start_date_month, 
            item_planned_start_date_day,
            item_planned_end_date_year, 
            item_planned_end_date_month, 
            item_planned_end_date_day,
            item.progress,
            "null" if item.predecessor_item == None else "'{0}'".format(item.predecessor_item.wbs_id)
            )
    return s


def build_gantt_chart_lines(item):
    lines = []
    lines.append(build_gantt_chart_line(item))
    for children in item.get_descendants():
        lines.append(build_gantt_chart_line(children))

    return lines



@register.simple_tag
def get_gantt_chart_data(projectItems):
    lines = []
    for item in projectItems:
        lines.extend(build_gantt_chart_lines(item))
    ss = '[\n' + ',\n'.join(lines) + "\n]"
    return "" # mark_safe(ss)


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

    page_menu.append({'name': "Team workload report", 'url_reverse': reverse('reports-team-workload') })


    return mark_safe(build_menu(page_menu))