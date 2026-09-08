from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DB_HOST:str = "localhost"
  DB_PORT:int = 3306
  DB_USER:str = "root"
  DB_PASSWORD:str = "123456"
  DB_NAME:str = "mental_health_assistant"
  JWT_SECRET:str = "elfplayer93718!@#$%^&*()_+SecureKeyHere"
  JWT_EXPIRATION:int = 86400000
  JWT_REFRESH_EXPIRATION:int = 604800000
  LLM_API_KEY:str = "sk-agutsdxqapeoyslqubcrwqkxnqyorinrazzabcvczclmcwex"
  LLM_BASE_URL:str = "https://api.siliconflow.cn"
  LLM_MODEL:str = "deepseek-ai/DeepSeek-V3"
  
  model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
  
#全局单例
settings = Settings()