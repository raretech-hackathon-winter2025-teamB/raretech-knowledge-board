from django.urls import path
from . import views

# 【ファイル責務】質問掲示板機能と公開コンテンツのURLを定義
app_name = "knowledgeapp"
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('home/', views.QuestionList.as_view(), name='question'),
    path('bookmark/', views.BookmarkList.as_view(), name='bookmark_legacy'),
    path('bookmarks/', views.BookmarkList.as_view(), name='bookmarks'),
    path('my-questions/', views.MyQuestionList.as_view(), name='my_questions'),
    path('how-to-ask/', views.HowToAskView.as_view(), name='how_to_ask'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('features/question-post/', views.FeatureQuestionPostView.as_view(), name='feature_question_post'),
    path('features/question-list/', views.FeatureQuestionListView.as_view(), name='feature_question_list'),
    path('features/question-guide/', views.FeatureQuestionGuideView.as_view(), name='feature_question_guide'),
    path('upload-image/', views.ImageUploadView.as_view(), name='upload_image'),
    path('question/<int:pk>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('question/<int:pk>/resolve/', views.QuestionResolve.as_view(), name='question_resolve'),
    path('question/<int:pk>/bookmark/', views.BookmarkToggle.as_view(), name='bookmark_toggle'),
    path('question/<int:pk>/answer/', views.AnswerCreate.as_view(), name='answer_create'),
    path('question/new/', views.QuestionCreate.as_view(), name='new_question'),
    path('delete_question/<int:pk>/', views.delete_question, name='delete_question'),
    path('question/<int:pk>/edit/', views.QuestionUpdate.as_view(), name='update_question'),
]
