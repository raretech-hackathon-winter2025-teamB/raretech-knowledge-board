# RareTECHナレッジ掲示板

RareTECH生専用Q&Aプラットフォーム

## 開発環境

- Python 3.10
- Django 5.2
- MySQL 8.0
- Docker / Docker Compose

## ディレクトリ構造
```
raretech-knowledge-board/
├── app/
│   ├── config/            # プロジェクト設定
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
├── docker/
│   └── Dockerfile
├── .env
├── .env.sample
├── docker-compose.yml
├── requirements.txt
├── Makefile
└── README.md
```

## 初回セットアップ

### 1. リポジトリをクローン
```bash
git clone https://github.com/raretech-hackathon-winter2025-teamB/raretech-knowledge-board.git
cd raretech-knowledge-board
```

### 2. 環境変数ファイルを作成
```bash
cp .env.sample .env
```

### 3. SECRET_KEYを生成
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 4. `.env`を編集

生成したSECRET_KEYと、任意のパスワードを設定してください。
```bash
# .envの編集例

# ======= ✅ チームで共通（変更不要） =======
MYSQL_DATABASE=hackathon_db
MYSQL_USER=dev_user
DJANGO_TIME_ZONE=Asia/Tokyo
DJANGO_LANGUAGE_CODE=ja
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# ======= 🔧 各自で設定 =======
MYSQL_PASSWORD=devpass123              # 任意のパスワード
MYSQL_ROOT_PASSWORD=rootpass123        # 任意のパスワード
DJANGO_SECRET_KEY=ここに生成したキーを貼り付け
DJANGO_DEBUG=True
```

### 5. Djangoプロジェクトを初期化（初回のみ）

> ⚠️ この手順は初回セットアップ時のみ実行してください。
> リポジトリに `app/` が既に存在する場合はスキップしてください。
```bash
mkdir -p app
docker compose run --rm web django-admin startproject config /app
sudo chown -R $USER:$USER app/
```

### 6. コンテナを起動
```bash
docker compose up -d
```

### 7. マイグレーションを実行
```bash
make migrate
```

### 8. 動作確認

ブラウザで http://localhost:8000 にアクセスし、Djangoのロケット画面が表示されれば成功です。

## 2回目以降の起動
```bash
cd raretech-knowledge-board
docker compose up -d
```

## 管理者ユーザー作成（任意）
```bash
make createsuperuser
```

作成後、http://localhost:8000/admin でログインできます。

## よく使うコマンド

| やりたいこと | コマンド |
|-------------|---------|
| コンテナ起動 | `make up` |
| コンテナ停止 | `make down` |
| ログ確認 | `make logs` |
| コンテナに入る | `make shell` |
| マイグレーション作成 | `make makemigrations` |
| マイグレーション実行 | `make migrate` |
| 管理者作成 | `make createsuperuser` |
| 全部リセット | `make clean` |

## トラブルシューティング

### `permission denied` エラーが出る場合
```bash
sudo chown -R $USER:$USER app/
```

### DBに接続できない場合

MySQLの起動を待ってから再試行：
```bash
docker compose down
docker compose up -d
```

### 全部やり直したい場合
```bash
make clean
```

⚠️ データベースのデータも削除されます。
