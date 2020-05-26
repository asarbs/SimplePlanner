from django.urls import reverse

from PlannerApp.models import Item, Status, Team, Project

def split_button(nodeItem):
    return '<a href="' + reverse('item-create') + '?iid={0}" class="button">Add child</a>'.format(nodeItem.id)

def start_button(nodeItem):
    button = ""
    if Status(nodeItem.status) == Status.NEW:
        button = '<button type="button" onclick="startItem({0})">Start</button>'.format(nodeItem.id)
    elif Status(nodeItem.status) == Status.IN_PROGRESS:
        button = '<button type="button" onclick="closeItem({0})">Close</button>'.format(nodeItem.id)
    ss = '{0}\n'.format( button)

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

def progress_select(nodeItem):
    if not nodeItem.is_leaf_node():
        return ""
    ss = '<select id="item_progress_{0}" onchange="updateProgress({0})" class="select_progress">\n'.format(nodeItem.id)
    ss += '<option value="0">--</option>\n'
    for p in range(0,110,10):
        selected = ''
        if p == nodeItem._progress:
            selected = 'selected'
        ss += '<option value="{0}" {2}>{1}</option>\n'.format(p, p, selected)

    ss += '</select>\n'
    return ss

def build_item_line(nodeItem, line):
    line_class = "even" if line % 2 == 0 else "odd"
    ss = '<tr class="'+ line_class +'">\n'
    ss += '<td style="padding-left: {0}px;"><a href="{1}">{2}</a></td>\n'.format((nodeItem.generation * 10), reverse('item-details', args=(nodeItem.id,) ), nodeItem)
    ss += '<td id="statusItem_'+ str(nodeItem.id) +'">{0}</td>'.format(Status(nodeItem.getStatus()))
    ss += '<td>{0}%</td>'.format(nodeItem.progress)
    ss += '<td>{0} - {1}</td>\n'.format(nodeItem.planned_start_date, nodeItem.planned_end_date)
    ss += '<td id="dates_{0}">{1} - {2}</td>\n'.format(nodeItem.id, nodeItem.start_date, nodeItem.end_date)
    ss += '<td>{0}</td>\n'.format(build_team_select(nodeItem.team, nodeItem))
    ss += '<td>'
    ss += start_button(nodeItem)
    ss += split_button(nodeItem)
    ss += progress_select(nodeItem)
    ss += '</td>'
    ss += '</tr>\n'
    return ss