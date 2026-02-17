from django import forms
from .models import Question

# 【ファイル責務】質問投稿/編集用フォーム定義

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'title', 'detail', 'image_url']
