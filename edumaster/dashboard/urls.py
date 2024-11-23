from django.urls import path # type: ignore
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('notes',views.notes,name="notes"),
    path('delete_note/<int:pk>',views.delete_note,name="delete_note"),
    path('notes_detail/<int:pk>',views.NotesDetailView.as_view(), name="notes-detail"),
    path('homework',views.homework,name="homework"),
    path('update_homework/<int:pk>',views.update_homework,name="update-homework"),
    path('delete_homework/<int:pk>',views.delete_homework,name="delete-homework"),
    path('youtube',views.youtube,name="youtube"),
    path('todo',views.todo,name="todo"),
    path('update_todo/ <int:pk>',views.update_todo,name="update_todo"),
    path('delete_todo/ <int:pk>',views.delete_todo,name="delete_todo"),
    path('books',views.books,name="books"),
    path('dictionary',views.dictionary,name="dictionary"),
    path('books',views.books,name="books"),
    path('wiki',views.wiki,name="wiki"),
    # path('learning_plan/', views.learning_plan, name='learning_plan'),
    # path('quiz_view/', views.quiz_view, name='quiz_view'),
    # path('feedback_view/', views.feedback_view, name='feedback_view'),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    path('generate_study_plan/', views.generate_study_plan, name='generate_study_plan'),
]  