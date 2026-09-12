from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.common import Code
from app.services.consultation_session_service import ConsultationSessionService
from app.services.consultation_message_service import ConsultationMessageService
from app.schemas.consultation import (
    ConsultationSessionCreate,
    ConsultationStream,
    StreamChatSession,
    message_to_response,
)
from app.ai.llm_client import LLMClient
from app.ai.chat_memory import ChatMemory
from app.ai.prompt_manager import PSYCHOLOGICAL_SUPPORT_SYSTEM_PROMPT
from app.exceptions.business_exception import BusinessException
import json


class ChatService:
    """
    整合：
    - ConsultationSessionService（会话管理）
    - ConsultationMessageService（消息管理）
    - LLMClient（AI 对话）
    - ConversationMemory（对话记忆）
    """

    def __init__(
        self,
        session: AsyncSession,
        llm_client: LLMClient = None,
        chat_memory: ChatMemory = None,
    ) -> None:
        self.session_service = ConsultationSessionService(session)
        self.message_service = ConsultationMessageService(session)
        self.llm_client = llm_client or LLMClient()
        self.chat_memory = chat_memory or ChatMemory()

    # 开始咨询对话
    async def start_conversation(
        self, user_id: int, create_dto: ConsultationSessionCreate
    ):
        """
        开始咨询会话

        流程：
        1. 创建数据库会话记录
        2. 保存用户的初始消息
        3. 返回会话信息
        """

        # 创建会话
        consultation_session = await self.session_service.create_consultation_session(
            user_id, create_dto
        )

        # 保存用户的初始消息
        await self.message_service.create_user_message(
            consultation_session.id, create_dto.initial_message
        )

        # 构建响应
        session_id = f"session_{consultation_session.id}"
        now_ms = int(consultation_session.started_at.timestamp() * 1000)
        expiry_time = now_ms + 86400000  # 24小时后过期

        return StreamChatSession(
            session_id=session_id,
            expiry_time=expiry_time,
            user_hash=user_id,
            initial_message=create_dto.initial_message,
            start_time=now_ms,
            message_count=1,
            status="active",
        ).model_dump(mode="json")

    # 流式对话
    async def stream_conversation(
        self,stream_dto: ConsultationStream
    ) -> AsyncIterator[str]:
        """

        参数：
        - user_id: 当前登录用户 ID
        - stream_dto: { session_id, user_message }

        返回：
        - AsyncIterator[str]：SSE 格式的事件字符串
        """
        db_session_id = self._extract_session_id(stream_dto.session_id)
        if not db_session_id:
            raise BusinessException(code=Code.INVALID_SESSION_ID, msg="无效的会话ID")

        # 判断是不是初始消息
        #   如果 count==1 且 lastMessage.senderType==1 且内容相同 → 初始消息
        message_count = await self.message_service.get_message_count_by_session_id(
            db_session_id
        )
        is_initial_message = False
        if message_count == 1:
            last_message = await self.message_service.get_latest_message_by_session_id(
                db_session_id
            )
            if (
                last_message
                and last_message.sender_type == 1
                and last_message.content == stream_dto.user_message
            ):
                is_initial_message = True

        # 不是初始消息则保存消息
        if not is_initial_message:
            await self.message_service.create_user_message(
                db_session_id, stream_dto.user_message, None
            )

        # 构建对话记忆的 conversation_id
        conversation_id = f"conversation_{stream_dto.session_id}"

        # 同步用户消息到对话记忆
        self.chat_memory.add_user_message(conversation_id, stream_dto.user_message)

        # 流式对话
        result_message = ""
        try:
            # 开启流式
            async for chunk in self.llm_client.stream_chat(
                stream_dto.user_message,
                system_message=PSYCHOLOGICAL_SUPPORT_SYSTEM_PROMPT,
                history=self.chat_memory.get_history(conversation_id),
            ):
                result_message += chunk
                # 构建sse格式
                sse_data = {
                    "code": "200",
                    "data": {"content": chunk, "type": "normal"},
                    "msg": "操作成功",
                }
                yield f"event:message\ndata:{json.dumps(sse_data,ensure_ascii=False)}\n\n"

            # 回复完成保存记忆
            if result_message:
                await self.message_service.create_ai_message(
                    db_session_id, result_message
                )
                self.chat_memory.add_ai_message(
                    conversation_id, stream_dto.user_message, result_message
                )
            # 结束发送done事件
            yield f"event:done\ndata:{{}}\n\n"
        except Exception as e:
            # 异常发送错误事件
            error_sse_data = {"code": "-1", "data": None, "msg": f"ai对话异常,{str(e)}"}
            yield f"event:error\ndata:{json.dumps(error_sse_data,ensure_ascii=False)}\n\n"
            raise

    @staticmethod
    def _extract_session_id(session_id: str) -> int | None:
        """提取会话ID"""
        if session_id.startswith("session_"):
            try:
                return int(session_id[len("session_") :])
            except ValueError:
                return None
        return None
