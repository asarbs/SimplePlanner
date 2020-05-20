from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from simple_history.admin import SimpleHistoryAdmin
from PlannerApp.models import Item
from PlannerApp.models import Team
from PlannerApp.models import Board
from PlannerApp.models import Project




class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    model = Item
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'priority', 'assignment', 'status', 'start_date', 'end_date', 'planned_start_date', 'planned_end_date', 'length', 'item_id', 'team')
    list_display_links = ('indented_title', )
    list_editable = ( 'status', 'planned_start_date', 'planned_end_date', 'team', 'start_date', 'end_date')


@admin.register(Team)
class TeamAdmin(SimpleHistoryAdmin):
    pass


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, CustomMPTTModelAdmin)

# Register your models here.
