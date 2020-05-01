from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse


register = template.Library()


def build_line(nodeItem):
    ss = '<tr>'
    ss += '<td><a href="' + reverse('item-details', args=(nodeItem.id,) ) + '">' + str(nodeItem.item_id) + '</a><td>'
    ss += '<td>' + str(nodeItem.name) + '<td>'
    ss += '<td>' + str(nodeItem.start_date) + '<td>'
    ss += '<td>' + str(nodeItem.end_date) + '<td>'
    ss += '<td>' + str(nodeItem.assignment) + '<td>'
    ss += "</tr>"
    return ss


@register.simple_tag
def build_tree(nodeItems):
    ss = ""
    for i in nodeItems:
        ss += '<table border="1">'
        ss += build_line(i)
        for item in i.get_descendants().all():
            ss += build_line(item)
        ss += "</table>"
    return mark_safe(ss)


@register.simple_tag
def build_item_affiliation(nodeItem):
    ss = 'Project Parh'
    for item in nodeItem.get_ancestors():
        ss += " > "
        ss += str(item)
    return mark_safe(ss)
