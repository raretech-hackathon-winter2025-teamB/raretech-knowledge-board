from django.db import models
from django.conf import settings



# Categoriesテーブルの定義
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='カテゴリ')

    def __str__(self):
        return self.name



#Questionsテーブルの定義
class Question(models.Model):
    STATUS = {
        '1':'解決済み',
        '2':'未解決',
    }
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='投稿者') #on_delete=models.SET_NULLユーザーが消えても質問は残る。
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #on_delete=models.CASECASE カテゴリが消えてら質問も消える。
    title = models.CharField(max_length=255, verbose_name='質問タイトル')
    detail = models.TextField(max_length=4000, verbose_name='質問本文')
    image_url = models.URLField(max_length=2048, verbose_name='画像URL', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')
    status = models.CharField(max_length=16, choices=STATUS, verbose_name='ステータス', default='2')

    def __str__(self):
        return self.title



#Answersテーブルの定義
class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='回答者')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='質問')
    detail = models.TextField(max_length=4000, verbose_name='回答本文')
    image_url = models.URLField(max_length=2048, verbose_name='画像URL', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='回答日時')

    def __str__(self):
        return self.question.title



#Bookmarksテーブルの定義
class Bookmark(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='回答者')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='質問')
    
    def __str__(self):
        return self.question.title