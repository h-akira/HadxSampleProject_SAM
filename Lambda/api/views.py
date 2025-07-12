from hadx.shortcuts import json_response
import json
import logging

logger = logging.getLogger(__name__)

def token_exchange(master):
    """
    認証コードをトークンに交換するエンドポイント
    POST /api/auth/token
    """
    body = json.loads(master.event.get('body', '{}'))
    code = body.get('code')
    if code:
        flag = master.settings.COGNITO.set_auth_by_code(master, code)
        if flag:
            logger.info(f"username: {master.request.username}")
            return json_response(master, {"message": "success"})
        else:
            return json_response(master, {"error": "failed to exchange code to token"}, code=400)
    else:
        return json_response(master, {"error": "code is not found, probably expired"}, code=400)

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

def sample(master):
    """
    サンプルAPIエンドポイント
    GET /api/sample
    """
    return json_response(master, {"message": "サンプル文字列"}) 