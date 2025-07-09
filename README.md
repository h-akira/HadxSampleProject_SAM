# HADX Sample Backend

hadx_sampleのVueアプリケーション用のバックエンドAPIです。AWS Lambda + API Gateway + Cognitoを使用しています。

## 技術スタック

- **Framework**: hadx（Djangoライクなサーバーレスフレームワーク）
- **Runtime**: Python 3.12
- **Deployment**: AWS SAM
- **Authentication**: AWS Cognito
- **Database**: DynamoDB（必要に応じて）

## API エンドポイント

### 認証 API

| Method | Endpoint | 説明 |
|--------|----------|------|
| POST | `/api/auth/token` | 認証コードをトークンに交換 |
| GET | `/api/auth/status` | 認証状態の確認 |
| POST | `/api/auth/logout` | ログアウト |

### その他

| Method | Endpoint | 説明 |
|--------|----------|------|
| GET | `/` | API情報の表示 |

## セットアップ

### 1. 必要な条件

- Python 3.12+
- AWS CLI設定済み
- SAM CLI インストール済み
- AWS Cognito User Pool作成済み

### 2. SSMパラメータの設定

AWS Systems Manager Parameter Storeに以下のパラメータを設定してください：

```bash
# Cognitoドメイン
aws ssm put-parameter --name "/hadx_sample/Cognito/domain" --value "https://your-domain.auth.ap-northeast-1.amazoncognito.com" --type "String"

# User Pool ID
aws ssm put-parameter --name "/hadx_sample/Cognito/user_pool_id" --value "ap-northeast-1_XXXXXXXXX" --type "String"

# Client ID
aws ssm put-parameter --name "/hadx_sample/Cognito/client_id" --value "XXXXXXXXXXXXXXXXXXXXXXXXXX" --type "String"

# Client Secret
aws ssm put-parameter --name "/hadx_sample/Cognito/client_secret" --value "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" --type "SecureString"

# フロントエンドURL
aws ssm put-parameter --name "/hadx_sample/URL/frontend" --value "http://localhost:8080" --type "String"
```

### 3. ローカル開発

```bash
# 依存関係のインストール
pip install -r requirements.txt

# hadxフレームワークのインストール
cd ../hadx
pip install -e .
cd ../hadx_sample_backend

# ローカルサーバー起動
sam local start-api --port 3000
```

### 4. デプロイ

```bash
# ビルド
sam build

# デプロイ
sam deploy --guided
```

初回デプロイ時は`--guided`オプションでパラメータを設定してください。

### 5. プロダクション設定

デプロイ後、API Gateway のURLを取得し、以下を更新してください：

1. **Vue アプリの設定** (`../hadx_sample/src/config.js`)
   ```javascript
   baseUrl: 'https://YOUR_API_GATEWAY_URL.execute-api.ap-northeast-1.amazonaws.com/prod'
   ```

2. **Cognito設定** 
   - コールバックURLにAPI Gateway URLを追加
   - ログアウトURLにVue アプリのURLを追加

## 開発時の注意点

### CORS設定

ローカル開発時は、Vue アプリ（http://localhost:8080）からのリクエストを許可するようにCORSが設定されています。

### 認証フロー

1. Vue アプリからCognitoマネージドログインページにリダイレクト
2. ログイン成功後、認証コードがコールバックURLに送信
3. Vue アプリが認証コードを `/api/auth/token` に送信
4. バックエンドでトークンに交換し、HttpOnly Cookieで返却
5. 以降のAPIリクエストは自動的にCookieが送信される

### ログ

Lambda関数のログはCloudWatch Logsで確認できます：

```bash
sam logs -n HadxSampleFunction --stack-name hadx-sample-backend --tail
```

## トラブルシューティング

### 1. Cognito設定エラー

SSMパラメータが正しく設定されているか確認してください：

```bash
aws ssm get-parameter --name "/hadx_sample/Cognito/domain"
```

### 2. CORS エラー

API GatewayのCORS設定を確認し、フロントエンドのOriginが許可されているか確認してください。

### 3. 認証エラー

- Cognitoの設定でコールバックURLが正しく設定されているか確認
- リダイレクトURIがAPIリクエストと一致しているか確認

## 今後の拡張

- [ ] ユーザー管理API
- [ ] データ管理API  
- [ ] ファイルアップロード機能
- [ ] 通知機能

## ライセンス

MIT License
