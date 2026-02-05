from django.urls import path
from .views import TopView, QuestionList

urlpatterns = [
    path('', TopView.as_view(), name='top'),
    path('home/', QuestionList.as_view(), name='question'),
]
