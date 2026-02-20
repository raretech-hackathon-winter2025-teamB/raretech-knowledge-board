# RareTECHナレッジ掲示板 バックエンド仕様書

- 文書版数: 1.0
- 更新日: 2026-02-15
- 対象: `app/` 配下バックエンド（Django 5.2）
- 前提: Python 3.10 / MySQL 8 / django-storages + boto3（S3利用時）

## 1. 概要

本アプリは Django テンプレートアプリケーションであり、バックエンドは以下を提供する。

- 認証（signup/login/logout/withdraw）
- 質問・回答・ブックマーク管理
- 画像アップロード（`default_storage` 経由）
- 4xx/5xx エラー応答（通常HTML + htmx断片）

## 2. 技術仕様

- Framework: Django `5.2`
- DB: MySQL（`config/settings.py` の `DATABASES`）
- 認証: カスタムユーザ（`accounts.User`）
- Storage:
  - `USE_S3=False` の場合: ローカル `MEDIA_ROOT`
  - `USE_S3=True` の場合: S3（`STORAGES['default'] = storages.backends.s3.S3Storage`）
- 主要レスポンス:
  - 通常リクエスト: HTMLリダイレクト/テンプレート応答
  - htmxリクエスト: 部分HTML + `HX-Redirect`/`HX-Retarget` 等

## 3. ドメインモデル

## 3.1 accounts.User
- PK: `UUIDField`
- 主な項目: `name`, `email(unique)`, `password(unique)`, `is_active`, `is_staff`, `is_superuser`
- 認証識別子: `USERNAME_FIELD = email`

注意:
- `password` フィールドに `unique=True` が付与されている。一般的には非推奨構成であり、運用上の制約になり得る。

## 3.2 knowledgeapp.Category
- 項目: `id`, `name(50)`

## 3.3 knowledgeapp.Question
- 項目: `user(FK)`, `category(FK)`, `title`, `detail`, `image_url`, `created_at`, `status`
- `status`: `'1'=解決済み`, `'2'=未解決`（デフォルト `'2'`）

## 3.4 knowledgeapp.Answer
- 項目: `user(FK)`, `question(FK)`, `detail`, `image_url`, `created_at`

## 3.5 knowledgeapp.Bookmark
- 項目: `user(FK)`, `question(FK)`
- ユニーク制約は未定義（View側で存在確認して重複作成を抑制）

## 4. ルーティング仕様

## 4.1 ルート統合（`config/urls.py`）
- `''` -> `knowledgeapp.urls`
- `''` -> `accounts.urls`
- `''` -> `django.contrib.auth.urls`
- `/errors/<code>/` 系プレビューと固定エラーURL
- DEBUG時のみ `MEDIA_URL` を配信

## 4.2 認証系（`accounts/urls.py`）
- `GET/POST /signup/` : `SignUpView`
- `GET/POST /login/` : `LoginView`
- `GET/POST /logout/` : `LogoutView`
- `GET /setting/` : `Setting`（ログイン必須）
- `POST /withdraw/` : `WithdrawView`（ログイン必須）

## 4.3 QA系（`knowledgeapp/urls.py`）
- `GET /` : `TopView`
- `GET /home/` : `QuestionList`
- `GET /my-questions/` : `MyQuestionList`
- `GET /bookmarks/` : `BookmarkList`
- `GET /bookmark/` : `BookmarkList`（旧互換）
- `GET /question/new/` : `QuestionCreate`
- `POST /question/new/` : `QuestionCreate`
- `GET /question/<int:pk>/` : `QuestionDetail`（実質有効）
- `POST /question/<int:pk>/resolve/` : `QuestionResolve`
- `POST /question/<int:pk>/bookmark/` : `BookmarkToggle`
- `POST /question/<int:pk>/answer/` : `AnswerCreate`
- `POST|GET /upload-image/` : `ImageUploadView(postのみ)`
- `GET /how-to-ask/`, `GET /terms/`, `GET /privacy-policy/`, `GET /features/*`

注意:
- `knowledgeapp/urls.py` には `path('question/<int:pk>/', QuestionDetail)` と `path('question/<int:pk>/', QuestionUpdate)` が重複定義されており、後者は通常到達しない。

## 5. ユースケース別仕様

## 5.1 サインアップ
- `SignUpForm` バリデーション成功時にユーザ作成
- 直後に `login()` 実行
- htmx時: `HX-Redirect: /home/`
- 非htmx時: `/home/` へ `redirect`

## 5.2 ログイン
- `LoginView` で認証
- `redirect_authenticated_user = True`
- htmx時: `HX-Redirect` 返却

## 5.3 ログアウト
- `GET`/`POST` どちらも同一処理
- htmx時: `HX-Redirect: /`
- 非htmx時: `/` へ `redirect`

## 5.4 退会
- `current_password` 検証
- 不一致: `messages.error` + `/setting/` へ戻す
- 一致: `logout` -> `user.delete`

## 5.5 質問一覧/検索
- 検索条件: `q`, `category`, `status`
- 例外時（DB未作成/接続問題等）は空配列返却で表示継続

## 5.6 質問投稿
- 未ログインは `/login/` へ誘導
- 投稿時に `user` と `status='2'` を設定

## 5.7 質問詳細・回答投稿
- 詳細で `answers` を時系列取得
- 回答投稿はログイン必須
- `detail` が空なら保存しない

## 5.8 ブックマーク切替
- ログイン必須
- 既存あれば削除、なければ作成
- htmx時はボタン部品HTMLを返却

## 5.9 画像アップロード
- 拡張子許可: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- 保存先: `uploads/<uuid>.<ext>`（`default_storage`）
- htmx時: `data-target`, `data-name`, `data-url` を返却
- 非htmx時: `{"url": "..."}`

## 6. エラー応答仕様（`config/error_views.py`）

- ハンドラ: `400/403/404/500`
- 追加画面: `405/429/502/503`
- htmx時:
  - テンプレート: `errors/partials/error_panel.html`
  - `HX-Reselect: #error-panel`
  - `HX-Retarget: main`
  - `HX-Reswap: innerHTML`
- 共通: `Cache-Control: no-store`

## 7. 設定仕様（`config/settings.py`）

- `AUTH_USER_MODEL = "accounts.User"`
- 認証遷移:
  - `LOGIN_URL = "/login/"`
  - `LOGIN_REDIRECT_URL = "/home/"`
  - `LOGOUT_REDIRECT_URL = "/login"`
- Storage切替:
  - `USE_S3=False`: ローカル `MEDIA_ROOT`
  - `USE_S3=True`: S3設定を有効化し `default_storage` を S3 へ切替

## 8. 既知制約・課題

1. `knowledgeapp/urls.py` の同一パス重複定義（`question/<pk>/`）
2. `accounts.User.password` の `unique=True`
3. `Bookmark` のDBユニーク制約未定義
4. 一部ViewでDB障害時に空表示へフォールバックするため、障害検知が遅れる可能性

## 9. テスト観点（最小）

1. 認証成功/失敗（htmx・通常）で遷移が正しい
2. `/upload-image/` が保存先（ローカル or S3）へ正しく保存する
3. 質問・回答・ブックマークのCRUDが期待どおり
4. 4xx/5xx を htmx/通常の双方で表示できる
5. URL重複パスの意図確認（`QuestionUpdate` 到達性）
