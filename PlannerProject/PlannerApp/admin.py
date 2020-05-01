from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from PlannerApp.models import Sprint
from PlannerApp.models import Item
from PlannerApp.models import Team
from PlannerApp.models import Board
from PlannerApp.models import Project


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    pass


class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    model = Item
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'priority', 'assignment', 'status', 'start_date', 'end_date', 'length', 'item_id')
    list_display_links = ('indented_title', )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, CustomMPTTModelAdmin)

# Register your models here.