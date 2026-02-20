# バックエンド テスト設計書（アクセス制御）

- 文書版数: 1.0
- 更新日: 2026-02-15
- 対象: 未ログイン遮断 / ログイン済み公開URLリダイレクト
- 対象コード:
  - `app/knowledgeapp/views.py`
  - `app/accounts/views.py`

## 1. テスト目的

- 未ログインユーザーがログイン後画面へアクセスできないことを担保する。
- ログイン済みユーザーが公開URLへアクセスした際に `/home/` へリダイレクトされることを担保する。
- GET/POSTの入口で意図どおりアクセス制御が機能することを確認する。

## 2. テスト範囲

## 2.1 In Scope
- 認証公開URL:
  - `/login/`, `/signup/`
- 公開URL:
  - `/`, `/terms/`, `/privacy-policy/`, `/features/*`
- ログイン後画面:
  - `/home/`, `/question/new/`, `/my-questions/`, `/bookmarks/`, `/how-to-ask/`, `/question/<pk>/`
- ログイン後POST:
  - `/question/new/`, `/question/<pk>/resolve/`, `/question/<pk>/bookmark/`, `/question/<pk>/answer/`

## 2.2 Out of Scope
- UIレンダリング詳細（文言・CSS）
- 画像アップロード機能の正常系/異常系
- DB障害時のフォールバック挙動

## 3. テスト観点

1. ログイン済みユーザーの公開ページアクセス制御
2. 未ログインユーザーのログイン後ページアクセス遮断（GET）
3. 未ログインユーザーのログイン後操作遮断（POST）
4. ログイン済みユーザーのログイン後ページ正常アクセス

## 4. テストケース一覧

## 4.1 accounts
- `AuthPublicAccessControlTests.test_login_page_redirects_authenticated_user_to_home`
- `AuthPublicAccessControlTests.test_signup_page_redirects_authenticated_user_to_home`
- `AuthPublicAccessControlTests.test_setting_requires_login`

## 4.2 knowledgeapp
- `KnowledgeAppAccessControlTests.test_public_pages_redirect_authenticated_user_to_home`
- `KnowledgeAppAccessControlTests.test_protected_pages_require_login`
- `KnowledgeAppAccessControlTests.test_protected_posts_require_login`
- `KnowledgeAppAccessControlTests.test_protected_pages_accessible_when_authenticated`

## 5. 期待結果

- 公開URLアクセス（ログイン済み）: `302` かつ `/home/` へ遷移
- 保護URLアクセス（未ログイン）: `302` かつ `/login/` へ遷移
- 保護URLアクセス（ログイン済み）: `200`

## 6. 実行手順

1. 作業ディレクトリへ移動
   - `cd app`
2. テスト実行
   - `python manage.py test accounts knowledgeapp`

## 7. 合否判定

- 全テストケースが `OK` の場合を合格とする。
- 失敗時は以下を切り分ける。
  - URLルーティング重複/誤設定
  - `LoginRequiredMixin` 付与漏れ
  - 公開Viewへのリダイレクトミックスイン適用漏れ
