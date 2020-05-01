
from django.forms import ModelForm, CharField
from django.forms import DateInput
from django.forms import IntegerField
from django.forms import HiddenInput
from PlannerApp.models import Project, Item


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
        #self.fields['project_id'].widget = HiddenInput()
        self.iid = iid
        self.fields['item_id'].initial = iid
        # self.fields['item_id'].widget = HiddenInput()

    class Meta:
        model = Item
        fields = ['name', 'parent', 'priority', 'sprint', 'assignment', 'start_date', 'end_date', 'status', 'project_id', 'item_id']
        widgets = {
            'start_date': DateInput(format=('%d.$m.%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'end_date': DateInput(format=('%d.$m.%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }
