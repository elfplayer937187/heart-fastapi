from typing import Optional, List, Dict, Any, Union, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


# 定义基础响应类型
class BaseResponse(BaseModel):
    code: int = Field(default="200",description="状态码")
    msg: str = Field(default="操作成功",description="消息")
    data: Optional[T] = None


# 响应码常量(不需要enum定义)


class Code:
    """状态码常量（只用字符串常量，不需要枚举类）"""

    SUCCESS = 200
    BUSINESS_ERROR = 209
    ACCOUNT_SAME = 210
    USER_NOT_EXIST = 211
    SESSION_NOT_FOUND = 212
    INVALID_SESSION_ID = 213
    ERROR = -1
    UNAUTHORIZED = 401
    SYSTEM_ERROR = 500
    PARAM_ERROR = 400
    TOKEN_INVALID = 230
    ACCESS_UNAUTHORIZED = 301
    TOKEN_ACCESS_FORBIDDEN = 231

#定义快捷方法

#成功响应
def success(data:any=None,msg:str='操作成功')->BaseResponse:
  return BaseResponse(code=Code.SUCCESS,msg=msg,data=data)

#错误响应
def error(msg:str='操作失败',code:str=Code.ERROR ,data:any=None)->BaseResponse:
  return BaseResponse(code=code,msg=msg,data=data)


