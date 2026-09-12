from ast import Dict
from typing import List, Optional


class ChatMemory:
    def __init__(self, max_history: int = 30):
        self.max_history = max_history
        self._store: Dict[str, List[tuple[str, str]]] = {}

    def add_user_message(self, conversation_id: str, message: str):
        """
        添加用户消息到记忆
        如果该对话还不存在，初始化为空列表。
        """
        if conversation_id not in self._store:
            self._store[conversation_id] = []
            pass

    def add_ai_message(self, conversation_id: str, user_message: str, ai_message: str):
        """
        添加 AI 回复到记忆
        将配对的 (用户消息, AI回复) 存入历史
        """
        if conversation_id not in self._store:
            self._store[conversation_id] = []

        # 追加记忆
        self._store[conversation_id].append((user_message, ai_message))

        # 限制记忆长度
        if len(self._store[conversation_id]) > self.max_history:
            self._store[conversation_id] = self._store[conversation_id][
                -self.max_history :
            ]

    def get_history(self, conversation_id: str) -> List[tuple[str, str]]:
        """
        获取对话历史
        返回列表，包含所有 (用户消息, AI回复) 对
        """
        if conversation_id not in self._store:
            return []
        return self._store[conversation_id]

    def clear(self, conversation_id: str):
        """
        清除对话记忆

        """
        if conversation_id in self._store:
            del self._store[conversation_id]


# 全局单例
memory = ChatMemory()
