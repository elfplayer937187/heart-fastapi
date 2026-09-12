import json
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.exceptions.business_exception import BusinessException
from app.services.chat_service import ChatService
from app.schemas.consultation import ConsultationSessionCreate, ConsultationStream
from app.schemas.common import success, Code, error

router = APIRouter(prefix="/api/psychological-chat", tags=["心理咨询"])


# 获取chatservice实例
async def get_chat_service(session: AsyncSession = Depends(get_db)) -> ChatService:
    return ChatService(session)


# 开始对话接口
@router.post("/session/start")
async def start_conversation(
    request: Request,
    create_dto: ConsultationSessionCreate,
    chat_service: ChatService = Depends(get_chat_service),
):
    user_id = request.state.user_id
    if user_id is None:
        raise BusinessException(code=Code.UNAUTHORIZED, message="请先登录")

    result = await chat_service.start_conversation(user_id, create_dto)
    return success(data=result)


@router.post("/session/stream")
async def stream_conversation(
    request: Request,
    stream_dto: ConsultationStream,
    chat_service: ChatService = Depends(get_chat_service),
):
    user_id = request.state.user_id
    if user_id is None:
        # 返回一个错误的sse
        async def error_sse():
            error_sse_data = {"code": "-1", "data": None, "msg": "请先登录"}

            yield f"event:error\ndata:{json.dumps(error_sse_data,ensure_ascii=False)}\n\n"

        return StreamingResponse(error_sse(), media_type="text/event-stream")

    return StreamingResponse(
        chat_service.stream_conversation(stream_dto),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
