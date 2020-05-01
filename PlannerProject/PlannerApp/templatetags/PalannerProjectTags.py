from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Q
from PlannerApp.models import Item, Status, Team

import logging
logger = logging.getLogger(__name__)

register = template.Library()

@register.simple_tag
def build_tree(nodeItems):
    ss = '<ul class="tree">'
    logger.debug(type(nodeItems))
    for nodeItem in nodeItems:
        ss += '<li>'
        ss += '<a href="' + reverse('item-details', args=(nodeItem.id,) ) + '">' + str(nodeItem.name) + '</a>'
        ss += ' Status: ' + str(Status(nodeItem.status))
        ss += ' Planned Duration: ' + str(nodeItem.planned_start_date) + ' - ' + str(nodeItem.planned_end_date)
        ss += ' Duration: ' + str(nodeItem.start_date) + ' - ' + str(nodeItem.end_date)
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
    pert = (done/total) * 100
    return u'{0}/{1} {2}%'.format(done,total,pert)

@register.simple_tag
def get_sprint_team(sprint):
    team = Team.objects.filter(sprint=sprint)[0]
    return team.name

@register.simple_tag
def get_strint_items(sprint):
    items = Item.objects.filter(sprint=sprint)
    logger.debug(items)
    return items
