from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Question

# 【ファイル責務】knowledgeappのアクセス制御テスト


class KnowledgeAppAccessControlTests(TestCase):
    # 【セクション】未ログイン遮断とログイン済み公開URLリダイレクトを検証
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            name="tester",
            email="tester-qa@example.com",
            password="StrongPass123!",
        )
        self.category = Category.objects.create(name="テストカテゴリ")
        self.question = Question.objects.create(
            user=self.user,
            category=self.category,
            title="テスト質問",
            detail="テスト詳細",
            status="2",
        )

    def test_public_pages_redirect_authenticated_user_to_home(self):
        self.client.force_login(self.user)
        public_urls = [
            reverse("knowledgeapp:top"),
            reverse("knowledgeapp:terms"),
            reverse("knowledgeapp:privacy_policy"),
            reverse("knowledgeapp:feature_question_post"),
            reverse("knowledgeapp:feature_question_list"),
            reverse("knowledgeapp:feature_question_guide"),
        ]
        for url in public_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, "/home/", fetch_redirect_response=False)

    def test_protected_pages_require_login(self):
        protected_urls = [
            reverse("knowledgeapp:question"),
            reverse("knowledgeapp:new_question"),
            reverse("knowledgeapp:my_questions"),
            reverse("knowledgeapp:bookmarks"),
            reverse("knowledgeapp:how_to_ask"),
            reverse("knowledgeapp:question_detail", kwargs={"pk": self.question.pk}),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith("/login/"))

    def test_protected_posts_require_login(self):
        post_targets = [
            (reverse("knowledgeapp:new_question"), {"title": "a", "detail": "b", "category": self.category.pk}),
            (reverse("knowledgeapp:question_resolve", kwargs={"pk": self.question.pk}), {}),
            (reverse("knowledgeapp:bookmark_toggle", kwargs={"pk": self.question.pk}), {}),
            (reverse("knowledgeapp:answer_create", kwargs={"pk": self.question.pk}), {"detail": "reply"}),
        ]
        for url, payload in post_targets:
            with self.subTest(url=url):
                response = self.client.post(url, payload)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith("/login/"))

    def test_protected_pages_accessible_when_authenticated(self):
        self.client.force_login(self.user)
        protected_urls = [
            reverse("knowledgeapp:question"),
            reverse("knowledgeapp:new_question"),
            reverse("knowledgeapp:my_questions"),
            reverse("knowledgeapp:bookmarks"),
            reverse("knowledgeapp:how_to_ask"),
            reverse("knowledgeapp:question_detail", kwargs={"pk": self.question.pk}),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
