from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from routers import sensor_router, statistics_router

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description="树莓派传感器数据API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(sensor_router)
app.include_router(statistics_router)

# 根路由
@app.get("/")
def root():
    return {"message": "欢迎使用树莓派传感器数据API"}

# 示例问候路由
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"你好 {name}，欢迎使用树莓派传感器数据API"}

# 如果作为主程序运行
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
