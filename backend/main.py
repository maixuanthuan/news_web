from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import router

app = FastAPI()

# Dùng path tuyệt đối → chạy đúng cả local lẫn Railway
BASE_DIR = Path(__file__).parent.parent          # thư mục gốc news_web/
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
app.include_router(router, prefix="/api")


@app.get("/")
async def home():
    return FileResponse(FRONTEND_DIR / "index.html")