# RareTECHナレッジ掲示板 バックエンド構成管理書

- 文書版数: 1.0
- 更新日: 2026-02-15
- 対象: `app/` バックエンド実装

## 1. 構成管理方針

- バックエンド変更は `config` / `accounts` / `knowledgeapp` を責務単位で管理する。
- URL・View・Template の参照整合を必須確認とする。
- `default_storage` は環境変数 `USE_S3` で切替し、コード分岐を最小化する。
- 変更管理は `jj` を基本とし、論理単位でコミット分割する。

## 2. ディレクトリ構成（バックエンド）

- `app/config/`
  - `settings.py` : Django設定、DB、認証、Storage切替
  - `urls.py` : URL統合、エラーハンドラ定義
  - `error_views.py` : 4xx/5xx 応答
- `app/accounts/`
  - `models.py` : カスタムユーザ
  - `form.py` : サインアップフォーム
  - `views.py` : 認証、設定、退会
  - `urls.py` : 認証系URL
  - `migrations/` : スキーマ履歴
- `app/knowledgeapp/`
  - `models.py` : Category/Question/Answer/Bookmark
  - `forms.py` : QuestionForm
  - `views.py` : QA機能、画像アップロード
  - `urls.py` : QA/公開ページURL
  - `migrations/` : スキーマ履歴
- `app/manage.py` : 管理コマンド実行エントリ

## 3. ファイル責務台帳

## 3.1 config
- `app/config/settings.py`
  - DB接続
  - 認証系設定
  - 静的/メディア設定
  - `USE_S3` による `STORAGES` 切替
- `app/config/urls.py`
  - ルートURL集約
  - `handler400/403/404/500` 割当
- `app/config/error_views.py`
  - エラー文言管理（`ERROR_META`）
  - htmx向け断片応答

## 3.2 accounts
- `app/accounts/models.py`
  - `User` モデルと `CustomUserManager`
- `app/accounts/form.py`
  - `SignUpForm(UserCreationForm)`
- `app/accounts/views.py`
  - `LoginView`, `LogoutView`, `SignUpView`, `Setting`, `WithdrawView`
- `app/accounts/urls.py`
  - `signup/login/logout/setting/withdraw`

## 3.3 knowledgeapp
- `app/knowledgeapp/models.py`
  - `Category`, `Question`, `Answer`, `Bookmark`
- `app/knowledgeapp/forms.py`
  - `QuestionForm`
- `app/knowledgeapp/views.py`
  - 一覧/詳細/投稿/回答/ブックマーク/画像アップロード
  - 公開ページ（terms/privacy/features）
- `app/knowledgeapp/urls.py`
  - QA機能と公開コンテンツURL

## 4. 依存関係管理

- `requirements.txt`
  - `Django==5.2`
  - `mysqlclient==2.2.0`
  - `python-dotenv==1.0.0`
  - `gunicorn==21.2.0`
  - `Pillow==10.1.0`
  - `django-storages==1.14.4`
  - `boto3==1.35.67`

## 5. 環境変数管理

標準:
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_ROOT_PASSWORD`
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_TIME_ZONE`
- `DJANGO_LANGUAGE_CODE`

S3利用時:
- `USE_S3=True`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_REGION_NAME`
- `AWS_MEDIA_LOCATION`
- `AWS_S3_CUSTOM_DOMAIN`（任意）

## 6. 変更手順（標準）

1. 変更対象を分類（URL / View / Model / Settings）
2. 影響範囲調査
   - `rg` で参照先検索
   - URL逆引き（`reverse`, `name`）整合確認
3. 実装
   - 最小差分で反映
4. 検証
   - 起動確認
   - 対象API/UIの成功・失敗ケース確認
5. 差分確認
   - `jj diff` / `jj st`
6. 文書更新
   - 本書、仕様書、必要な運用手順書更新

## 7. 品質チェックリスト（バックエンド）

- URL name と View が重複/衝突していない
- 認証必須画面で未ログイン遷移が正しい
- htmx時の `HX-Redirect` / 部分HTML返却が正しい
- DB例外時の挙動が仕様どおり
- 画像アップロード保存先が環境設定どおり（ローカル/S3）
- エラーハンドラが 4xx/5xx で期待どおり動作

## 8. 既知リスクと管理対象

1. `knowledgeapp/urls.py` の同一URL重複（`question/<int:pk>/`）
- 管理: ルーティング修正時に最優先で解消する

2. `accounts.User.password` の `unique=True`
- 管理: モデル改修時に互換性を確認して是正検討

3. `Bookmark` のユニーク制約未設定
- 管理: DB制約追加時は既存データ重複を事前調査

4. S3切替時の運用依存
- 管理: `docs/s3_media_setup.md` を正とし、環境差分を運用手順へ反映

## 9. 付随文書

- `docs/backend_spec_doc.md` : バックエンド仕様
- `docs/s3_media_setup.md` : S3保存切替手順
- `docs/spec_doc.md` : 全体仕様（フロント含む）
- `docs/config_doc.md` : 全体構成管理（フロント含む）

## 10. バックエンドコメント運用ルール

### 10.1 目的
- 変更時の影響範囲を短時間で判断できる状態を維持する。
- URL / View / Model / Settings の責務境界を明確化する。

### 10.2 記法
- Pythonコメントは `#` を使用する。
- 形式は `【分類】説明` に統一する。
- 1コメント1責務とし、冗長な説明は避ける。

### 10.3 分類ラベル
- `【ファイル責務】` : ファイル冒頭で責務を明示する。
- `【セクション】` : クラス/関数/処理ブロックの目的を示す。
- `【遷移】` : リダイレクトや `HX-Redirect` 等の遷移意図を示す。
- `【例外】` : 例外処理の意図を示す。
- `【補足】` : 将来の保守で必要な前提事項を示す。

### 10.4 配置ルール
- 各ファイル先頭に `【ファイル責務】` を1つ置く。
- 長い関数では主要処理ブロック前に `【セクション】` を置く。
- 例外ハンドリング直前に `【例外】` を置く。
- 明白な代入・returnにはコメントを付けない。

### 10.5 禁止事項
- 実装と一致しない将来予定の記述をしない。
- コメントで仕様を隠蔽しない（仕様変更はコードと文書を同時更新）。
- 旧仕様の説明を残置しない。
