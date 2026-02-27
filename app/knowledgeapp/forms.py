from django import forms
from .models import Question, Answer, Category

class QuestionForm(forms.ModelForm):
    # Categoryを選択するためのフィールドを追加
    # querysetにCategory.objects.all()を指定することで、DBの全てのカテゴリが選択肢になる
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), # ここでDBからタグを取得
        required=True, # カテゴリ選択は必須
        empty_label="カテゴリを選択してください", # 選択なしのオプション
        # Selectウィジェットを使用(一つしか選択できない)
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = Question
        # フォームで入力させるフィールド
        fields = ['title', 'category', 'detail', 'image_url']
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1, 'placeholder': 'タイトルを入力してください...'}),
            'detail': forms.Textarea(attrs={'rows': 5, 'placeholder': '詳細を入力してください...'}),
            'image_url': forms.URLInput(attrs={'placeholder': '画像のURL (任意)'}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        # フォームで入力させるフィールド
        fields = ['detail', 'image_url']
        widgets = {
            'detail': forms.Textarea(attrs={'rows': 5, 'placeholder': '回答を入力してください...'}),
            'image_url': forms.URLInput(attrs={'placeholder': '画像のURL (任意)'}),
        }
