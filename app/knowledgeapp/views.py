from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView, UpdateView
# LoginRequiredMixin：ログイン必須
# UserPassesTestMixin：回答の投稿者のみ編集可能
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Question, Answer, Category
from django.urls import reverse_lazy, reverse
from .forms import QuestionForm, AnswerForm


#TOP画面の表示
class TopView(TemplateView):
    template_name = 'index.html'
    

#質問一覧の表示
class QuestionList(LoginRequiredMixin,ListView):
    template_name = 'home.html'
    model = Question

# def homeview(request):
#     return render(request, 'home.html')

#質問投稿
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
        return super().form_valid(form)

# 質問詳細
class DeteilQuestion(LoginRequiredMixin,DetailView):
    template_name = 'detail_question.html'
    model = Question
    # テンプレートでQustionオブジェクトを参照する際の変数名
    context_object_name = 'question'
    # URLからプライマリキーを取得する際のキーワード引数名
    pk_url_kwarg = 'question_id' 

    # このメソッドは、HTMLテンプレートに渡す追加のデータを準備するために使われる
    def get_context_data(self, **kwargs):
        # 親クラスがデフォでテンプレに渡してくれる便利なデータを全部取得して、contextに代入
        # super()を使って、親クラス（DetailViewなど）が持っているget_context_dataメソッドを呼び出している
        # **kwargsはこのメソッドに渡された全てのキーワード引数を、そのまま親クラスのメソッドにも渡す意味
        context = super().get_context_data(**kwargs)
        # self.objectは現在のQuestionインスタンス
        # DetailViewはURLの<int:question_id>から数値のIDを受け取り。Question.objects.getを内部的に実行し、取得したQuestionオブジェクトをself.objectに自動的にセットしてくれる
        context['question'] = self.object
        # Answerテーブルの related_name='answers'をみてる
        context['answers'] = Answer.objects.filter(question = self.object)
        return context

# 回答作成
class CreateAnswer(LoginRequiredMixin,CreateView):
    template_name = 'detail_question.html'
    model = Answer
    form_class = AnswerForm
    
    # テンプレートに渡すデータの準備
    # kwargsとは、URLパターンで定義されたキーワード引数(例: <int:question_id>のquestion_id)が、ビューのメソッドにkwargsという辞書として渡される
    # 例えばquestion_id=123が渡された場合、ビューのメソッド内ではself.kwargsが{'question_id': 123}という辞書になる
    def get_context_data(self, **kwargs):
        # 親クラス（CreateView）がデフォで用意してくれるデータ(空のAnswerFormなど)をcontextに代入
        context = super().get_context_data(**kwargs)
        # 「どの質問に対する回答なのか」というQuestionオブジェクトをテンプレに渡している
        # そのIDを持つQuestionオブジェクトをDBから取得する。見つからなければ自動的に404エラーを出す
        context['question'] = get_object_or_404(Question, pk = self.kwargs.get('question_id'))
        # 何のquestion_idのAnswerオブジェクトを取得したいのか指定する必要がある
        context['answers'] = Answer.objects.filter(question = self.kwargs.get('question_id'))
        return context
    
    # フォームが正しく入力されたときの処理
    def form_valid(self, form):
        # form.instanceはユーザがフォームに入力したデータをもとに作られた、まだDBに保存されていないAnswerオブジェクトのこと
        # Answerオブジェクトのuserに、現在ログインしているユーザを設定している
        form.instance.user = self.request.user
        # Answerオブジェクトのquestionに、どの質問に対する回答なのかを示すQuestionオブジェクトを設定している
        form.instance.question = get_object_or_404(Question, pk=self.kwargs.get('question_id'))
        # 必要な情報をform.instanceに設定したら親クラス(CreateView)のform_validメソッドに処理を任せる
        # form_validはform.save()を実行してAnswerオブジェクトをDBに保存し、その後get_success_url()で指定されたページにリダイレクトする
        return super().form_valid(form)
    
    # 回答作成後のリダイレクト先
    def get_success_url(self):
        question_id = self.kwargs.get('question_id')
        return reverse('knowledgeapp:detail_question', kwargs={'question_id': question_id})

# 回答編集
class UpdateAnswer(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # CreateAnswerとは別テンプレにする
    # detail_question.htmlだと回答作成フォームだと認識されてしまう
    template_name = 'update_answer.html'
    model = Answer
    form_class = AnswerForm
    # UpdateViewはこのanswer_idを使ってDBから編集対象のAnswerオブジェクトを自動的に取得する
    pk_url_kwarg = 'answer_id'

    # ユーザがこの回答を編集する権限があるかチェック
    # UserPassesTestMixinが呼び出すメソッド
    def test_func(self):
        # UpdateViewがURLから取得した現在のAnswerオブジェクトを取得する
        answer = self.get_object()
        # ログインユーザが回答の投稿者と一致するか
        # 一致すればTrueを返し編集を許可する。一致しなければFalseを返しアクセスを拒否する
        return answer.user == self.request.user
    
    def get_context_data(self, **kwargs):
        # 親クラス（CreateView）がデフォで用意してくれるデータ(空のAnswerFormなど)をcontextに代入
        context = super().get_context_data(**kwargs)
        # 編集中のAnswerオブジェクトが紐付いているQuestionオブジェクトを取得し、テンプレにquestionという名前で渡す
        # questionはAnswerオブジェクトのquestion
        context['question'] = self.get_object().question
        context['answer'] = self.object
        return context

    # 回答編集後のリダイレクト先
    def get_success_url(self):
        # 編集された回答が紐付いている質問の詳細ページにリダイレクト
        # pk=idフィールドの値取得
        question_id = self.get_object().question.pk
        return reverse('knowledgeapp:detail_question', kwargs={'question_id': question_id})

# 回答削除
class DeleteAnswer(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    template_name = 'detail_question.html'
    model = Answer
    # DeleteViewはフォームを必要としないので、form_class = AnswerFormは削除すべき
    # DeleteViewはこのanswer_idを使ってDBから編集対象のAnswerオブジェクトを自動的に取得する
    pk_url_kwarg = 'answer_id'

    # ユーザがこの回答を削除する権限があるかチェック
    # UserPassesTestMixinが呼び出すメソッド
    def test_func(self):
        # DeleteViewがURLから取得した現在のAnswerオブジェクトを取得する
        answer = self.get_object()
        print(f"Answer user: {answer.user.id}, Request user: {self.request.user.id}")
        # ログインユーザが回答の投稿者と一致するか
        # 一致すればTrueを返し編集を許可する。一致しなければFalseを返しアクセスを拒否する
        return answer.user == self.request.user
        
    
    def get_context_data(self, **kwargs):
        # 親クラス（CreateView）がデフォで用意してくれるデータ(空のAnswerFormなど)をcontextに代入
        context = super().get_context_data(**kwargs)
        # 編集中のAnswerオブジェクトが紐付いているQuestionオブジェクトを取得し、テンプレにquestionという名前で渡す
        # questionはAnswerオブジェクトのquestion
        context['question'] = self.get_object().question
        return context

    # 回答削除後のリダイレクト先
    def get_success_url(self):
        # 削除された回答が紐付いている質問の詳細ページにリダイレクト
        # pk=idフィールドの値取得
        question_id = self.get_object().question.pk
        return reverse('knowledgeapp:detail_question', kwargs={'question_id': question_id})
