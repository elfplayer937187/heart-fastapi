from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.utils.jwt_util import extract_token_from_header, verify_token
from app.schemas.common import Code, BaseResponse, error
from fastapi import Response
from rich import print as rp
PUBLIC_PATHS = {
    "/api/test",
    "/api/user/login",
    "/api/user/add",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/user/logout",
}

# 文档类路径及静态资源，无需认证
DOC_PATHS_PREFIX = ()


# 定义jwt中间件类
class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    """
    JWT 认证中间件
    对应 Java 的 JwtAuthenticationFilter + SecurityConfig 的组合

    职责：
    1. 检查请求路径是否在公开列表中，是则放行
    2. 从 header 提取 token
    3. 验证 token 有效性
    4. 将用户信息存入 request.state 供后续使用
    5. token 无效则返回 401
    """

    def _init_(self, app: ASGIApp):
        super.__init__(app)

    async def dispatch(self, request: Request, call_next: any) -> Response:
        path = request.url.path
        if path in PUBLIC_PATHS or path.startswith(DOC_PATHS_PREFIX):
            return await call_next(request)

        # 从请求头提取token
        token = extract_token_from_header(request)
        if not token:
            return JSONResponse(
                status_code=401,
                # 将pydantic模型转换为字典
                content=error(
                    code=Code.UNAUTHORIZED,
                    msg="token无效或者过期",
                ).model_dump(),
            )

        payload = verify_token(token)
        if not payload:
            return JSONResponse(
                status_code=401,
                content=error(
                    code=Code.TOKEN_INVALID,
                    msg="token无效或者过期",
                ).model_dump(),
            )

        # 将用户信息存入request.state
        rp(payload)
        request.state.user_id = payload["userId"]
        request.state.username = payload["username"]
        request.state.role_type = payload["roleType"]
        request.state.token = token

        # 调用下一个中间件
        return await call_next(request)
