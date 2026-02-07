# from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# from .models import Question


#TOP画面の表示
class TopView(TemplateView):
    template_name = 'index.html'
    


#質問一覧の表示
#本当はListView使用
class QuestionList(LoginRequiredMixin,TemplateView):
    template_name = 'home.html'
    # model = Question