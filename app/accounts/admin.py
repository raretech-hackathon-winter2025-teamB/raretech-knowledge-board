from django.contrib import admin
# デフォルトのUserモデルの管理クラスをインポート。これを継承することで既存の管理機能を再利用しつつカスタムユーザーモデルに合わせて変更可
from django.contrib.auth.admin import UserAdmin

from .models import User

# Djangoの管理サイトでカスタムユーザーモデルを使いやすくするための設定
class CustomUserAdmin(UserAdmin):
    # どのフィールドを表示するかを指定
    list_display = (
        "name",
        "email",
        "is_staff",
        "is_active",
    )

    # 検索ボックスに入力されたキーワードがどのフィールドに対して検索されるかを指定
    search_fields = ("name", "email")

    # ユーザーがどのフィールドでソート（並べ替え）されるかを指定
    ordering = ("email",)

    fieldsets = (("User Info", {"fields": ("name", "email", "password")}),)

    # 新しいユーザーを追加する際のフォームの表示をカスタマイズ
    # デフォルトのUserAdminは多くのフィールドを持っているが、カスタムユーザーモデルに合わせて必要なものだけを表示している
    add_fieldsets = (
        (
            None,
            {
                "fields": ("name", "email", "password"),
            },
        ),
    )

# Djangoの管理サイトに「Userモデルを、CustomUserAdminで定義した設定を使って登録してください」という指示
admin.site.register(User, CustomUserAdmin)