from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DatabaseConfig(BaseModel):
    host: str = os.getenv("DB_HOST", "debian")
    user: str = os.getenv("DB_USER", "root")
    password: str = os.getenv("DB_PASSWORD", "778057151")
    database: str = os.getenv("DB_NAME", "fast_api")
    port: int = int(os.getenv("DB_PORT", "3306"))

    @property
    def url(self) -> str:
        """返回数据库连接 URL"""
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

class Settings(BaseModel):
    app_name: str = "RaspberryPi Sensor API"
    db: DatabaseConfig = DatabaseConfig()
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    api_prefix: str = "/api"

# 全局设置实例
settings = Settings() 