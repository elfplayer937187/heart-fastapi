from email import message
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.exceptions.business_exception import BusinessException
from app.schemas.common import Code, BaseResponse, error
from starlette.authentication import AuthenticationError

#业务异常处理器（自定义异常）
async def business_exception_handler(
    request: Request, exc: BusinessException
) -> JSONResponse:
    """
    处理业务异常（BusinessException）
    """
    return JSONResponse(
        status_code=Code.BUSINESS_ERROR,
        content=error(
            code=Code.BUSINESS_ERROR, msg=exc.message, data=exc.data
        ).model_dump(),
    )


# 参数校验异常（FastAPI默认异常） 
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    处理参数校验异常
    对应 Java @ExceptionHandler(MethodArgumentNotValidException.class)

    FastAPI 默认的校验错误是返回 422 + detail 数组
    这里转换成和 Java 一致的格式：code + msg + data
    """
    errors=exc.errors()
    message=[]
    
    for error in errors:
      #获取错误字段
      field='->'.join([str(e) for e in error.get('loc')])

      #获取错误消息
      msg=error.get('msg') or '参数校验失败'
      
      message.append(f"{field}:{msg}")
      
    str_message=';'.join(message) if message else "参数校验失败"
    
    return JSONResponse(
      status_code=Code.VALIDATION_ERROR,
      content=error(
        code=Code.VALIDATION_ERROR,
        msg=str_message,
      ).model_dump(),
    )

#未认证异常处理器
async def unauthorized_exception_handler(request: Request, exc: AuthenticationError) -> JSONResponse:
    """
    处理未认证异常
    """
    return JSONResponse(
        status_code=401,
        content=error(code=Code.UNAUTHORIZED, msg="暂未登录或token已经过期").model_dump(),
    )

#兜底异常处理器
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    兜底异常处理器 —— 处理所有未捕获的异常
    """
    # 这里可以加日志记录
    print(f"[ERROR] 未捕获异常: {exc}")

    return JSONResponse(
        status_code=500,
        content=error(code=Code.SYSTEM_ERROR, msg="系统内部错误").model_dump(),
    )
