from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

# 导入数据库依赖
from app.database import get_db

# 导入用户服务
from app.exceptions.business_exception import BusinessException
from app.schemas.common import Code, success
from app.services.user_service import UserService

# 导入schemas
from app.schemas.user import (
    UserLoginRequest,
    UserRegisterRequest,
    UserLoginResponse,
    UserDetailResponse,
)
from app.utils.jwt_util import get_current_user_id

router = APIRouter(prefix="/api/user",tags=["用户管理"])


# 依赖注入工厂函数
async def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)


# 登录接口
@router.post("/login")
async def login(
    request: UserLoginRequest, user_service: UserService = Depends(get_user_service)
) -> UserLoginResponse:
    """
    Pydantic 模型默认的 `.model_dump()` 返回的是 Python 对象字典。但 `datetime`、`date` 这些类型不能直接 JSON 序列化，需要转换成字符串。`mode="json"`
    """
    result = await user_service.login(request)
    return success(data=result.model_dump(mode="json"))


@router.post("/add")
async def add(
    request: UserRegisterRequest, user_service: UserService = Depends(get_user_service)
) -> UserDetailResponse:
    result = await user_service.register(request)
    return success(data=result.model_dump(mode="json"))


@router.get("/current")
async def get_current_user(
    request: Request, user_service: UserService = Depends(get_user_service)
) -> UserDetailResponse:
    user_id = request.state.user_id or None
    if not user_id:
        raise BusinessException(code=Code.UNAUTHORIZED, message="请先登录")
    result = await user_service.get_user_by_id(user_id)
    return success(data=result.model_dump(mode="json"))


@router.post("logout")
async def logout():
    return success(msg="退出成功")
