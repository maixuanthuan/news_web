from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import router   # bỏ tiền tố "app."

app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend"), name="static")
app.include_router(router, prefix="/api")


@app.get("/")
async def home():
    return FileResponse("../frontend/index.html")
