from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth import password_validation
from django.views.generic import CreateView, View
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.urls import reverse_lazy
from .form import SignUpForm

# 【ファイル責務】認証（login/signup/logout）と設定/退会のViewを提供


class RedirectAuthenticatedToHomeMixin:
    # 【ファイル責務】ログイン済みユーザーの公開認証ページアクセスを/homeへ統一
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/home/")
        return super().dispatch(request, *args, **kwargs)

# ユーザ編集画面
class Setting(LoginRequiredMixin, View):
    template_name = "app/pages/profile/setting.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        action = request.POST.get("action", "")
        user = request.user

        if action == "update_name":
            name = request.POST.get("name", "").strip()
            if not name:
                messages.error(request, "ユーザー名を入力してください。")
            else:
                user.name = name
                user.save(update_fields=["name"])
                messages.success(request, "ユーザー名を変更しました。")

        elif action == "update_email":
            email = request.POST.get("email", "").strip()
            if not email:
                messages.error(request, "メールアドレスを入力してください。")
            else:
                User = get_user_model()
                if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                    messages.error(request, "このメールアドレスは既に使用されています。")
                else:
                    user.email = email
                    user.save(update_fields=["email"])
                    messages.success(request, "メールアドレスを変更しました。")

        elif action == "update_password":
            current_password = request.POST.get("current_password", "")
            new_password1 = request.POST.get("new_password1", "")
            new_password2 = request.POST.get("new_password2", "")

            if not user.check_password(current_password):
                messages.error(request, "現在のパスワードが正しくありません。")
            elif new_password1 != new_password2:
                messages.error(request, "新しいパスワードが一致しません。")
            else:
                try:
                    password_validation.validate_password(new_password1, user)
                except ValidationError as e:
                    messages.error(request, e.messages[0])
                else:
                    user.set_password(new_password1)
                    user.save(update_fields=["password"])
                    update_session_auth_hash(request, user)
                    messages.success(request, "パスワードを変更しました。")

        if request.headers.get("HX-Request") == "true":
            response = HttpResponse("")
            response["HX-Redirect"] = "/setting/"
            return response
        return redirect("/setting/")


class LogoutView(View):
    def get(self, request):
        # 【セクション】ログアウト実行後、htmx時はHX-Redirectでトップへ遷移
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
        # 【セクション】現在パスワード検証
        current_password = request.POST.get("current_password", "")
        user = request.user

        if not current_password or not user.check_password(current_password):
            # 【例外】パスワード不一致時は設定画面へ戻す
            messages.error(request, "現在のパスワードが正しくありません。")
            return redirect("/setting/")

        # 【セクション】退会処理
        logout(request)
        user.delete()

        if request.headers.get("HX-Request") == "true":
            response = HttpResponse("")
            response["HX-Redirect"] = "/"
            return response
        return redirect("/")


class LoginView(RedirectAuthenticatedToHomeMixin, auth_views.LoginView):
    template_name = "app/pages/auth/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        # 【遷移】htmxログイン成功時はHX-Redirectで遷移
        response = super().form_valid(form)
        if self.request.headers.get("HX-Request") == "true":
            htmx_redirect = HttpResponse("")
            htmx_redirect["HX-Redirect"] = self.get_success_url()
            return htmx_redirect
        return response


# ユーザ登録
class SignUpView(RedirectAuthenticatedToHomeMixin, CreateView):
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
        if self.request.headers.get("HX-Request") == "true":
            # 【遷移】htmx登録成功時はHX-Redirectで遷移
            response = HttpResponse("")
            response["HX-Redirect"] = self.get_success_url()
            return response
        # self.get_success_url()は、クラス属性success_urlの値を返すメソッド
        return redirect(self.get_success_url())
