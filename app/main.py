from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.exceptions.business_exception import BusinessException
from app.exceptions.handler import (
    business_exception_handler,
    validation_exception_handler,
    unauthorized_exception_handler,
    general_exception_handler,
)
from starlette.authentication import AuthenticationError

from app.middleware.jwt_middleware import JWTAuthenticationMiddleware
from app.api import user
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    yield 之前：应用启动时执行（初始化数据库连接、加载模型等）
    yield 之后：应用关闭时执行（清理资源）
    """
    print("应用启动中...")
    yield
    print("应用关闭中...")


app = FastAPI(
    title="心理健康助手后端服务",
    description="基于 FastAPI + LangChain 的心理健康助手后端服务",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AuthenticationError, unauthorized_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
#添加JWT认证中间件
app.add_middleware(JWTAuthenticationMiddleware)

#添加用户路由
app.include_router(user.router)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
