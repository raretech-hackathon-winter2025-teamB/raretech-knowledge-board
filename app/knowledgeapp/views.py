from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Question


#TOP画面の表示
class TopView(TemplateView):
    template_name = 'index.html'
    


#質問一覧の表示
class QuestionList(ListView):
    template_name = 'home.html'
    model = Question

# def homeview(request):
#     return render(request, 'home.html')