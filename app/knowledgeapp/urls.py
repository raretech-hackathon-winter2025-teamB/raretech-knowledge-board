from django.urls import path
from . import views

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('home/', views.QuestionList.as_view(), name='question'),
]