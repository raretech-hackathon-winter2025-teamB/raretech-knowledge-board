from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True, template_name="app/pages/auth/login.html"
        ),  # 認証済みの状態でログインページにアクセスした際にホーム画面にリダイレクト
        name="login",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("setting/", views.Setting.as_view(), name="setting"),
    path("withdraw/", views.WithdrawView.as_view(), name="withdraw"),
]
