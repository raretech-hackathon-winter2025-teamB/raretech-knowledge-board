# from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question
from django.urls import reverse_lazy
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt  # curl確認用
from django.shortcuts import get_object_or_404
from .forms import QuestionForm


#TOP画面の表示
class TopView(TemplateView):
    template_name = 'index.html'
    

#質問一覧の表示
class QuestionList(LoginRequiredMixin,ListView):
    template_name = 'home.html'
    model = Question


#質問投稿画面の表示
class QuestionCreate(LoginRequiredMixin,CreateView):
    template_name = 'new_question.html'
    model = Question
    form_class = QuestionForm
    # fields = ('title', 'category', 'detail', 'image_url')  #create時に必要な項目をmodelから選んでおく。
    success_url = reverse_lazy('knowledgeapp:question') #データを登録後、urls.pyのなかのname=○○の箇所に遷移させる。

    def form_valid(self, form):
        # 保存する前に、現在ログインしているユーザーをセットし、登録する        
        form.instance.user = self.request.user
        form.instance.status = '2'
        return super().form_valid(form)  #QuestionCreateとform_validをセットにして返す。
    

#質問の削除 　フロント→バック受け渡し　href="{% url 'knowledgeapp:delete_question' pk=question.pk %}"
# @csrf_exempt # ←curl確認事項用
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk) #指定されたQuestionIDの質問があるか確認し、なければエラーを出す。
    # if request.method == 'DELETE':
    question.delete() #データベースから削除する。
    return HttpResponse(f"ID {pk} を削除しました！", status=200) #削除した際にブラウザに値を返す。


#質問編集機能  フロント→バック受け渡し　href="{% url 'knowledgeapp:update_question' pk=question.pk %}"
class QuestionUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'new_question.html' # または編集用テンプレート
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('knowledgeapp:question')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = '2'
        return super().form_valid(form)

