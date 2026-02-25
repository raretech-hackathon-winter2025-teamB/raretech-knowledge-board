from django import forms
from .models import Question, Answer

# 【ファイル責務】質問/回答の投稿・編集用フォーム定義

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'title', 'detail', 'image_url']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['detail', 'image_url']
