from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Q
from PlannerApp.models import Item, Status, Team, Project

import logging
logger = logging.getLogger(__name__)

register = template.Library()

def start_button(nodeItem):
    button = ""
    if Status(nodeItem.status) == Status.NEW:
        button = '<button type="button" onclick="startItem({0})">Start</button>'.format(nodeItem.id)
    elif Status(nodeItem.status) == Status.IN_PROGRESS:
        button = '<button type="button" onclick="closeItem({0})">Close</button>'.format(nodeItem.id)
    ss = '<td>{0}</td>\n'.format( button)

    return ss


def build_team_select(selectedTeam, nodeItem):
    teams = Team.objects.all()
    ss = '<select id="select_team_{0}" onchange="updateTeam({0})">\n'.format(nodeItem.id)
    ss += '<option value="0">--</option>\n'
    for team in teams:
        selected = ''
        if team == selectedTeam:
            selected = 'selected'
        ss += '<option value="{0}" {2}>{1}</option>\n'.format(team.id, team, selected)

    ss += '</select>\n'
    return ss


def build_item_line(nodeItem, line):
    line_class = "even" if line % 2 == 0 else "odd"
    ss = '<tr class="'+ line_class +'">\n'
    ss += '<td style="padding-left: {0}px;"><a href="{1}">{2}</a></td>\n'.format((nodeItem.generation * 10), reverse('item-details', args=(nodeItem.id,) ), nodeItem.name)
    ss += '<td id="statusItem_'+ str(nodeItem.id) +'">{0}</td>'.format(Status(nodeItem.status))
    ss += '<td>{0} - {1}</td>\n'.format(nodeItem.planned_start_date, nodeItem.planned_end_date)
    ss += '<td id="dates_{0}">{1} - {2}</td>\n'.format(nodeItem.id, nodeItem.start_date, nodeItem.end_date)
    ss += '<td>{0}</td>\n'.format(build_team_select(nodeItem.team, nodeItem))
    ss += start_button(nodeItem)
    ss += '</tr>\n'
    return ss

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
    <th colspan="2">Status</th>
    <th>Planned dates</th>
    <th>Execution dates</th>
    <th>Team</th>
    <th>Sprints</th>
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
    logger.debug(project_items)
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
        lines.extend(foo(item.get_children(), item.item_id))
    return lines

@register.simple_tag
def get_gnat_chart_data(projectItems):
    lines = []
    lines.extend(foo(projectItems))
    ss = '[\n' + ',\n'.join(lines) + "\n]"
    logger.debug(ss)
    return mark_safe(ss)


@register.simple_tag
def status_translate(statusInt):
    return Status(statusInt)