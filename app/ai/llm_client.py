from langchain_openai import ChatOpenAI
from typing import List, Any
from app.config import settings
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage,
)


class LLMClient:
    def __init__(self) -> None:
        self.mode = ChatOpenAI(
            temperature=0.7,
            model=settings.LLM_MODEL,
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            max_tokens=4096,
            timeout=30,
            streaming=True,
        )

    # 流式对话
    async def stream_chat(
        self,
        user_message: str,
        system_message: str,
        history: List[tuple[str, Any]] | None = None,
    ):
        """流式对话"""
        messages = [SystemMessage(content=system_message)]
        # 将历史加入messages
        if history:
            for user_msg, ai_msg in history:
                messages.append(HumanMessage(content=user_msg))
                messages.append(AIMessage(content=ai_msg))

        messages.append(HumanMessage(content=user_message))

        # 流式对话
        async for chunk in self.mode.astream(messages):
            chunk = chunk.content
            if chunk:
                yield chunk

    # 非流式对话
    async def chat(
        self,
        user_message: str,
        system_prompt: str,
        history: list[tuple[str, str]] | None = None,
    ) -> str:
        """
        非流式对话（一次性返回）

        用于不需要流式的场景，比如情绪分析、总结等。
        """
        # 复用流式逻辑，但把所有块拼起来
        full_response = ""
        async for chunk in self.stream_chat(user_message, system_prompt, history):
            full_response += chunk
        return full_response
