from datetime import date, datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, SmallInteger, Date, DateTime, func
)
from sqlalchemy.orm import Mapped
from app.database import Base
from app.enums.user_type import UserType
from app.enums.user_status import UserStatus

class User(Base):
  "用户表"
  __tablename__ = "user"
  
  id:Mapped[int]=Column[int](BigInteger,primary_key=True,autoincrement=True,comment='用户id')
  username:Mapped[str]=Column[str](String(50),nullable=False,unique=True,comment='用户名')
  email:Mapped[str]=Column[str](String(100), nullable=True, comment="邮箱")   
  phone:Mapped[str]=Column[str](String(20), nullable=True, comment="手机号")
  password:Mapped[str]=Column[str](String(255), nullable=False, comment="密码")
  nickname:Mapped[str]=Column[str](String(100), nullable=True, comment="昵称")
  avatar:Mapped[str]=Column[str](String(500), nullable=True, comment="头像URL")
  gender:Mapped[int]=Column[int](SmallInteger, default=0, comment="性别 0:未知 1:男 2:女")
  birthday:Mapped[date]=Column[date](Date, nullable=True, comment="生日")
  user_type:Mapped[int]=Column[int]("user_type", SmallInteger, default=1, comment="用户类型 1:普通 2:管理员")
  status:Mapped[int]=Column[int](SmallInteger, default=1, comment="用户状态 0:禁用 1:正常")
  created_at:Mapped[datetime]=Column[datetime](DateTime,default=func.now(),comment='创建时间')
  updated_at:Mapped[datetime]=Column[datetime](DateTime,default=func.now(),onupdate=func.now(),comment='更新时间')


  @property
  def display_name(self)->str:
    return self.nickname.strip() if self.nickname.strip() and self.nickname.strip()!='' else self.username.strip()
  
  @property
  def user_type_display_name(self)->str:
    try:
      return UserType.from_code(self.user_type)
    except ValueError:
      return ''
    
  @property
  def gender_display_name(self) -> str:
      """获取性别显示名称"""
      if self.gender == 1:
          return "男"
      elif self.gender == 2:
          return "女"
      return "未知"

  def is_active(self) -> bool:
      """是否正常状态"""
      return UserStatus.NORMAL.code == self.status

  def __repr__(self):
      return f"<User(id={self.id}, username={self.username})>"