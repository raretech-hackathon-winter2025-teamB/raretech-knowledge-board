# RareTECHナレッジ掲示板 構成管理書

- 文書版数: 0.4
- 更新日: 2026-02-14
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
- `templates/layouts/error_base.html`

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
- `templates/app/components/qa/common/_search_filter_bar.html`
- `templates/app/components/qa/common/_filter_modal.html`
- `templates/app/components/qa/list/_page_header.html`

### 3.5 Error pages
- `templates/errors/400.html`
- `templates/errors/403.html`
- `templates/errors/404.html`
- `templates/errors/405.html`
- `templates/errors/429.html`
- `templates/errors/500.html`
- `templates/errors/502.html`
- `templates/errors/503.html`
- `templates/errors/_error_content.html`
- `templates/errors/partials/error_panel.html`

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
- 認証失敗時に`#auth-form-shell`のみ差し替わり、Vanta背景が維持される
- 認証成功時に`HX-Redirect`で`/home/`へ遷移する
- 404/500等の異常系でエラーページが表示される（htmx時はパネル表示）
- `_hyperscript`式で構文エラーがない
- SVG/属性のクォート欠落がない
- Markdownプレビューが質問投稿・回答投稿の双方で動作する
- ログイン後画面でサイドバー/メインのレイアウト崩れがない

## 7. ファイル責務一覧
- `config/settings.py` : Django設定全般（DB、AUTH、STATIC/MEDIA）
- `config/urls.py` : ルートURL統合（knowledgeapp/accounts/auth）
- `config/error_views.py` : 4xx/5xxエラーハンドラとhtmx向け断片応答
- `knowledgeapp/urls.py` : QA・公開ページのURL定義
- `knowledgeapp/views.py` : 質問/回答/ブックマーク/画像アップロード処理
- `accounts/urls.py` : signup/login/logout/setting/withdraw URL
- `accounts/views.py` : 認証補助（LoginViewの`HX-Redirect`対応を含む）、設定画面、退会処理
- `templates/layouts/public_base.html` : 公開画面の共通レイアウト
- `templates/layouts/app_base.html` : ログイン後画面の共通レイアウト（共通JS読込を含む）
- `templates/app/pages/auth/login.html` : ログインフォーム（`#auth-form-shell`部分更新）
- `templates/app/pages/auth/signup.html` : 新規登録フォーム（`#auth-form-shell`部分更新）
- `templates/app/components/sidebar.html` : ログイン後サイドメニュー
- `templates/app/components/editor/_*.html` : MarkdownエディタUI部品
- `templates/app/components/qa/common/_search_filter_bar.html` : 検索フォーム＋絞り込みボタン共通部品（質問一覧/自分の質問/ブックマークで再利用）
- `templates/app/components/qa/common/_filter_modal.html` : カテゴリ/ステータス絞り込みモーダル共通部品
- `templates/app/components/qa/list/_page_header.html` : 質問一覧ヘッダー部品
- `static/js/markdown-editor.js` : Markdownプレビュー・コード装飾・Copy処理
- `static/js/public-base.js` : 公開画面Vanta制御（`data-vanta-page`判定、初期化/破棄）
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
- エラー表示: `config/error_views.py`, `templates/errors/*`, `templates/layouts/error_base.html`

## 10. HTMLファイル一覧（責務説明付き）

### 10.1 レイアウト
- `templates/layouts/public_base.html` : 公開画面共通レイアウト（ヘッダー/フッター/Vanta制御の土台）。
- `templates/layouts/app_base.html` : ログイン後画面共通レイアウト（サイドバー + `main` 差し替え領域）。
- `templates/layouts/error_base.html` : エラーページ共通レイアウト。

### 10.2 公開ページ（pages）
- `templates/public/pages/home.html` : トップページ（サービス紹介、認証導線）。
- `templates/public/pages/terms.html` : 利用規約ページ。
- `templates/public/pages/privacy_policy.html` : プライバシーポリシーページ。
- `templates/public/pages/features/question_post.html` : 機能紹介（質問投稿）。
- `templates/public/pages/features/question_list.html` : 機能紹介（質問一覧/検索）。
- `templates/public/pages/features/question_guide.html` : 機能紹介（質問ガイド）。

### 10.3 公開共通部品（components）
- `templates/public/components/header.html` : 公開画面ヘッダー（ログイン/新規登録導線）。
- `templates/public/components/footer.html` : 公開画面フッター（サービス情報/リンク）。

### 10.4 ログイン後ページ（pages）
- `templates/app/pages/auth/login.html` : ログインフォーム画面（`#auth-form-shell` 部分更新対象）。
- `templates/app/pages/auth/signup.html` : 新規登録フォーム画面（規約/ポリシーモーダル含む）。
- `templates/app/pages/profile/setting.html` : マイページ設定画面（プロフィール/パスワード/退会UI）。
- `templates/app/pages/qa/question_list.html` : 質問一覧画面（検索・絞り込み・カード一覧）。
- `templates/app/pages/qa/question_form.html` : 質問投稿画面（Markdownエディタ）。
- `templates/app/pages/qa/question_detail.html` : 質問詳細画面（本文・回答一覧・返信フォーム）。
- `templates/app/pages/qa/my_questions.html` : 自分の質問一覧画面（検索・絞り込み）。
- `templates/app/pages/qa/bookmarks.html` : ブックマーク一覧画面（検索・絞り込み）。
- `templates/app/pages/qa/how_to_ask.html` : 「いい質問の仕方」ガイド画面。

### 10.5 ログイン後共通部品（components）
- `templates/app/components/sidebar.html` : ログイン後サイドバー（アクティブ状態制御）。
- `templates/app/components/message.html` : Djangoメッセージ表示部品。

### 10.6 認証パーツ（components/auth）
- `templates/app/components/auth/_branding_partial.html` : 認証画面のブランドロゴ/タイトル部。
- `templates/app/components/auth/_panel_header_partial.html` : フォームカード上部ヘッダー。
- `templates/app/components/auth/_switch_action_partial.html` : login/signup相互遷移ボタン。
- `templates/app/components/auth/_copyright_partial.html` : 認証画面フッター文言。
- `templates/app/components/auth/_vanta_sync_partial.html` : 認証画面のVanta再初期化補助。

### 10.7 法務文面パーツ（components/legal）
- `templates/app/components/legal/_terms_content_partial.html` : 利用規約本文（モーダル内表示）。
- `templates/app/components/legal/_privacy_content_partial.html` : プライバシーポリシー本文（モーダル内表示）。

### 10.8 エディタパーツ（components/editor）
- `templates/app/components/editor/_markdown_editor_partial.html` : 編集/プレビュー全体ラッパー。
- `templates/app/components/editor/_tabs_partial.html` : 編集・プレビュー切替タブ。
- `templates/app/components/editor/_toolbar_partial.html` : Markdownツールバー。
- `templates/app/components/editor/_upload_partial.html` : 画像アップロード入力/連携部。

### 10.9 QAパーツ（components/qa）
- `templates/app/components/qa/_question_list_partial.html` : 質問カード一覧描画。
- `templates/app/components/qa/_question_card_partial.html` : 単一質問カード。
- `templates/app/components/qa/_question_empty_partial.html` : 空状態表示。
- `templates/app/components/qa/_bookmark_button_partial.html` : ブックマーク切替ボタン。
- `templates/app/components/qa/_question_detail_header_partial.html` : 質問詳細ヘッダー。
- `templates/app/components/qa/_question_detail_body_partial.html` : 質問本文/メタ情報/状態表示。
- `templates/app/components/qa/_answer_list_partial.html` : 回答一覧ラッパー。
- `templates/app/components/qa/_answer_item_partial.html` : 単一回答表示。
- `templates/app/components/qa/_answer_form_partial.html` : 回答投稿フォーム。

### 10.10 QA共通化パーツ（components/qa/common, list）
- `templates/app/components/qa/common/_search_filter_bar.html` : 検索入力 + 検索ボタン + 絞り込みボタン共通部品。
- `templates/app/components/qa/common/_filter_modal.html` : カテゴリ/ステータス絞り込みモーダル共通部品。
- `templates/app/components/qa/list/_page_header.html` : 質問一覧専用ヘッダー。

### 10.11 エラーページ（errors）
- `templates/errors/400.html` : 400 Bad Request フルページ。
- `templates/errors/403.html` : 403 Forbidden フルページ。
- `templates/errors/404.html` : 404 Not Found フルページ。
- `templates/errors/405.html` : 405 Method Not Allowed フルページ。
- `templates/errors/429.html` : 429 Too Many Requests フルページ。
- `templates/errors/500.html` : 500 Internal Server Error フルページ。
- `templates/errors/502.html` : 502 Bad Gateway フルページ。
- `templates/errors/503.html` : 503 Service Unavailable フルページ。
- `templates/errors/_error_content.html` : エラー本文共通パーツ。
- `templates/errors/partials/error_panel.html` : htmx向けエラー断片表示。

## 11. アイコン管理（SVG）

### 11.1 管理方針
- インラインSVGは使用せず、`templates/app/components/icons/*.svg` を `{% include %}` で参照する。
- 色は `currentColor` ベースで制御し、呼び出し側で `text-*` クラスを付与する。
- サイズは `icon_class` 引数で指定する（例: `w-4 h-4`, `w-6 h-6`）。
- 線幅差分が必要な場合のみ引数化（例: `check.svg` の `stroke_width`）。

### 11.2 命名規約
- ファイル名は `kebab-case.svg`。
- アイコンの意味が分かる名詞で命名する（例: `bookmark.svg`, `login-square.svg`）。
- 状態差分はサフィックスで表現する（例: `bookmark.svg` / `bookmark-filled.svg`）。

### 11.3 アイコン一覧と主用途
- `templates/app/components/icons/alert-circle.svg` : 注意・ガイド見出し。
- `templates/app/components/icons/arrow-right.svg` : CTA矢印。
- `templates/app/components/icons/book-guide.svg` : ガイド機能カード。
- `templates/app/components/icons/bookmark.svg` : ブックマーク通常状態。
- `templates/app/components/icons/bookmark-filled.svg` : ブックマーク選択状態。
- `templates/app/components/icons/bulb.svg` : ナレッジ共有表現。
- `templates/app/components/icons/chat.svg` : 質問/会話系。
- `templates/app/components/icons/check.svg` : 完了・ステータスチェック。
- `templates/app/components/icons/clipboard-check.svg` : 完全例・チェック済み文脈。
- `templates/app/components/icons/close.svg` : モーダル閉じる。
- `templates/app/components/icons/code-chevrons.svg` : コード例/コード見出し。
- `templates/app/components/icons/community.svg` : コミュニティ系。
- `templates/app/components/icons/file-corner.svg` : 手順・ドキュメント見出し。
- `templates/app/components/icons/filter.svg` : 絞り込み操作。
- `templates/app/components/icons/image.svg` : 画像挿入。
- `templates/app/components/icons/link.svg` : リンク挿入。
- `templates/app/components/icons/lock.svg` : パスワード入力。
- `templates/app/components/icons/login-square.svg` : ログイン操作。
- `templates/app/components/icons/logout.svg` : ログアウト操作。
- `templates/app/components/icons/mail.svg` : メール入力。
- `templates/app/components/icons/search.svg` : 検索入力。
- `templates/app/components/icons/send.svg` : 投稿/送信操作。
- `templates/app/components/icons/settings.svg` : 設定見出し。
- `templates/app/components/icons/star.svg` : おすすめ・メリット訴求。
- `templates/app/components/icons/user.svg` : マイページ・ユーザー系。
- `templates/app/components/icons/user-circle.svg` : ユーザー入力（認証フォーム）。
- `templates/app/components/icons/user-plus.svg` : 新規登録操作。
- `templates/app/components/icons/users-group.svg` : コミュニケーション見出し。

### 11.4 呼び出し例
- 例1: `{% include "app/components/icons/search.svg" with icon_class="w-5 h-5" %}`
- 例2: `{% include "app/components/icons/check.svg" with icon_class="w-4 h-4" stroke_width="3" %}`
