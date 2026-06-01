import time
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from urllib.parse import urlparse
from pydantic import BaseModel
from api.rss_fetcher import fetch_news               # bỏ tiền tố "app."
from api.scraper_vnexpress import scrape_vnexpress   # bỏ tiền tố "app."

router = APIRouter()


# ── CACHE ─────────────────────────────────────────────────────

CACHE_TTL = 300  # 5 phút

_cache = {
    "data": {},
    "last_fetch": 0.0,
}


async def get_news_data() -> dict:

    now = time.time()

    if now - _cache["last_fetch"] > CACHE_TTL or not _cache["data"]:
        print("[RSS] Fetching fresh data...")
        _cache["data"] = await fetch_news()
        _cache["last_fetch"] = now

    return _cache["data"]


# ── ROUTES ────────────────────────────────────────────────────

@router.get("/news")
async def get_news():
    return await get_news_data()


class ArticleRequest(BaseModel):
    url: str

@router.post("/article")
async def get_article(req: ArticleRequest):

    domain = urlparse(req.url).netloc

    if "vnexpress.net" in domain:
        return await scrape_vnexpress(req.url)

    raise HTTPException(status_code=400, detail=f"Chưa hỗ trợ nguồn: {domain}")


@router.get("/image-proxy")
async def image_proxy(url: str):
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        response = await client.get(url, headers={
            "Referer": "https://vnexpress.net/",
            "Origin": "https://vnexpress.net",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-site",
        })
    return StreamingResponse(
        iter([response.content]),
        media_type=response.headers.get("content-type", "image/jpeg")
    )
