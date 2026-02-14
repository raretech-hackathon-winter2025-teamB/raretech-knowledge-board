from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("setting/", views.Setting.as_view(), name="setting"),
    path("withdraw/", views.WithdrawView.as_view(), name="withdraw"),
]
