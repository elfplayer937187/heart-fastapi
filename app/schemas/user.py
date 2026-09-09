from pydantic import BaseModel, Field, EmailStr, ValidationInfo, field_validator
import re
from typing import Optional
from datetime import datetime, date


# 用户登录请求体
class UserLoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=20, description="用户名或者邮箱")
    password: str = Field(min_length=6, max_length=20, description="密码")
    # 给请求体添加额外字段时抛出异常
    model_config = {"extra": "forbid"}


# 用户注册请求体
class UserRegisterRequest(BaseModel):

    username: str = Field(
        min_length=1, max_length=20, description="用户名", pattern=r"^\w+$"
    )
    email: str = Field(
        description="邮箱", pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    nickname: Optional[str] = Field(min_length=6, max_length=50, description="昵称")
    phone: Optional[str] = Field(description="手机号", pattern=r"^1[3-9]\d{9}$")
    password: str = Field(min_length=2, max_length=50, description="密码")
    confirm_password: str = Field(min_length=2, max_length=50, description="确认密码")
    gender: Optional[int] = Field(description="性别", ge=0, le=2)
    user_type: Optional[int] = Field(1)
    birthday: Optional[date] = None

    model_config = {"extra": "forbid"}

    # 校验密码一致性
    @field_validator("confirm_password")
    @classmethod
    def validate_password(cls, value: str, context_info: ValidationInfo) -> str:
        if "password" in context_info.data and value != context_info.data["password"]:
            raise ValueError("密码不一致")
        return value

    # 校验email合法性
    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str, context_info: ValidationInfo) -> str:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise ValueError("邮箱格式不合法")
        return value

    # 校验手机号合法性
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str, context_info: ValidationInfo) -> str:
        if not re.match(r"^1[3-9]\d{9}$", value):
            raise ValueError("手机号格式不合法")
        return value


# 定义响应体
class UserDetailResponse(BaseModel):
    """用户详情 — 对应 UserLoginResponseDTO.UserDetailResponseDTO"""

    id: int
    username: str
    email: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[int] = None
    gender_display_name: Optional[str] = None
    birthday: Optional[date] = None
    user_type: Optional[int] = None
    user_type_display_name: Optional[str] = None
    status: Optional[int] = None
    status_display_name: Optional[str] = None
    display_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # 允许从数据库模型中导入数据
    model_config = {"from_attributes": True}


class UserLoginResponse(BaseModel):
    """登录响应 — 对应 UserLoginResponseDTO.java"""

    token: str
    role_type: str
    user_info: UserDetailResponse

def build_login_response(token:str,user_info:UserDetailResponse)->UserLoginResponse:
  """构建登录响应"""
  return UserLoginResponse(token=token,role_type=user_info.role_type,user_info=user_info)