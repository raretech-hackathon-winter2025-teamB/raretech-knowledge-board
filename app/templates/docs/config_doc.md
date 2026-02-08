# RareTECHナレッジ掲示板 構成管理書

- 文書版数: 0.2
- 更新日: 2026-02-13
- 対象: `app/` 配下

## 1. 構成管理方針
- 画面は「公開」「ログイン後」でディレクトリ分離する。
- `template_name` と実ファイルの対応を1対1で管理する。
- htmx部分更新の対象はパーシャル化して再利用する。
- スタイルは既存色定義（16進数）を維持し、変更時は全画面影響を確認する。
- 変更履歴管理は`jj`を基本とする。

## 2. ディレクトリ標準

### 2.1 アプリケーション
- `accounts/` : 認証・マイページ・退会
- `knowledgeapp/` : 質問/回答/ブックマーク/ガイド
- `config/` : Django設定・URL統合
- `static/` : グローバルCSS・共通JS
- `media/` : アップロード画像保存先

### 2.2 テンプレート
- `templates/layouts/` : ベースレイアウト
- `templates/public/pages/` : 公開ページ
- `templates/public/components/` : 公開共通部品
- `templates/app/pages/` : ログイン後ページ
- `templates/app/components/` : ログイン後共通部品・パーシャル
- `templates/docs/` : 本仕様書・構成管理書

## 3. 現行テンプレート構成

### 3.1 Layout
- `templates/layouts/public_base.html`
- `templates/layouts/app_base.html`

### 3.2 Public pages
- `templates/public/pages/home.html`
- `templates/public/pages/terms.html`
- `templates/public/pages/privacy_policy.html`
- `templates/public/pages/features/question_post.html`
- `templates/public/pages/features/question_list.html`
- `templates/public/pages/features/question_guide.html`

### 3.3 App pages
- `templates/app/pages/auth/login.html`
- `templates/app/pages/auth/signup.html`
- `templates/app/pages/profile/setting.html`
- `templates/app/pages/qa/question_list.html`
- `templates/app/pages/qa/question_form.html`
- `templates/app/pages/qa/question_detail.html`
- `templates/app/pages/qa/my_questions.html`
- `templates/app/pages/qa/bookmarks.html`
- `templates/app/pages/qa/how_to_ask.html`

### 3.4 App components
- `templates/app/components/sidebar.html`
- `templates/app/components/message.html`
- `templates/app/components/auth/*`
- `templates/app/components/legal/*`
- `templates/app/components/editor/*`
- `templates/app/components/qa/*`

## 4. 命名規約
- 画面テンプレート: `snake_case.html`
- パーシャル: `_xxx_partial.html`
- 機能ディレクトリ: `auth`, `profile`, `qa`, `features`
- 静的JS: `kebab-case.js`（例: `markdown-editor.js`）

## 5. 変更管理手順（標準）
1. 対象URLを`urls.py`で確認
2. 対応Viewの`template_name`と分岐条件を確認
3. 画面本体とパーシャルの影響範囲を分離
4. `rg`で旧参照・構文崩れをスキャン
5. htmx遷移（部分更新）と直接アクセス（全画面）で両方確認
6. `jj diff`で差分を確認して記録

## 6. 品質確認チェックリスト
- URLに対してテンプレート参照切れがない
- htmx遷移で`main`差し替え時にJS依存が欠落しない
- `_hyperscript`式で構文エラーがない
- SVG/属性のクォート欠落がない
- Markdownプレビューが質問投稿・回答投稿の双方で動作する
- ログイン後画面でサイドバー/メインのレイアウト崩れがない

## 7. ファイル責務一覧
- `config/settings.py` : Django設定全般（DB、AUTH、STATIC/MEDIA）
- `config/urls.py` : ルートURL統合（knowledgeapp/accounts/auth）
- `knowledgeapp/urls.py` : QA・公開ページのURL定義
- `knowledgeapp/views.py` : 質問/回答/ブックマーク/画像アップロード処理
- `accounts/urls.py` : signup/login/logout/setting/withdraw URL
- `accounts/views.py` : 認証補助、設定画面、退会処理
- `templates/layouts/public_base.html` : 公開画面の共通レイアウト
- `templates/layouts/app_base.html` : ログイン後画面の共通レイアウト（共通JS読込を含む）
- `templates/app/components/sidebar.html` : ログイン後サイドメニュー
- `templates/app/components/editor/_*.html` : MarkdownエディタUI部品
- `static/js/markdown-editor.js` : Markdownプレビュー・コード装飾・Copy処理
- `static/globals.css` : 全体スタイル

## 8. 既知リスク
- Tailwind CDN依存（本番最適化未実施）
- DBマイグレーション未適用時は一部画面が空表示となる
- 設定画面のユーザー情報更新はUI先行で、永続化処理は別途実装が必要

## 9. 管理台帳（更新対象）
- ルーティング: `config/urls.py`, `knowledgeapp/urls.py`, `accounts/urls.py`
- ビュー: `knowledgeapp/views.py`, `accounts/views.py`
- レイアウト: `templates/layouts/*.html`
- QAページ: `templates/app/pages/qa/*`
- QAパーツ: `templates/app/components/qa/*`, `templates/app/components/editor/*`
- 認証/設定: `templates/app/pages/auth/*`, `templates/app/pages/profile/*`
- 公開ページ: `templates/public/pages/*`, `templates/public/components/*`
- 共通JS/CSS: `static/js/*.js`, `static/*.css`
