from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Q
from PlannerApp.models import Item, Status, Team, Project

import logging
logger = logging.getLogger(__name__)

register = template.Library()

def start_button(nodeItem):
    ss = '<td>{0} <button type="button" onclick="startItem({1})">Start</button></td>\n'.format(Status(nodeItem.status), nodeItem.id)

    return ss

def build_item_line(nodeItem, line):
    line_class = "even" if line % 2 == 0 else "odd"
    ss = '<tr class="'+ line_class +'">\n'
    ss += '<td style="padding-left: '+ (str(nodeItem.generation * 10) ) +'px;"><a href="' + reverse('item-details', args=(nodeItem.id,) ) + '">' + str(nodeItem.name) + '</a></td>\n'
    ss += start_button(nodeItem)
    ss += '<td>' + str(nodeItem.planned_start_date) + ' - ' + str(nodeItem.planned_end_date)  + '</td>\n'
    ss += '<td>' + str(nodeItem.start_date) + ' - ' + str(nodeItem.end_date) + '</td>\n'
    ss += '<td>' + str(nodeItem.team) + '</td>\n'
    ss += '<td>' + str(nodeItem.sprint) + '</td>\n'
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
    <th>Sprints</th>
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
    <th>Sprints</th>
</tr>
    """
    for nodeItem in nodeItems:
        ss += build_item_line(nodeItem, line)
        line += 1
    ss += "</table>"
    return mark_safe(ss)

@register.simple_tag
def project_progress(project):
    return "project_progress"


@register.simple_tag
def build_item_affiliation(nodeItem):
    ss = ''
    project = Project.objects.get(items=nodeItem.get_root())
    ss += '<a href="' + reverse('project-details', args=(project.id,) ) + '">' + str(project) + '</a>'
    for item in nodeItem.get_ancestors():
        ss += " > "
        ss += '<a href="' + reverse('item-details', args=(item.id,) ) + '">' + str(item.name) + '</a>'


    return mark_safe(ss)


@register.simple_tag
def sprint_details(t_sprint):
    total = Item.objects.filter(sprint = t_sprint).filter(~Q(status = Status.REJECTED.value)).count()
    done = Item.objects.filter(sprint = t_sprint).filter(status = Status.DONE.value).count()
    if total == 0:
        return None
    pert = (done/total) * 100
    return u'{0}/{1} {2}%'.format(done,total,pert)

@register.simple_tag
def get_sprint_team(sprint):
    team = Team.objects.filter(sprint=sprint)[0]
    return team.name

@register.simple_tag
def get_strint_items(sprint):
    items = Item.objects.filter(sprint=sprint)
    ss = "<ul>"
    for item in items:
        ss += "<li>"
        ss += build_item_line(item)
        ss += "</li>"
    ss += "</ul>"
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