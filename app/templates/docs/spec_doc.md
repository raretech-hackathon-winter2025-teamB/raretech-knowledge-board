# RareTECHナレッジ掲示板 仕様書

- 文書版数: 0.2
- 更新日: 2026-02-13
- 対象: `app/`（Djangoプロジェクト）
- 前提: Django 5.2 / Python 3.10 / MySQL / htmx 1.9.12 / _hyperscript 0.9.12 / Tailwind CSS（CDN）

## 1. システム概要
RareTECHナレッジ掲示板は、エンジニア向けQ&Aを中心としたナレッジ共有アプリケーションである。  
公開ページ（未ログイン）と、ログイン後の質問管理ページで構成される。

## 2. 技術スタック
- サーバサイド: Django 5.2（Class-Based View）
- データベース: MySQL（`hackathon_db`）
- ユーザ認証: Django認証（`AUTH_USER_MODEL = accounts.User`）
- フロントエンド: Django Templates + Tailwind CSS（CDN）
- 部分更新/UI制御: htmx + _hyperscript
- Markdown処理: `marked` + `DOMPurify` + `highlight.js`
- 画像アップロード: Django `default_storage`（`MEDIA_ROOT`）

## 3. URL仕様

### 3.1 公開ページ
- `GET /` : トップページ
- `GET /login/` : ログイン
- `GET /signup/` : 新規登録
- `GET /terms/` : 利用規約
- `GET /privacy-policy/` : プライバシーポリシー
- `GET /features/question-post/` : 機能紹介（質問投稿）
- `GET /features/question-list/` : 機能紹介（質問一覧）
- `GET /features/question-guide/` : 機能紹介（質問ガイド）

### 3.2 ログイン後ページ
- `GET /home/` : 質問一覧
- `GET /question/new/` : 質問投稿画面
- `POST /question/new/` : 質問投稿実行
- `GET /question/<int:pk>/` : 質問詳細
- `POST /question/<int:pk>/answer/` : 回答投稿
- `POST /question/<int:pk>/resolve/` : 質問ステータスを解決済みに更新（投稿者のみ）
- `POST /question/<int:pk>/bookmark/` : ブックマーク切替
- `GET /my-questions/` : 自分の質問一覧
- `GET /bookmarks/` : ブックマーク一覧
- `GET /bookmark/` : 旧互換URL（`/bookmarks/`同等）
- `GET /how-to-ask/` : いい質問の仕方
- `GET /setting/` : マイページ設定
- `POST /withdraw/` : 退会処理（本人パスワード確認あり）

### 3.3 共通API/補助
- `POST /upload-image/` : Markdownエディタ画像アップロード
- `GET /logout/` : ログアウト
- `POST /logout/` : ログアウト

## 4. 主要機能仕様

### 4.1 認証
- 新規登録成功時は自動ログインし `/home/` へ遷移。
- ログアウトは通常遷移とhtmx遷移の両方をサポート。

### 4.2 質問一覧
- キーワード、カテゴリ、ステータス（解決済/未解決）で絞り込み可能。
- 一覧カードから質問詳細へ遷移。
- 各カード上でブックマーク切替可能。

### 4.3 質問投稿・回答投稿
- 共通Markdownエディタを使用。
- 画像アップロード時、返却URLをMarkdown形式で本文へ追記。
- 未ログイン時の投稿は `/login/` へ誘導。

### 4.4 質問詳細
- 質問本文・回答本文はMarkdownレンダリング表示。
- コードブロックは行番号・Copyボタン・シンタックスハイライト表示。
- 投稿者本人のみ「解決済みにする」実行可。

### 4.5 マイページ
- 表示項目: ユーザー名、メールアドレス、パスワード、退会。
- パスワード変更モーダルは以下3項目UI:
  - 現在のパスワード
  - 新しいパスワード
  - 新しいパスワード（確認）
- 退会は現在パスワード入力を必須とし、検証成功時にユーザー削除。

## 5. Markdownエディタ仕様
- 対象ファイル: `static/js/markdown-editor.js`
- 提供機能:
  - `window.MarkdownEditor.renderPreview(editorId, previewId)`
  - `window.MarkdownEditor.renderMarkdownBlocks(root)`
- イベント連携:
  - `DOMContentLoaded`
  - `htmx:afterSwap`
  - `htmx:load`
- 変換失敗時フォールバック:
  - `marked`未読込時は`<pre>`のエスケープ表示

## 6. UI構成

### 6.1 公開画面
- レイアウト: `templates/layouts/public_base.html`
- 共通部品: `templates/public/components/header.html`, `templates/public/components/footer.html`
- Vanta背景（Birds）をトップ系画面に適用。

### 6.2 ログイン後画面
- レイアウト: `templates/layouts/app_base.html`
- 左サイドバー + メインコンテンツ
- 共通部品: `templates/app/components/sidebar.html`, `templates/app/components/message.html`

## 7. 例外・障害耐性
- DB未作成・接続異常時に、一覧系は空配列返却でテンプレート描画を継続する実装あり。
- UUIDセッション不整合時の例外に対して、画面崩壊を避けるため防御的実装を一部導入。

## 8. 既知制約
- Tailwind CDN利用のため、本番ではPostCSS/CLIビルド移行が必要。
- `favicon.ico`未配置時は404ログが出る。
- 一部設定画面の保存処理（ユーザー名・メール・パスワード更新）はUI先行で、バックエンド永続化の追加実装が必要。

## 9. 今後改善候補
- Tailwindをビルド方式へ移行
- 設定画面の更新処理（POST + バリデーション + メッセージ）を正式実装
- 監査ログ（投稿/回答/退会/ブックマーク）を追加
