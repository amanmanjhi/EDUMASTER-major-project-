from django import forms
from . models import * 
# from edumaster.dashboard.models import Notes


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

class DateInput(forms.DateInput):
    input_type = 'date'



class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}

        fields = ['subject','title','description','due','is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter Your Search:")

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','is_finished']
    
