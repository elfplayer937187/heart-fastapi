from datetime import datetime
from sqlalchemy import Column, BigInteger, SmallInteger, String, Text, DateTime, func
from app.database import Base


class ConsultationMessage(Base):
    """咨询消息表"""

    __tablename__ = "consultation_message"

    id = Column[int](BigInteger, primary_key=True, autoincrement=True, comment="消息ID")
    session_id = Column[int](BigInteger, nullable=False, comment="会话ID")
    sender_type = Column[int](SmallInteger, nullable=False, comment="发送者类型 1:用户 2:AI")
    message_type = Column[int](SmallInteger, default=1, comment="消息类型 1:文本")
    content = Column[str](Text, nullable=False, comment="消息内容")
    emotion_tag = Column[str](String(50), nullable=True, comment="情绪标签")
    ai_model = Column[str](String(50), nullable=True, comment="使用的AI模型")
    created_at = Column[datetime](DateTime, server_default=func.now(), comment="创建时间")

    @property
    def sender_type_desc(self) -> str:
        """发送者类型描述，对应 Java 的 getSenderTypeDesc()"""
        if self.sender_type == 1:
            return "用户"
        elif self.sender_type == 2:
            return "AI助手"
        return "未知"

    @property
    def message_type_desc(self) -> str:
        """消息类型描述"""
        if self.message_type == 1:
            return "文本"
        return "未知"

    @property
    def content_length(self) -> int:
        """消息长度"""
        return len(self.content) if self.content else 0

    def __repr__(self):
        return f"<ConsultationMessage(id={self.id}, sender_type={self.sender_type})>"
