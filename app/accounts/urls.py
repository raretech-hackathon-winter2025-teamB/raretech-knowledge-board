from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('signup/',views.SignUpView.as_view(), name="signup" ),
    # LoginViewはデフォでdjango.contrib.auth.forms.AuthenticationFormというフォームクラスを使用するように設定されている
    # AuthenticationFormは、USERNAME_FIELDで指定されたフィールドとパスワードのフィールドを自動的に持っている
    # forms.pyに書かなくても、LoginViewが裏でAuthenticationFormをインスタンス化して、テンプレに{{ form.as_p }}を書けばフォームができる
    path(
        "login/",
        auth_views.LoginView.as_view(
          redirect_authenticated_user=True, template_name="accounts/login.html"
        ),# 認証済みの状態でログインページにアクセスした際にホーム画面にリダイレクト
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("setting/", views.Setting.as_view(), name="setting"),
]