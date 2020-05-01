from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Q
from PlannerApp.models import Item, Status, Team

import logging
logger = logging.getLogger(__name__)

register = template.Library()

def build_item_line(nodeItem):
    ss = '<a href="' + reverse('item-details', args=(nodeItem.id,) ) + '">' + str(nodeItem.name) + '</a>'
    ss += ' Status: ' + str(Status(nodeItem.status))
    ss += ' Planned Duration: ' + str(nodeItem.planned_start_date) + ' - ' + str(nodeItem.planned_end_date)
    ss += ' Duration: ' + str(nodeItem.start_date) + ' - ' + str(nodeItem.end_date)
    return ss

@register.simple_tag
def build_tree(nodeItems):
    ss = '<ul class="tree">'
    for nodeItem in nodeItems:
        ss += '<li>'
        ss += build_item_line(nodeItem)
        ss += build_tree(Item.objects.filter(parent=nodeItem))
        ss += '</li>'
    ss += '</ul>'
    return mark_safe(ss)


@register.simple_tag
def project_progress(project):
    return "project_progress"


@register.simple_tag
def build_item_affiliation(nodeItem):
    ss = 'Project Parh:'
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


#[
#         ['2014Spring', 'Spring 2014', 'spring', new Date(2014, 2, 22), new Date(2014, 5, 20), null, 100, null],
#         ['2014Summer', 'Summer 2014', 'summer', new Date(2014, 5, 21), new Date(2014, 8, 20), null, 100, null],
#         ['2014Autumn', 'Autumn 2014', 'autumn', new Date(2014, 8, 21), new Date(2014, 11, 20), null, 100, null]
#]

      # data.addColumn('string', 'Task ID');
      # data.addColumn('string', 'Task Name');
      # data.addColumn('string', 'Resource');
      # data.addColumn('date', 'Start Date');
      # data.addColumn('date', 'End Date');
      # data.addColumn('number', 'Duration');
      # data.addColumn('number', 'Percent Complete');
      # data.addColumn('string', 'Dependencies');

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


