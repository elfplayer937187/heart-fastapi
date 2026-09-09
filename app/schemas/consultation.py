from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ==================== 请求体 ====================

class ConsultationSessionCreate(BaseModel):
    """开始会话请求体 — 对应 ConsultationSessionCreateDTO.java"""
    session_title: Optional[str] = Field(None, max_length=200, description="会话标题")
    initial_message: str = Field(..., min_length=1, max_length=2000, description="初始消息")

    model_config = {"extra": "forbid"}


class ConsultationStream(BaseModel):
    """流式对话请求体 — 对应 ConsultationStreamDTO.java"""
    session_id: str = Field(..., description="会话ID（格式: session_xxx）")
    user_message: str = Field(..., min_length=1, max_length=2000, description="用户消息")

    model_config = {"extra": "forbid"}


# ==================== 响应体 ====================

class StreamChatSession(BaseModel):
    """会话启动响应 — 对应 StructOutPut.StreamChatSession"""
    session_id: str
    user_hash: int
    initial_message: str
    start_time: int
    expiry_time: int
    message_count: int
    status: str


class ConsultationMessageResponse(BaseModel):
    """消息响应 — 对应 ConsultationMessageResponseDTO.java"""
    id: int
    session_id: int
    sender_type: int
    sender_type_desc: Optional[str] = None
    message_type: int
    message_type_desc: Optional[str] = None
    content: str
    emotion_tag: Optional[str] = None
    ai_model: Optional[str] = None
    created_at: Optional[datetime] = None
    content_length: Optional[int] = None

    model_config = {"from_attributes": True}


# ==================== 转换函数 ====================

def message_to_response(message) -> ConsultationMessageResponse:
    """
    将 ConsultationMessage 实体转为响应 DTO
    对应 Java 的 convertToResponseDTO() 方法
    """
    return ConsultationMessageResponse(
        id=message.id,
        session_id=message.session_id,
        sender_type=message.sender_type,
        sender_type_desc=message.sender_type_desc,
        message_type=message.message_type,
        message_type_desc=message.message_type_desc,
        content=message.content,
        emotion_tag=message.emotion_tag,
        ai_model=message.ai_model,
        created_at=message.created_at,
        content_length=message.content_length,
    )