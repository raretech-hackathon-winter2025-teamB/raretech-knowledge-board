# S3メディア保存 設定手順書

- 文書版数: 1.0
- 更新日: 2026-02-15
- 対象: RareTECHナレッジ掲示板（Django 5.2）
- 目的: 画像アップロード先をアプリサーバローカルから AWS S3 へ切替する

## 1. 前提

- コード側のS3対応は反映済み（`USE_S3` フラグで切替）。
- 依存は `django-storages`, `boto3` を使用。
- 画像アップロードは `default_storage` 経由で実装されている。

## 2. AWS側の準備

### 2.1 S3バケット作成

- バケット名を作成（例: `raretech-knowledge-board-media`）。
- リージョンは `AWS_S3_REGION_NAME` と一致させる。
- オブジェクト保存先プレフィックスは `uploads/` を使用する。

### 2.2 CORS設定

S3バケット `Permissions > CORS` に以下を設定。

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedOrigins": ["http://localhost:8000"],
    "ExposeHeaders": ["ETag"],
    "MaxAgeSeconds": 3000
  }
]
```

### 2.3 IAMポリシー（最小権限）

`<BUCKET_NAME>` を実際のバケット名に置換。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListBucketForUploadsPrefix",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::<BUCKET_NAME>",
      "Condition": {
        "StringLike": {
          "s3:prefix": ["uploads/*"]
        }
      }
    },
    {
      "Sid": "ObjectAccessForUploads",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::<BUCKET_NAME>/uploads/*"
    }
  ]
}
```

## 3. アプリ側の設定

プロジェクトルートの `.env` に以下を追加または更新。

```env
USE_S3=True
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME=YOUR_BUCKET_NAME
AWS_S3_REGION_NAME=ap-northeast-1
AWS_MEDIA_LOCATION=uploads
AWS_S3_CUSTOM_DOMAIN=
```

備考:
- CloudFrontを使う場合のみ `AWS_S3_CUSTOM_DOMAIN` を設定。
- ローカル保存へ戻す場合は `USE_S3=False`。

## 4. 反映手順

```bash
docker compose build web
docker compose up -d
```

## 5. 動作確認

1. `/question/new/` を開く
2. 画像を添付してアップロードする
3. `POST /upload-image/` レスポンスの `data-url` が S3 URL であることを確認する
4. 挿入された画像URLをブラウザで開き、画像表示できることを確認する

## 6. 障害切り分け

- `NoCredentialsError`
  - `.env` の `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` を確認
- `AccessDenied`
  - IAMポリシー、バケットポリシー、プレフィックス権限を確認
- URLは返るが画像表示不可
  - CORS、公開設定、`AWS_S3_CUSTOM_DOMAIN` の整合を確認
- ローカル保存される
  - `USE_S3=True` 反映有無、コンテナ再起動有無を確認

## 7. ロールバック

1. `.env` を `USE_S3=False` に変更
2. 再起動
   - `docker compose up -d --build`
3. ローカル `MEDIA_ROOT` 保存へ復帰したことを確認
