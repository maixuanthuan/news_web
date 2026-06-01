"""
Scraper cho VnExpress.
Mỗi báo khác nhau thì tạo thêm file scraper riêng tương tự.
"""

import httpx
import re
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


async def scrape_vnexpress(url: str) -> dict:
    """
    Trả về:
    {
        "title":    str,
        "author":   str,
        "date":     str,
        "lead":     str,   # đoạn lead/sapo
        "content":  str,   # full HTML nội dung bài (đã làm sạch)
        "thumbnail": str,  # URL ảnh đại diện
    }
    """

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # ── Title
    title = ""
    tag = soup.find("h1", class_="title-detail")
    if tag:
        title = tag.get_text(strip=True)

    # ── Lead / Sapo
    lead = ""
    tag = soup.find("p", class_="description")
    if tag:
        lead = tag.get_text(strip=True)

    # ── Author
    author = ""
    tag = soup.find("strong", class_="author_mail") or soup.find("p", class_="author")
    if tag:
        author = tag.get_text(strip=True)

    # ── Date
    date = ""
    tag = soup.find("span", class_="date")
    if tag:
        date = tag.get_text(strip=True)

    # ── Thumbnail
    thumbnail = ""
    tag = soup.find("meta", property="og:image")
    if tag:
        thumbnail = tag.get("content", "")

    # ── Content
    content_html = ""
    tag = soup.find("article", class_="fck_detail")
    if tag:
        _clean_content(tag)
        content_html = str(tag)

    return {
        "title":     title,
        "author":    author,
        "date":      date,
        "lead":      lead,
        "content":   content_html,
        "thumbnail": thumbnail,
    }


def _clean_content(tag):
    """Xóa các phần không cần thiết trong nội dung bài"""

    # Xóa script, style, quảng cáo
    for el in tag.find_all(["script", "style", "iframe"]):
        el.decompose()

    # Xóa div quảng cáo VnExpress
    for el in tag.find_all("div", class_=re.compile(r"box_|banner|ads|relate|comment")):
        el.decompose()

    # Fix lazy load: chuyển data-src → src
    for img in tag.find_all("img"):
        data_src = img.get("data-src") or img.get("data-original")
        if data_src:
            img["src"] = f"/api/image-proxy?url={data_src}"
        # Xóa attribute lazy load
        for attr in ["data-src", "data-original", "loading"]:
            if attr in img.attrs:
                del img.attrs[attr]