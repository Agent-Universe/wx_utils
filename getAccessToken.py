from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import json
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging
from logging.handlers import TimedRotatingFileHandler

# 加载环境变量
load_dotenv()

# 微信小程序的AppID和AppSecret
app_id = os.getenv('APP_ID', 'your_app_id')
app_secret = os.getenv('APP_SECRET', 'your_app_secret')

# 初始化 FastAPI 应用
app = FastAPI()

# 初始化全局变量
access_token = None
last_refresh_time = 0

# 配置日志记录器
log_dir = '.log'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'access_token.log')
logger = logging.getLogger('access_token_logger')
logger.setLevel(logging.INFO)

# 创建日志文件处理器，按周轮换日志文件
handler = TimedRotatingFileHandler(log_file, when='W0', interval=1, backupCount=4)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# 获取access_token
def get_access_token(app_id, app_secret):
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}'
    response = requests.get(url)
    data = response.json()
    if 'access_token' in data:
        logger.info(f"Successfully fetched access token: {data['access_token']}")
        return data['access_token']
    else:
        logger.error(f"Failed to fetch access token: {data}")
        raise HTTPException(status_code=500, detail=data)

# 定时任务：每7000秒刷新一次access_token
def refresh_access_token():
    global access_token, last_refresh_time
    try:
        access_token = get_access_token(app_id, app_secret)
        last_refresh_time = time.time()
        logger.info("Access token refreshed successfully")
    except Exception as e:
        logger.error(f"Failed to refresh access token: {e}")

# 启动定时任务
scheduler = BackgroundScheduler()
scheduler.add_job(refresh_access_token, 'interval', seconds=7000)
scheduler.start()

# 获取当前的access_token
@app.get("/access_token")
def get_current_access_token():
    global access_token
    if access_token:
        logger.info("Access token retrieved successfully")
        return JSONResponse(content={"access_token": access_token})
    else:
        logger.error("Access token not available")
        raise HTTPException(status_code=500, detail="Access token not available")

# 手动刷新access_token
@app.post("/refresh_token")
def manual_refresh_token():
    global access_token, last_refresh_time
    try:
        access_token = get_access_token(app_id, app_secret)
        last_refresh_time = time.time()
        logger.info("Access token manually refreshed successfully")
        return JSONResponse(content={"message": "Access token refreshed successfully", "access_token": access_token})
    except Exception as e:
        logger.error(f"Failed to manually refresh access token: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 启动 FastAPI 应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)