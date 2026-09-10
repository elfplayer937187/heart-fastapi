from ast import stmt
from datetime import datetime
from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.consultation_session import ConsultationSession

from app.schemas.common import Code
from app.schemas.consultation import ConsultationSessionCreate
from app.exceptions.business_exception import BusinessException


# 咨询会话业务
class ConsultationSessionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_consultation_session(
        self, user_id: int, consultation_session: ConsultationSessionCreate
    ) -> ConsultationSession:
        """
        流程：
            1. 验证用户是否存在
            2. 创建会话记录
            3. 自动生成会话标题（如果没有提供）
            4. 插入数据库并返回
        """
        # 1. 验证用户是否存在
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise BusinessException(
                data=None, code=Code.USER_NOT_EXIST, message="用户不存在"
            )

        # 2. 创建会话记录
        session_title = (
            consultation_session.session_title
            or f"会话_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        new_session=ConsultationSession(
          user_id=user_id,
          session_title=session_title,
          started_at=datetime.now(),
        )
        
        #3. 插入数据库
        self.session.add(new_session)
        await self.session.commit()
        return new_session
      
      
    async def get_session_by_id(self, session_id: int) -> ConsultationSession:
      """
      流程：
        1. 根据主键查询会话
        2. 如果会话不存在，抛出会话不存在异常
        3. 返回会话
      """
      #根据主键查询会话
      session_result=await self.session.get(ConsultationSession, session_id)
      if not session_result:
        raise BusinessException(
          data=None, code=Code.SESSION_NOT_FOUND, message="会话不存在"
        )
      return session_result

    #查询用户所有的会话列表
    async def get_user_sessions(self, user_id: int) -> List[ConsultationSession]:
      stmt=select(ConsultationSession).where(ConsultationSession.user_id==user_id).order_by(ConsultationSession.id.desc())
      result=await self.session.scalars(stmt)
      if not result:
        return []
      return result.all()