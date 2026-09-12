from typing import Any, Optional


from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ConsultationSession(Base):
    """咨询会话表"""

    __tablename__ = 'consultation_session'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment='会话ID'
    )
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment='用户ID')
    session_title: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, comment='会话标题'
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), comment='开始时间'
    )
    last_emotion_analysis: Mapped[Optional[Any]] = mapped_column(
        JSON, nullable=True, comment='最后一次情绪分析结果(JSON)'
    )
    last_emotion_updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, comment='情绪分析更新时间'
    )

    def __repr__(self):
        return f'<ConsultationSession(id={self.id}, user_id={self.user_id})>'
