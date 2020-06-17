from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from simple_history.admin import SimpleHistoryAdmin
from PlannerApp.models import Item
from PlannerApp.models import Team
from PlannerApp.models import Project


class CustomMPTTModelAdmin(DraggableMPTTAdmin, SimpleHistoryAdmin):
    model = Item
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'priority', 'assignment', 'status', 'start_date', 'end_date', '_planned_start_date', '_planned_end_date', 'length', 'team', '_progress', 'next_item', 'predecessor_item')
    list_display_links = ('indented_title', )
    list_editable = ( 'status', '_planned_start_date', '_planned_end_date', 'team', 'start_date', 'end_date', '_progress', 'next_item', 'predecessor_item')


@admin.register(Team)
class TeamAdmin(SimpleHistoryAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, CustomMPTTModelAdmin)

# Register your models here.
