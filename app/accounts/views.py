from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import CreateView, TemplateView, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from .form import SignUpForm


# ユーザ編集画面
class Setting(LoginRequiredMixin, TemplateView):
    template_name = "app/pages/profile/setting.html"


class LogoutView(View):
    def get(self, request):
        logout(request)
        if request.headers.get("HX-Request") == "true":
            response = HttpResponse("")
            response["HX-Redirect"] = "/"
            return response
        return redirect("/")

    def post(self, request):
        return self.get(request)


class WithdrawView(LoginRequiredMixin, View):
    def post(self, request):
        current_password = request.POST.get("current_password", "")
        user = request.user

        if not current_password or not user.check_password(current_password):
            messages.error(request, "現在のパスワードが正しくありません。")
            return redirect("/setting/")

        logout(request)
        user.delete()

        if request.headers.get("HX-Request") == "true":
            response = HttpResponse("")
            response["HX-Redirect"] = "/"
            return response
        return redirect("/")


# ユーザ登録
class SignUpView(CreateView):
    # このビューが使用するフォームクラスを指定
    form_class = SignUpForm
    # ユーザ作成後のリダイレクト先
    success_url = reverse_lazy("knowledgeapp:question")
    template_name = "app/pages/auth/signup.html"

    # CreateViewはフォームがバリデーションに成功したときに自動的にform_valid()メソッドを呼び出す
    # デフォのform_valid()の動作をカスタマイズする
    def form_valid(self, form):
        # 新しいUserオブジェクトをDBに保存
        user = form.save()
        # django.contrib.authが提供するlogin関数を呼び出して、今作成したばかりのユーザをその場でログインさせている
        login(self.request, user)
        # 作成されたオブジェクトをself.objectに設定している
        # CreateViewの場合フォームが保存された後、新しく作成されたモデルインスタンスがこのself.objectに設定されることが期待されている
        self.object = user
        # self.get_success_url()は、クラス属性success_urlの値を返すメソッド
        return redirect(self.get_success_url())
