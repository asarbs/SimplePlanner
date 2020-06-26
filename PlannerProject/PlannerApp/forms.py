
from dal import autocomplete

from django.forms import ModelForm, CharField
from django.forms import DateInput
from django.forms import IntegerField
from django.forms import HiddenInput
from django.forms import Select
from django.forms import TextInput
from PlannerApp.models import Project, Item, Team


class NewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']


class NewItemForm(ModelForm):

    project_id = IntegerField()
    item_id = IntegerField()

    def __init__(self, pid = -1, iid = -1 , *args, **kwargs):
        super(NewItemForm, self).__init__(*args, **kwargs)
        self.pid = pid
        self.fields['project_id'].initial = pid
        self.fields['project_id'].widget = HiddenInput()
        self.iid = iid
        self.fields['item_id'].initial = iid
        self.fields['item_id'].widget = HiddenInput()
        self.fields['name'].initial = "item"

    class Meta:
        model = Item
        fields = ['name', 'wbs_id', 'parent', 'priority', 'assignment', 'start_date', 'end_date', 'status', '_planned_start_date', '_planned_end_date', 'team', 'next_item', 'description']
        widgets = {
            'wbs_id': TextInput(attrs={'readonly':'readonly'}),
            'start_date': DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'end_date': DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            '_planned_start_date': DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            '_planned_end_date': DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

class NewTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'teamMembers']

        widgets = {
            'teamMembers': autocomplete.ModelSelect2Multiple(url='user-autocomplete', attrs={'data-placeholder': 'Autocomplete ...','data-html': True})
        }