from typing import Optional
from fastapi import APIRouter, Depends, Request, Security, Header
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

# 导入数据库依赖
from app.database import get_db

# 导入用户服务
from app.exceptions.business_exception import BusinessException
from app.schemas.common import Code, BaseResponse, success
from app.services.user_service import UserService

# 导入schemas
from app.schemas.user import (
    UserLoginRequest,
    UserRegisterRequest,
)
from app.utils.jwt_util import get_current_user_id

router = APIRouter(prefix="/api/user",tags=["用户管理"])

# token 认证方案（对应中间件读取的 'token' 请求头）
token_scheme = APIKeyHeader(name="token", auto_error=False, description="登录后返回的 token")


# 依赖注入工厂函数
async def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)


# 登录接口
@router.post("/login",description="登录",summary="登录")
async def login(
    request: UserLoginRequest, user_service: UserService = Depends(get_user_service)
) -> BaseResponse:
    result = await user_service.login(request)
    return success(data=result.model_dump(mode="json"))


@router.post("/add",description="注册",summary="注册用户")
async def add(
    request: UserRegisterRequest, user_service: UserService = Depends(get_user_service)
) -> BaseResponse:
    result = await user_service.register(request)
    return success(data=result.model_dump(mode="json"))


@router.get("/current",description="获取当前用户",summary="获取当前用户信息")
async def get_current_user(
    request: Request,
    credentials: str = Security(token_scheme),
    user_service: UserService = Depends(get_user_service),
) -> BaseResponse:
    user_id = request.state.user_id or None
    if not user_id:
        raise BusinessException(code=Code.UNAUTHORIZED, message="请先登录")
    result = await user_service.get_user_by_id(user_id)
    return success(data=result.model_dump(mode="json"))


@router.post("/logout",description="退出",summary="退出登录")
async def logout():
    return success(msg="退出成功")
