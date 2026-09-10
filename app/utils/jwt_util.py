from typing import Optional
import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings
from jwt import ExpiredSignatureError,InvalidTokenError
from fastapi import Request
# 签发者
ISSUER = "mental-health-assistant"

# 生成JWT令牌
def generate_token(user_id: int, username: str, role_type: int) -> str:
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(milliseconds=settings.JWT_EXPIRATION)

    payload = {
        "userId": user_id,
        "username": username,
        "roleType": role_type,
        "iss": ISSUER,
        "iat": now,
        "exp": expiration,
    }
    
    token=jwt.encode(payload,settings.JWT_SECRET,algorithm="HS256")
    return token
  

#解密JWT令牌
def decode_token(token:str)->dict:
  "解密JWT令牌"
  return jwt.decode(token,settings.JWT_SECRET,algorithms=["HS256"])

# 验证JWT令牌
def verify_token(token:str)->Optional[dict]:
  "验证JWT令牌"
  try:
    payload=jwt.decode(token,settings.JWT_SECRET,algorithms=["HS256"],options={"verify_exp":True})
    #查看签发者是否为ISSUER
    if payload["iss"]!=ISSUER:
      raise InvalidTokenError("Invalid token issuer")
    return payload
  except ExpiredSignatureError:
    raise InvalidTokenError("Token expired")
  except InvalidTokenError:
    raise InvalidTokenError("Invalid token")
  
  
#从请求体提取JWT令牌
def extract_token_from_header(request:Request)->Optional[str]:
  "获取请求头中的JWT令牌"
  token=request.headers.get('token')
  return token if token else None

#获取当前用户id
def get_current_user_id(request:Request)->Optional[int]:
  "获取当前用户id"
  token=extract_token_from_header(request)
  if not token:
    return None
  try:
    payload=verify_token(token)
    return payload["userId"]
  except InvalidTokenError:
    return None
  