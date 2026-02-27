from django.urls import path
from . import views

app_name = "knowledgeapp"
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('home/', views.QuestionList.as_view(), name='question'),
    path('question/new/', views.QuestionCreate.as_view(), name='new_question'),
    path('question/<int:question_id>/', views.DeteilQuestion.as_view(), name='detail_question'),
    path('question/<int:question_id>/create_answer', views.CreateAnswer.as_view(), name='create_answer'),
    path('answer/<int:answer_id>/update_answer', views.UpdateAnswer.as_view(), name='update_answer'),
    path('answer/<int:answer_id>/delete_answer', views.DeleteAnswer.as_view(), name='delete_answer'),

]
