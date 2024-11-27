from pyexpat.errors import messages
from django.shortcuts import redirect,render # type: ignore
from django.contrib import messages 
from . forms import *
from django.views import generic
from youtubesearchpython import VideosSearch # type: ignore
import requests  # type: ignore
import wikipedia  # type: ignore
from django.contrib.auth.decorators import login_required
from django.conf import settings
import openai  # type: ignore # Assuming you have `openai` installed for API access
from .forms import LearningObjectiveForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseRedirect

from cohere import Client
import pandas as pd
import os

# openai.api_key = settings.OPENAI_API_KEY

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method=="POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user, title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"notes added from {request.user.username} Successfully!")
    else:
        form = NotesForm()
    notes= Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form':form}
    return render(request,'dashboard/notes.html',context)
    
@login_required        
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")  # type: ignore
    
class NotesDetailView(generic.DetailView):
    model = Notes




@login_required
def homework(request):

    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except: 
                finished = False

            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f'Homework Added from {request.user.username}!!')
    else:
            form = HomeworkForm()

    homework= Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {
        'homeworks':homework,
        'homework_done':homework_done,
        'form':form,
        }
    return render(request,'dashboard/homework.html',context) 
 
@login_required
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True

    homework.save()
    return redirect('homework')



@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete() 
    return redirect("homework")

def youtube(request):
    if request.method=="POST":
        form= DashboardForm(request.POST)
        text= request.POST['text']
        video= VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dictionery={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
                 
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            
            result_dictionery['description'] = desc
            result_list.append(result_dictionery)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context={'form':form}
    return render(request,'dashboard/youtube.html',context )

@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished= request.POST["is_finished"]
                if finished == "on":
                    finished=True
                else:
                    finished= False
            except:
                finished= False
            
            todos=Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f"ToDo Added From {request.user.username}!!")

    form=TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todos_done=True
    else:
        todos_done=False
    context = {'form':form,'todos':todo,'todos_done':todos_done}
    

    return render(request,"dashboard/todo.html",context)
@login_required
def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished==True
    else:
        todo.is_finished==False
    todo.save()
    return redirect('todo')

def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


def books(request):
    if request.method=="POST":
        form= DashboardForm(request.POST)
        text= request.POST['text']
        url= "https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLinks')
            }
            
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)
    else:
        form = DashboardForm()
    context={'form':form}
    return render(request,'dashboard/books.html',context )

def dictionary(request):
    if request.method=="POST":
        form= DashboardForm(request.POST)
        text= request.POST['text']
        url= "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r=requests.get(url)
        answer=r.json()
        try:
            phonetics=answer[0]['phonetics'][0]['text']
            audio=answer[0]['phonetics'][0]['audio']
            definition=answer[0]['meanings'][0]['definitions'][0]['definition']
            example=answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms,
            }
        except:
            context={
                'form':form,
                'input':''
            }
        return render(request,"dashboard/dictionary.html",context)

    else:

        form=DashboardForm()
        context={'form':form}

    return render(request,"dashboard/dictionary.html",context)



def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary


        }
        return render(request,"dashboard/wiki.html",context)
    else:
        form = DashboardForm()
        context={
            'form':form
    
        }
    return render(request,"dashboard/wiki.html",context)

def register(request):
    if request.method == 'POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"Account Created For {username}!!")
            return redirect("login")

    else:
        form=UserRegistrationForm()
    context={
        'form':form
    }
    return render(request,'dashboard/register.html',context)

@login_required
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,user=request.user)
    todos=Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks)==0:
        homework_done = True
    else:
        homework_done = False
    if len(todos)==0:
        todos_done = True
    else:
        todos_done = False
    context={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done,


    }

    return render(request,"dashboard/profile.html",context)

def logout(request):
    if request.method=="post":
        logout(request)
        return HttpResponseRedirect('/login/')
    return render(request, 'dashboard/logout.html')




@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # OpenAI ChatGPT API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or another model like 'gpt-4'
            messages=[{"role": "user", "content": user_message}]
        )
        chatbot_message = response.choices[0].message['content']

        return JsonResponse({"message": chatbot_message})
    return JsonResponse({"error": "Only POST requests are allowed."}, status=405)



# Initialize Cohere client
cohere_api_key = os.getenv("CO_API_KEY")
cohere_client = Client(cohere_api_key)

def generate_study_plan(request):
    if request.method == "POST":
        data = request.POST
        course_load = data.getlist('courses[]')
        deadlines = data.getlist('deadlines[]')
        preferences = data.get('preferences', '')
        print(f'the api key I get is {os.getenv("CO_API_KEY")}')

        # Prepare Cohere prompt
        prompt = f"Generate a detailed study plan for the following courses: {', '.join(course_load)}. " \
                 f"The deadlines are: {', '.join(deadlines)}. The study preferences are: {preferences}."

        try:
            response = cohere_client.generate(
                model='command-r-plus',
                prompt=prompt,
                max_tokens=1000,
                temperature=0.7
            )
            study_plan = response.generations[0].text
            return JsonResponse({"study_plan": study_plan}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    return render(request, 'dashboard/generate_study_plan.html')

        


