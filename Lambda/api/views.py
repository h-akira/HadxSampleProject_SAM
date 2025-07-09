from hadx.shortcuts import json_response
import json
import logging

logger = logging.getLogger(__name__)

def token_exchange(master):
    """
    認証コードをトークンに交換するエンドポイント
    POST /api/auth/token
    """
    try:
        # リクエストボディからコードを取得
        body = json.loads(master.event.get('body', '{}'))
        code = body.get('code')
        redirect_uri = body.get('redirect_uri')
        
        if not code:
            return json_response(master, {"error": "認証コードが必要です"}, code=400)
        
        if not redirect_uri:
            return json_response(master, {"error": "リダイレクトURIが必要です"}, code=400)
        
        # 認証コードをトークンに交換
        token_response = master.settings.COGNITO._authCode2token(code, redirect_uri)
        
        if not token_response or "id_token" not in token_response:
            return json_response(master, {"error": "トークン交換に失敗しました"}, code=400)
        
        # トークンをリクエストに設定
        master.request.set_token(
            access_token=token_response['access_token'],
            id_token=token_response['id_token'],
            refresh_token=token_response['refresh_token']
        )
        master.request.set_cookie = True
        
        # IDトークンをデコードしてユーザー情報を取得
        decode_token = master.settings.COGNITO._get_decode_token(token_response['id_token'])
        
        user_info = {
            'sub': decode_token.get('sub'),
            'email': decode_token.get('email'),
            'email_verified': decode_token.get('email_verified'),
            'cognito:username': decode_token.get('cognito:username')
        }
        
        response_data = {
            'user': user_info
        }
        
        return json_response(master, response_data)
        
    except json.JSONDecodeError:
        return json_response(master, {"error": "無効なJSONです"}, code=400)
    except Exception as e:
        logger.exception(f"Token exchange error: {e}")
        return json_response(master, {"error": "内部エラーが発生しました"}, code=500)

def auth_status(master):
    """
    認証状態を確認するエンドポイント
    GET /api/auth/status
    """
    try:
        if master.request.auth:
            # 認証済みの場合
            user_info = {
                'sub': master.request.decode_token.get('sub'),
                'email': master.request.decode_token.get('email'),
                'email_verified': master.request.decode_token.get('email_verified'),
                'cognito:username': master.request.decode_token.get('cognito:username')
            }
            
            response_data = {
                'authenticated': True,
                'user': user_info
            }
        else:
            # 未認証の場合
            response_data = {
                'authenticated': False,
                'user': None
            }
        
        return json_response(master, response_data)
        
    except Exception as e:
        logger.exception(f"Auth status error: {e}")
        return json_response(master, {"error": "内部エラーが発生しました"}, code=500)

def logout(master):
    """
    ログアウトエンドポイント
    POST /api/auth/logout
    """
    try:
        if master.request.auth:
            # Cognitoからサインアウト
            master.settings.COGNITO.sign_out(master)
        
        response_data = {
            'message': 'ログアウトしました'
        }
        
        return json_response(master, response_data)
        
    except Exception as e:
        logger.exception(f"Logout error: {e}")
        return json_response(master, {"error": "内部エラーが発生しました"}, code=500) 