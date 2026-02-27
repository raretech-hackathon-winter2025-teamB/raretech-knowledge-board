from django import forms
from django.contrib.auth import get_user_model
# Djangoが提供するユーザー登録（アカウント作成）のための便利なフォームクラス
# カスタムユーザーモデルを使用している場合に、ユーザー登録フォームを簡単に作成できるように設計されている
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    #Noneにしてもパスワードフォームは表示してるからなくても良い？
    usable_password = None

    class Meta:
        model = User
        # 本来ユーザ名とパスワード（確認用パスワードを含む）はデフォで提供
        # USERNAME_FIELDがemailなのでnameは明示的に追加する必要がある
        # emailは通常含まれるが、なぜか入れないと表示されないので追加
        fields = ('name', 'email',)