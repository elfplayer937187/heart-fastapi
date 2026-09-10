from sqlalchemy.ext.asyncio.session import AsyncSession


from app.config import settings

# 导入orm基类
from sqlalchemy.orm import DeclarativeBase

# 导入引擎
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# 拼接数据库url
# asyncmy 是 MySQL 的异步驱动，格式：mysql+asyncmy://user:pass@host:port/db
DB_URL = f"mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset=utf8mb4"

# 创建数据库引擎(异步,打印sql语句)
engine = create_async_engine(DB_URL, echo=True)

# 创建会话工厂
async_session = async_sessionmaker[AsyncSession](engine, expire_on_commit=False, class_=AsyncSession,autoflush=True)


# 定义orm基类
class Base(DeclarativeBase):
    pass


# 创建数据库依赖
async def get_db():
    async with async_session() as session:
        try:
            # 把session传递给请求上下文,并且上下文执行完后自动提交事务
            yield session
            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e
