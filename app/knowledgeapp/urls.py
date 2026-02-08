from django.urls import path
from . import views

app_name = "knowledgeapp"
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('home/', views.QuestionList.as_view(), name='question'),
    path('question/new/', views.QuestionCreate.as_view(), name='new_question'),
]
