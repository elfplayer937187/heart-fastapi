from enum import Enum


class UserStatus(Enum):
    "用户状态 0:禁用 1:正常"
    DISABLED=(0,'禁用')
    NORMAL=(1,'正常')

    def __init__(self, code: int, description: str) -> None:
        self.code = code
        self.description = description

    #通过code找出description
    @classmethod
    def from_code(cls,code):
      for member in cls:
        if member.code==code:
          return member.description
      raise ValueError(f"未知的状态代码 {code}")