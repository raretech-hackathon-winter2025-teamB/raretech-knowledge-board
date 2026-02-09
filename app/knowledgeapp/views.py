# from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question
from django.urls import reverse_lazy


#TOP画面の表示
class TopView(TemplateView):
    template_name = 'index.html'
    

#質問一覧の表示
class QuestionList(LoginRequiredMixin,ListView):
    template_name = 'home.html'
    model = Question

# def homeview(request):
#     return render(request, 'home.html')

#質問投稿画面の表示
class QuestionCreate(LoginRequiredMixin,CreateView):
    template_name = 'new_question.html'
    model = Question
    fields = ('title', 'category', 'detail', 'image_url')  #create時に必要な項目をmodelから選んでおく。
    success_url = reverse_lazy('knowledgeapp:question') #データを登録後、urls.pyのなかのname=○○の箇所に遷移させる。

    def form_valid(self, form):
        # 保存する前に、現在ログインしているユーザーをセットし、登録する        
        form.instance.user = self.request.user
        form.instance.status = '2'
        return super().form_valid(form)

#質問投稿の削除
class QuestionDelete(LoginRequiredMixin,DeleteView):
    template_name = 'delete_question.html'
    model = Question
    success_url = reverse_lazy('knowledgeapp:question')
