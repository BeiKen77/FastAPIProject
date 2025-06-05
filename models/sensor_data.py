from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger, Text
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from models.database import Base

# SQLAlchemy ORM模型
class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    sensor_type = Column(String(50), nullable=False, index=True)
    sensor_value = Column(Float(precision=10, asdecimal=True), nullable=False)
    unit = Column(String(20), nullable=True)
    device_id = Column(String(50), nullable=False, index=True)
    location = Column(String(100), nullable=True)
    timestamp = Column(DateTime, default=func.now(), index=True)
    created_at = Column(DateTime, default=func.now())

# Pydantic模型 - 用于API请求验证和响应
class SensorDataBase(BaseModel):
    sensor_type: str
    sensor_value: float
    unit: Optional[str] = None
    device_id: str
    location: Optional[str] = None

class SensorDataCreate(SensorDataBase):
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

class SensorDataResponse(SensorDataBase):
    id: int
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# 批量创建模型
class SensorDataBatchCreate(BaseModel):
    data: list[SensorDataCreate]

# 查询参数模型
class SensorDataTimeRangeQuery(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    sensor_type: Optional[str] = None
    device_id: Optional[str] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0 