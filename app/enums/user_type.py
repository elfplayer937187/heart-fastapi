from enum import Enum

class UserType(Enum):
  USER=(1,"普通用户")
  ADMIN=(2,"管理员")

  #接收code和description
  def __init__(self,code:int,description:str) -> None:
    self.code = code
    self.description = description
    
  #根据code枚举获取description
  @classmethod
  def from_code(cls,code:int)->str:
    """根据code枚举获取description"""
    for member in cls:
      if member.code == code:
        return member.description
    raise ValueError(f"未知的角色代码: {code}")

  #验证code是否有效
  @classmethod
  def is_valid(cls,code:int)->bool:
    """验证code是否有效"""
    return code in [member.code for member in cls]