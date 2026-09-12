import asyncio
from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PSYCHOLOGICAL_SUPPORT_SYSTEM_PROMPT
async def test_llm():
    llm_client=LLMClient()

    async for chunk in llm_client.stream_chat(user_message="你是谁",system_message=PSYCHOLOGICAL_SUPPORT_SYSTEM_PROMPT,history=[]):
        print(chunk,end="",flush=True)
    
asyncio.run(test_llm())