from django import forms
from . models import * 
from django.contrib.auth.forms import UserCreationForm
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

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['username', 'password1', 'password2']
        
class LearningObjectiveForm(forms.Form):
    course_name = forms.CharField(label='Course Name', max_length=100)
    objectives = forms.CharField(widget=forms.Textarea, label='What do you want to learn?')
    available_time = forms.IntegerField(label='Available hours per day')
    learning_days = forms.IntegerField(label='In how many days do you want to complete the course?')
    
