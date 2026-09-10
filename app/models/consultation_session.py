from typing import Any


from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, JSON, func
from app.database import Base


class ConsultationSession(Base):
    """咨询会话表"""

    __tablename__ = "consultation_session"

    id = Column[int](BigInteger, primary_key=True, autoincrement=True, comment="会话ID")
    user_id = Column[int](BigInteger, nullable=False, comment="用户ID")
    session_title = Column[str](String(200), nullable=True, comment="会话标题")
    started_at = Column[datetime](DateTime, server_default=func.now(), comment="开始时间")
    last_emotion_analysis = Column[Any](
        JSON, nullable=True, comment="最后一次情绪分析结果(JSON)"
    )
    last_emotion_updated_at = Column[datetime](
        DateTime, nullable=True, comment="情绪分析更新时间"
    )

    def __repr__(self):
        return f"<ConsultationSession(id={self.id}, user_id={self.user_id})>"
