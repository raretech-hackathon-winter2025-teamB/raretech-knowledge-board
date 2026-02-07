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
    # このビューが使用するフォームクラスを指定
    form_class = SignUpForm
    #ユーザ作成後のリダイレクト先
    success_url = reverse_lazy("knowledgeapp:question")
    template_name = "accounts/signup.html"

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
    


