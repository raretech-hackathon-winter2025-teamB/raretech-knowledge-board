from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.utils import ProgrammingError, OperationalError
from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .models import Question, Category, Answer, Bookmark
from django.urls import reverse_lazy, reverse
import os
import uuid
from django.utils.html import escape
from django.template.loader import render_to_string
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
    template_name = 'public/pages/home.html'


#いい質問の仕方画面の表示
class HowToAskView(TemplateView):
    template_name = 'app/pages/qa/how_to_ask.html'


class TermsView(TemplateView):
    template_name = 'public/pages/terms.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'public/pages/privacy_policy.html'


class FeatureQuestionPostView(TemplateView):
    template_name = 'public/pages/features/question_post.html'


class FeatureQuestionListView(TemplateView):
    template_name = 'public/pages/features/question_list.html'


class FeatureQuestionGuideView(TemplateView):
    template_name = 'public/pages/features/question_guide.html'


#質問一覧の表示
class QuestionList(ListView):
    template_name = 'app/pages/qa/question_list.html'
    model = Question

    def get_queryset(self):
        queryset = Question.objects.select_related('category').order_by('-created_at')
        keyword = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '').strip()
        status = self.request.GET.get('status', '').strip()

        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        if category:
            queryset = queryset.filter(category__name=category)
        if status in {'1', '2'}:
            queryset = queryset.filter(status=status)

        try:
            return list(queryset)
        except (ValidationError, ValueError, ProgrammingError, OperationalError):
            # UUID不整合やテーブル未作成時でも画面表示を継続するため空で返す
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_q'] = self.request.GET.get('q', '').strip()
        context['selected_category'] = self.request.GET.get('category', '').strip()
        context['selected_status'] = self.request.GET.get('status', '').strip()
        try:
            context['categories'] = list(Category.objects.order_by('name').values_list('name', flat=True))
        except (ProgrammingError, OperationalError):
            context['categories'] = []
        context['bookmarked_question_ids'] = set()
        if self.request.user.is_authenticated and context.get('object_list'):
            question_ids = [q.id for q in context['object_list']]
            try:
                context['bookmarked_question_ids'] = set(
                    Bookmark.objects.filter(
                        user=self.request.user,
                        question_id__in=question_ids,
                    ).values_list('question_id', flat=True)
                )
            except (ProgrammingError, OperationalError):
                context['bookmarked_question_ids'] = set()
        return context

# def homeview(request):
#     return render(request, 'home.html')

#質問投稿画面の表示
class QuestionCreate(CreateView):
    template_name = 'app/pages/qa/question_form.html'
    model = Question
    form_class = QuestionForm
    # fields = ('title', 'category', 'detail', 'image_url')  #create時に必要な項目をmodelから選んでおく。
    success_url = reverse_lazy('knowledgeapp:question') #データを登録後、urls.pyのなかのname=○○の箇所に遷移させる。

    def form_valid(self, form):
        # 未ログイン時の投稿は認証画面へ誘導する
        if not self.request.user.is_authenticated:
            return redirect('/login/')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['categories'] = list(Category.objects.order_by('name'))
        except (ProgrammingError, OperationalError):
            context['categories'] = []
        return context


# 自分の質問一覧の表示
class MyQuestionList(ListView):
    template_name = 'app/pages/qa/my_questions.html'
    model = Question

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return []

        queryset = Question.objects.select_related('category').filter(user=self.request.user).order_by('-created_at')
        keyword = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '').strip()
        status = self.request.GET.get('status', '').strip()
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        if category:
            queryset = queryset.filter(category__name=category)
        if status in {'1', '2'}:
            queryset = queryset.filter(status=status)

        try:
            return list(queryset)
        except (ValidationError, ValueError, ProgrammingError, OperationalError):
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_q'] = self.request.GET.get('q', '').strip()
        context['selected_category'] = self.request.GET.get('category', '').strip()
        context['selected_status'] = self.request.GET.get('status', '').strip()
        try:
            context['categories'] = list(Category.objects.order_by('name').values_list('name', flat=True))
        except (ProgrammingError, OperationalError):
            context['categories'] = []
        return context


class BookmarkList(ListView):
    template_name = 'app/pages/qa/bookmarks.html'
    model = Question

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return []

        keyword = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '').strip()
        status = self.request.GET.get('status', '').strip()
        try:
            queryset = (
                Question.objects.select_related('category')
                .filter(bookmark__user=self.request.user)
                .distinct()
                .order_by('-created_at')
            )
            if keyword:
                queryset = queryset.filter(title__icontains=keyword)
            if category:
                queryset = queryset.filter(category__name=category)
            if status in {'1', '2'}:
                queryset = queryset.filter(status=status)
            return list(queryset)
        except (ValidationError, ValueError, ProgrammingError, OperationalError):
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_q'] = self.request.GET.get('q', '').strip()
        context['selected_category'] = self.request.GET.get('category', '').strip()
        context['selected_status'] = self.request.GET.get('status', '').strip()
        try:
            context['categories'] = list(Category.objects.order_by('name').values_list('name', flat=True))
        except (ProgrammingError, OperationalError):
            context['categories'] = []
        context['bookmarked_question_ids'] = set()
        if self.request.user.is_authenticated and context.get('object_list'):
            context['bookmarked_question_ids'] = {q.id for q in context['object_list']}
        return context


class QuestionDetail(DetailView):
    template_name = 'app/pages/qa/question_detail.html'
    model = Question
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return Question.objects.select_related('user', 'category')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except (Question.DoesNotExist, ProgrammingError, OperationalError):
            raise Http404("Question not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['answers'] = list(
                Answer.objects.select_related('user')
                .filter(question=self.object)
                .order_by('created_at')
            )
        except (ProgrammingError, OperationalError):
            context['answers'] = []
        return context


class AnswerCreate(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('/login/')

        try:
            question = Question.objects.get(pk=pk)
        except (Question.DoesNotExist, ProgrammingError, OperationalError):
            raise Http404("Question not found")

        detail = request.POST.get('detail', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        if detail:
            Answer.objects.create(
                user=request.user,
                question=question,
                detail=detail,
                image_url=image_url or None,
            )
        return redirect(reverse('knowledgeapp:question_detail', kwargs={'pk': question.pk}))


class QuestionResolve(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('/login/')

        try:
            question = Question.objects.get(pk=pk)
        except (Question.DoesNotExist, ProgrammingError, OperationalError):
            raise Http404("Question not found")

        if question.user_id != request.user.id:
            return redirect(reverse('knowledgeapp:question_detail', kwargs={'pk': pk}))

        if question.status != '1':
            question.status = '1'
            question.save(update_fields=['status'])

        return redirect(reverse('knowledgeapp:question_detail', kwargs={'pk': pk}))


class BookmarkToggle(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('/login/')

        question = get_object_or_404(Question, pk=pk)
        try:
            bookmark_qs = Bookmark.objects.filter(user=request.user, question=question)
            if bookmark_qs.exists():
                bookmark_qs.delete()
                is_bookmarked = False
            else:
                Bookmark.objects.create(user=request.user, question=question)
                is_bookmarked = True
        except (ProgrammingError, OperationalError):
            is_bookmarked = False

        if request.headers.get('HX-Request') == 'true':
            context = {
                'q': question,
                'is_bookmarked': is_bookmarked,
                'bookmarked_question_ids': {question.id} if is_bookmarked else set(),
            }
            return HttpResponse(
                render_to_string('app/components/qa/_bookmark_button_partial.html', context=context, request=request)
            )

        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/home/'
        return redirect(next_url)


class ImageUploadView(View):
    def post(self, request):
        upload = request.FILES.get('image')
        if not upload:
            return HttpResponse("<div class='text-red-600 text-xs mt-2'>ファイルが選択されていません。</div>", status=400)

        ext = os.path.splitext(upload.name)[1].lower()
        if ext not in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
            return HttpResponse("<div class='text-red-600 text-xs mt-2'>対応していないファイル形式です。</div>", status=400)

        path = f"uploads/{uuid.uuid4().hex}{ext}"
        saved_path = default_storage.save(path, upload)
        url = default_storage.url(saved_path)
        target_field = request.POST.get('target_field', 'id_detail')
        filename = escape(upload.name)
        escaped_url = escape(url)
        escaped_target = escape(target_field)

        if request.headers.get('HX-Request') == 'true':
            return HttpResponse(
                f"""
                <div class="hidden" data-target="{escaped_target}" data-name="{filename}" data-url="{escaped_url}"></div>
                """
            )

        return JsonResponse({'url': url})
