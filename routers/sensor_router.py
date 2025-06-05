from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from models.database import get_db
from models.sensor_data import (
    SensorDataCreate, 
    SensorDataResponse, 
    SensorDataBatchCreate,
    SensorDataTimeRangeQuery
)
from services.sensor_service import SensorService

router = APIRouter(
    prefix="/api/sensor-data",
    tags=["sensor-data"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=SensorDataResponse, status_code=201)
def create_sensor_data(
    data: SensorDataCreate,
    db: Session = Depends(get_db)
):
    """创建单条传感器数据"""
    return SensorService.create_sensor_data(db, data)

@router.post("/batch", response_model=dict, status_code=201)
def create_sensor_data_batch(
    data: SensorDataBatchCreate,
    db: Session = Depends(get_db)
):
    """批量创建传感器数据"""
    result = SensorService.create_sensor_data_batch(db, data.data)
    return {"success": True, "count": len(result)}

@router.get("/", response_model=List[SensorDataResponse])
def get_all_sensor_data(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """获取所有传感器数据"""
    return SensorService.get_all_sensor_data(db, limit, offset)

@router.get("/{sensor_data_id}", response_model=SensorDataResponse)
def get_sensor_data(
    sensor_data_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取传感器数据"""
    db_sensor_data = SensorService.get_sensor_data(db, sensor_data_id)
    if db_sensor_data is None:
        raise HTTPException(status_code=404, detail="传感器数据不存在")
    return db_sensor_data

@router.get("/sensor/{sensor_type}", response_model=List[SensorDataResponse])
def get_sensor_data_by_type(
    sensor_type: str,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """根据传感器类型获取数据"""
    return SensorService.get_sensor_data_by_type(db, sensor_type, limit, offset)

@router.get("/device/{device_id}", response_model=List[SensorDataResponse])
def get_sensor_data_by_device(
    device_id: str,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """根据设备ID获取数据"""
    return SensorService.get_sensor_data_by_device(db, device_id, limit, offset)

@router.post("/time-range", response_model=List[SensorDataResponse])
def get_sensor_data_by_time_range(
    query_params: SensorDataTimeRangeQuery,
    db: Session = Depends(get_db)
):
    """根据时间范围和其他条件查询数据"""
    return SensorService.get_sensor_data_by_time_range(db, query_params)

# 统计API路由
statistics_router = APIRouter(
    prefix="/api/statistics",
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)

@statistics_router.get("/sensor/{sensor_type}")
def get_sensor_statistics(
    sensor_type: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """获取传感器数据统计信息"""
    return SensorService.get_sensor_statistics(db, sensor_type, start_time, end_time) 