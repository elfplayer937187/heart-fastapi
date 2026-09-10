class BusinessException(Exception):
  def __init__(self, data:any,code:int,message:str) -> None:
    self.data=data
    self.code=code
    self.message=message
    #使用super调用父类Exception的__init__方法,将错误信息传递给父类处理
    
    super().__init__(self.message)