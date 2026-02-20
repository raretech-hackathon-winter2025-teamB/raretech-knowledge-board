from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# 【ファイル責務】accountsアプリのアクセス制御テスト


class AuthPublicAccessControlTests(TestCase):
    # 【セクション】ログイン済みユーザーの公開認証URLアクセス制御を検証
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            name="tester",
            email="tester-auth@example.com",
            password="StrongPass123!",
        )

    def test_login_page_redirects_authenticated_user_to_home(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("accounts:login"))
        self.assertRedirects(response, "/home/", fetch_redirect_response=False)

    def test_signup_page_redirects_authenticated_user_to_home(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("accounts:signup"))
        self.assertRedirects(response, "/home/", fetch_redirect_response=False)

    def test_setting_requires_login(self):
        response = self.client.get(reverse("accounts:setting"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login/"))
