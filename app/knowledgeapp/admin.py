from django.contrib import admin
from .models import Question, Category, Answer, Bookmark


#管理画面の表示するテーブルを定義する。
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Answer)
admin.site.register(Bookmark)
