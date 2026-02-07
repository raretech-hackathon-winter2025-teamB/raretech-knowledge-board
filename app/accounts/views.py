from django.contrib.auth import login
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .form import SignUpForm

# ユーザ編集画面
class Setting(LoginRequiredMixin, TemplateView):
  template_name = "accounts/setting.html"

# ユーザ編集
  def setting(request):
      if request.method == "POST":
          user = request.user
          user.email = request.POST["email"]
          user.name = request.POST["name"]
          user.password = request.POST["password"]
          user.save()
          return redirect("accounts:setting")
      else:
          return render(request, "home.html")
    
# ユーザ登録
class SignUpView(CreateView):
    form_class = SignUpForm
    #ユーザ作成後のリダイレクト先
    success_url = reverse_lazy("accounts:setting")
    template_name = "accounts/signup.html"

    # form_valid:フォームが有効な場合に呼ばれ、ユーザーを保存し自動的にログインする
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return redirect(self.get_success_url())
    


