from django.contrib import admin
from .models import Question, Category, Answer, Bookmark

class CustomQuestion(admin.ModelAdmin):
    # どのフィールドを表示するかを指定
    list_display = (
        "id",
        "user",
        "category",
        "title",
        "detail",
    )
    list_filter = ("id",)



#管理画面の表示するテーブルを定義する。
admin.site.register(Question, CustomQuestion)
admin.site.register(Category)
admin.site.register(Answer)
admin.site.register(Bookmark)
