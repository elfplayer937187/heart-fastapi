from datetime import datetime
from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.models.consultation_message import ConsultationMessage
from app.schemas.consultation import (
    ConsultationMessageResponse,
    message_to_response,
)

#咨询消息服务
class ConsultationMessageService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user_message(
        self, session_id: int, content: str, emotion_tag: str = None
    ) -> ConsultationMessage:
        """创建并保存用户消息"""
        message = ConsultationMessage(
            session_id,
            sender_type=1,
            message_type=1,
            content=content,
            emotion_tag=emotion_tag,
        )
        self.session.add(message)
        await self.session.flush()
        return message

    # 创建ai消息
    async def create_ai_message(
        self, session_id: int, content: str, ai_model: str = "openai"
    ) -> ConsultationMessage:
        """创建并保存ai消息"""
        message = ConsultationMessage(
            session_id,
            sender_type=2,
            message_type=1,
            content=content,
            ai_model=ai_model,
        )
        self.session.add(message)
        await self.session.flush()
        return message

    async def get_message_count_by_session_id(self, session_id: int) -> int:
        """根据会话ID获取消息数量"""
        stmt = (
            select(func.count(ConsultationMessage.session_id))
            .select_from(ConsultationMessage)
            .where(ConsultationMessage.session_id == session_id)
        )
        result = await self.session.scalar(stmt)
        return result or 0

    async def get_latest_message_by_session_id(
        self, session_id: int
    ) -> ConsultationMessage|None:
        """根据会话ID获取最新消息"""
        stmt = (
            select(ConsultationMessage)
            .select_from(ConsultationMessage)
            .where(ConsultationMessage.session_id == session_id)
            .order_by(ConsultationMessage.created_at.desc())
            .limit(1)
        )
        result = await self.session.scalar(stmt)
        return result

    async def get_all_messages_by_session_id(
        self, session_id: int
    ) -> List[ConsultationMessage]:
        """根据会话ID获取所有消息"""
        stmt = (
            select(ConsultationMessage)
            .select_from(ConsultationMessage)
            .where(ConsultationMessage.session_id == session_id)
            .order_by(ConsultationMessage.created_at.desc())
        )
        result = await self.session.scalars(stmt)
        return list[ConsultationMessage](result)
      
      