#!/usr/bin/env python3
"""
树莓派传感器数据采集与发送示例
此脚本演示如何从树莓派上的传感器读取数据并发送到API服务器
"""

import time
import random
import json
import requests
from datetime import datetime
import logging
from typing import Dict, Any, List, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API服务器配置
API_BASE_URL = "http://localhost:8000/api"  # 替换为实际API服务器地址
DEVICE_ID = "raspberry-pi-001"  # 设备ID
LOCATION = "实验室-01"  # 设备位置

# 传感器类型配置
SENSORS = {
    "temperature": {
        "unit": "°C",
        "min": 18.0,
        "max": 28.0
    },
    "humidity": {
        "unit": "%",
        "min": 30.0,
        "max": 80.0
    },
    "pressure": {
        "unit": "hPa",
        "min": 990.0,
        "max": 1020.0
    },
    "light": {
        "unit": "lux",
        "min": 0.0,
        "max": 1000.0
    }
}

def read_sensor_data(sensor_type: str) -> float:
    """
    模拟从传感器读取数据
    在实际应用中，这里应该使用实际的传感器库读取数据
    例如：
    - 温湿度: Adafruit_DHT
    - 气压: BMP280
    - 光照: TSL2561
    """
    # 这里使用随机数模拟传感器数据
    sensor_config = SENSORS.get(sensor_type, {"min": 0, "max": 100})
    return random.uniform(sensor_config["min"], sensor_config["max"])

def collect_all_sensor_data() -> List[Dict[str, Any]]:
    """收集所有传感器数据"""
    data = []
    timestamp = datetime.now().isoformat()
    
    for sensor_type, config in SENSORS.items():
        try:
            value = read_sensor_data(sensor_type)
            data.append({
                "sensor_type": sensor_type,
                "sensor_value": value,
                "unit": config["unit"],
                "device_id": DEVICE_ID,
                "location": LOCATION,
                "timestamp": timestamp
            })
            logger.info(f"读取 {sensor_type} 传感器: {value} {config['unit']}")
        except Exception as e:
            logger.error(f"读取 {sensor_type} 传感器失败: {str(e)}")
    
    return data

def send_sensor_data(data: List[Dict[str, Any]]) -> bool:
    """将传感器数据发送到API服务器"""
    try:
        url = f"{API_BASE_URL}/sensor-data/batch"
        payload = {"data": data}
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 201:
            logger.info(f"成功发送 {len(data)} 条传感器数据")
            return True
        else:
            logger.error(f"发送数据失败: HTTP {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"发送数据时出错: {str(e)}")
        return False

def main():
    """主函数"""
    logger.info("树莓派传感器数据采集程序启动")
    
    try:
        while True:
            # 收集传感器数据
            sensor_data = collect_all_sensor_data()
            
            # 发送数据到API服务器
            if sensor_data:
                send_sensor_data(sensor_data)
            
            # 等待指定时间间隔
            time.sleep(60)  # 每分钟采集一次数据
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
    finally:
        logger.info("程序结束")

if __name__ == "__main__":
    main() 