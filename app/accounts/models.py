from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin,)
from django.db import models
import uuid

# 【ファイル責務】カスタムユーザーモデルとユーザー作成マネージャーを定義
# AbstractBaseUserを使う場合、カスタムマネージャーの定義が必要
# 新しい一般ユーザーを作成するためのロジックを定義
class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
         # パスワードをハッシュ化して設定
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # 新しいスーパーユーザー（管理者権限を持つユーザー）を作成するためのロジックを定義
    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)# 管理サイトへのアクセス権
        extra_fields.setdefault("is_superuser", True)# 全ての権限
        extra_fields.setdefault('is_active', True) # アカウントが有効(スーパーユーザーは通常アクティブ)
        # create_userメソッドを再利用してスーパーユーザーを作成
        return self.create_user(name, email, password, **extra_fields)

# AbstractBaseUserはDjangoの認証システムにおいて、ユーザーモデルが最低限持つべき機能やインターフェースを提供する基底クラス
# 継承することで、自分で作ったユーザーモデルが「これはDjangoの認証システムで使えるユーザーモデルだよ」と認識されるようになる
# パスワードのハッシュ化、パスワードの検証、セッション管理などが利用できるようになり自分で実装しなくて良い
# models.ModelだけだとDjangoの認証システムと連携しなくなってしまう
# PermissionsMixinはDjangoの認証システムにおいて、ユーザーの権限（パーミッション）を管理するための機能を提供するMixinクラス
class User(AbstractBaseUser, PermissionsMixin):
    # default=uuid.uuid4はuuidを自動で生成し設定してくれる
    # editable=Falseは値変更不可
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    # uniqueがあれば空が許されない
    name = models.CharField(max_length=50, unique=False, verbose_name='ユーザ名')
    email = models.EmailField(max_length=255, unique=True, verbose_name='メールアドレス')
    password = models.CharField(max_length=255, unique=True, verbose_name='パスワード')
    # PermissionsMixinで提供されるフィールドのデフォルト値を設定
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # 作成したカスタムマネージャー(Userクラス)をオブジェクトとして使えるようにするため？
    objects = CustomUserManager()

    # 認証に使うフィールドを指定
    # ログイン時にユーザー名ではなくメールアドレスで認証するようになる
    USERNAME_FIELD = "email"
    # createsuperuserコマンドを実行した際にメアドとパスワードに加えて、nameフィールドの入力が求められるようになる
    REQUIRED_FIELDS = ["name"]

    # 管理サイトの画面上で使われる
    # Userオブジェクトを管理画面で表示する時どのデータが判別しやすいか(今回はemailで各データを判別)
    def __str__(self):
      return self.email
