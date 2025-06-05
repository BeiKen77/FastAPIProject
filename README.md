# 树莓派传感器数据API

这是一个用于树莓派传感器数据采集和存储的FastAPI应用程序。该应用提供REST API接口，允许树莓派设备发送传感器数据并将其存储到MySQL数据库中。

## 功能特点

- 传感器数据的单条和批量上传
- 按ID、传感器类型、设备ID和时间范围查询数据
- 数据统计分析
- 异步SQL操作
- 交互式API文档

## 项目结构

```
FastAPIProject/
├── main.py                 # FastAPI主应用入口
├── config.py               # 配置文件
├── requirements.txt        # 项目依赖
├── raspberry_client.py     # 树莓派客户端示例
├── test_main.http          # API测试用例
├── models/                 # 数据模型
│   ├── __init__.py
│   ├── sensor_data.py      # 传感器数据模型
│   └── database.py         # 数据库连接和ORM模型
├── routers/                # API路由
│   ├── __init__.py
│   └── sensor_router.py    # 传感器数据相关API路由
└── services/               # 业务逻辑
    ├── __init__.py
    └── sensor_service.py   # 传感器数据处理服务
```

## 安装步骤

1. 克隆项目到本地

2. 创建虚拟环境并激活
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 配置数据库
   确保MySQL数据库已创建并可访问。数据库连接信息在`config.py`文件中配置。

5. 启动API服务器
   ```bash
   uvicorn main:app --reload
   ```

## API端点

### 传感器数据

- `POST /api/sensor-data` - 创建单条传感器数据
- `POST /api/sensor-data/batch` - 批量创建传感器数据
- `GET /api/sensor-data` - 获取所有传感器数据
- `GET /api/sensor-data/{id}` - 根据ID获取传感器数据
- `GET /api/sensor-data/sensor/{sensor_type}` - 根据传感器类型获取数据
- `GET /api/sensor-data/device/{device_id}` - 根据设备ID获取数据
- `POST /api/sensor-data/time-range` - 根据时间范围查询数据

### 数据统计

- `GET /api/statistics/sensor/{sensor_type}` - 获取传感器数据统计信息

## 使用树莓派客户端

提供了一个示例客户端脚本`raspberry_client.py`，演示如何从树莓派读取传感器数据并发送到API服务器。

在树莓派上运行:
```bash
python raspberry_client.py
```

## API文档

启动服务器后，可以通过以下URL访问交互式API文档:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 环境变量

可以通过`.env`文件或系统环境变量设置以下配置:

- `DB_HOST` - 数据库主机名
- `DB_USER` - 数据库用户名
- `DB_PASSWORD` - 数据库密码
- `DB_NAME` - 数据库名称
- `DB_PORT` - 数据库端口
- `DEBUG` - 调试模式(true/false) 