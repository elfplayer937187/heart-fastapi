from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.enums.user_status import UserStatus
from app.enums.user_type import UserType
from app.exceptions.business_exception import BusinessException
from app.schemas.user import (
    UserLoginRequest,
    UserRegisterRequest,
    UserLoginResponse,
    UserDetailResponse,
    build_login_response,
)
from app.models.user import User
from app.utils.jwt_util import generate_token
from app.utils.password_util import hash_password, verify_password
from app.schemas.common import Code
from rich import print as rp

class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # 登录
    async def login(self, request: UserLoginRequest) -> UserLoginResponse:
        """
        流程：
          1. 根据用户名或邮箱查用户
          2. 校验密码
          3. 检查用户状态
          4. 生成 JWT token
          5. 返回登录响应
        """
        # 1. 根据用户名或邮箱查用户
        query = select(User).where(
            User.username == request.username
        )
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise BusinessException(code=Code.USER_NOT_FOUND, message="用户名或邮箱不存在")

        if not user.is_active():
            raise BusinessException(code=Code.PARAM_ERROR, message="用户状态异常")

        if not verify_password(request.password, user.password):
            raise BusinessException(code=Code.INVALID_PASSWORD, message="密码错误")

        # 生成jwt token
        token = generate_token(user.id, user.username, user.user_type)
        rp(user)
        # 构建响应
        response = build_login_response(token, UserDetailResponse.model_validate(user))
        return response
    
    # 注册
    async def register(self, request: UserRegisterRequest):
        """
        流程：
        1. 校验密码一致性（Pydantic 已经做了）
        2. 检查用户名是否已存在
        3. 检查邮箱是否已存在
        4. 验证用户类型是否有效
        5. 加密密码
        6. 创建用户并插入数据库
        7. 返回用户详情
        """
        # 1. 校验密码一致性（Pydantic 已经做了）
        if request.password != request.confirm_password:
            raise BusinessException(data=None,code=Code.PARAM_ERROR,message='密码不一致')

        # 2. 检查用户名是否已存在
        query=select(User).where(User.username== request.username)
        result=await self.session.execute(query)
        users=result.scalars().all()
        
        if len(users)>0:
            rp(111111)
            raise BusinessException(data=None,code=Code.ACCOUNT_SAME,message='用户名已存在')
        
        # 3. 检查邮箱是否已存在
        query=select(User).where(User.email== request.email)
        result=await self.session.execute(query)
        users=result.scalars().all()
        
        if len(users)>0:
            raise BusinessException(data=None,code=Code.ACCOUNT_SAME,message='邮箱已存在')
        
        # 4. 验证用户类型是否有效
        if not UserType.is_valid(request.user_type):
            raise BusinessException(data=None,code=Code.PARAM_ERROR,message='用户类型无效')
        
        # 5. 加密密码   
        Hash_password=hash_password(request.password)

        # 6. 创建用户并插入数据库
        user=User(
            username=request.username,
            email=request.email,
            nickname=request.nickname,
            phone=request.phone,
            password=Hash_password,
            user_type=request.user_type,
            status=UserStatus.NORMAL.code,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.session.add(user)
        await self.session.flush()

        # 7. 返回用户详情
        return UserDetailResponse.model_validate(user)

    async def get_user_by_id(self, user_id: int) -> UserDetailResponse:
        """
        流程：
        1. 根据用户ID查询用户
        2. 返回用户详情
        """
        query=select(User).where(User.id==user_id)
        result=await self.session.execute(query)
        user=result.scalar_one_or_none()
        
        if not user:
            raise BusinessException(code=Code.USER_NOT_FOUND,message='用户不存在')
        
        return UserDetailResponse.model_validate(user)
        