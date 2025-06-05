from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime

from models.sensor_data import SensorData, SensorDataCreate, SensorDataTimeRangeQuery

class SensorService:
    """传感器数据服务，提供数据操作方法"""
    
    @staticmethod
    def create_sensor_data(db: Session, data: SensorDataCreate) -> SensorData:
        """创建单条传感器数据"""
        db_sensor_data = SensorData(
            sensor_type=data.sensor_type,
            sensor_value=data.sensor_value,
            unit=data.unit,
            device_id=data.device_id,
            location=data.location,
            timestamp=data.timestamp
        )
        db.add(db_sensor_data)
        db.commit()
        db.refresh(db_sensor_data)
        return db_sensor_data
    
    @staticmethod
    def create_sensor_data_batch(db: Session, data_list: List[SensorDataCreate]) -> List[SensorData]:
        """批量创建传感器数据"""
        db_sensor_data_list = [
            SensorData(
                sensor_type=data.sensor_type,
                sensor_value=data.sensor_value,
                unit=data.unit,
                device_id=data.device_id,
                location=data.location,
                timestamp=data.timestamp
            ) for data in data_list
        ]
        db.add_all(db_sensor_data_list)
        db.commit()
        
        # 返回已创建的对象，但没有ID (批量插入时难以获取)
        return db_sensor_data_list
    
    @staticmethod
    def get_sensor_data(db: Session, sensor_data_id: int) -> Optional[SensorData]:
        """根据ID获取传感器数据"""
        return db.query(SensorData).filter(SensorData.id == sensor_data_id).first()
    
    @staticmethod
    def get_all_sensor_data(
        db: Session, 
        limit: int = 100, 
        offset: int = 0
    ) -> List[SensorData]:
        """获取所有传感器数据，带分页"""
        return db.query(SensorData).order_by(SensorData.timestamp.desc()).limit(limit).offset(offset).all()
    
    @staticmethod
    def get_sensor_data_by_type(
        db: Session, 
        sensor_type: str,
        limit: int = 100, 
        offset: int = 0
    ) -> List[SensorData]:
        """根据传感器类型获取数据"""
        return db.query(SensorData).filter(SensorData.sensor_type == sensor_type).order_by(SensorData.timestamp.desc()).limit(limit).offset(offset).all()
    
    @staticmethod
    def get_sensor_data_by_device(
        db: Session, 
        device_id: str,
        limit: int = 100, 
        offset: int = 0
    ) -> List[SensorData]:
        """根据设备ID获取数据"""
        return db.query(SensorData).filter(SensorData.device_id == device_id).order_by(SensorData.timestamp.desc()).limit(limit).offset(offset).all()
    
    @staticmethod
    def get_sensor_data_by_time_range(
        db: Session,
        query_params: SensorDataTimeRangeQuery
    ) -> List[SensorData]:
        """根据时间范围和其他条件查询数据"""
        query = db.query(SensorData)
        
        # 添加筛选条件
        if query_params.start_time:
            query = query.filter(SensorData.timestamp >= query_params.start_time)
        if query_params.end_time:
            query = query.filter(SensorData.timestamp <= query_params.end_time)
        if query_params.sensor_type:
            query = query.filter(SensorData.sensor_type == query_params.sensor_type)
        if query_params.device_id:
            query = query.filter(SensorData.device_id == query_params.device_id)
            
        # 添加排序、分页
        query = query.order_by(SensorData.timestamp.desc())
        query = query.limit(query_params.limit).offset(query_params.offset)
        
        return query.all()
    
    @staticmethod
    def get_sensor_statistics(
        db: Session,
        sensor_type: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """获取传感器数据统计信息"""
        query = db.query(
            func.avg(SensorData.sensor_value).label("avg_value"),
            func.min(SensorData.sensor_value).label("min_value"),
            func.max(SensorData.sensor_value).label("max_value"),
            func.count(SensorData.id).label("count")
        ).filter(SensorData.sensor_type == sensor_type)
        
        if start_time:
            query = query.filter(SensorData.timestamp >= start_time)
        if end_time:
            query = query.filter(SensorData.timestamp <= end_time)
            
        stats = query.first()
        
        if not stats:
            return {
                "avg_value": 0,
                "min_value": 0,
                "max_value": 0,
                "count": 0
            }
            
        return {
            "avg_value": float(stats.avg_value) if stats.avg_value else 0,
            "min_value": float(stats.min_value) if stats.min_value else 0,
            "max_value": float(stats.max_value) if stats.max_value else 0,
            "count": stats.count
        } 