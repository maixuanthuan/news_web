import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime


# ── MAP RSS → CATEGORY ───────────────────────────────────────

RSS_SOURCES = {

    "doi-song": [
        "https://vnexpress.net/rss/doi-song.rss",
        "https://dantri.com.vn/xa-hoi.rss",
    ],

    "an-ninh": [
        "https://vnexpress.net/rss/phap-luat.rss",
        "https://dantri.com.vn/phap-luat.rss",
    ],

    "hoc-tap": [
        "https://vnexpress.net/rss/giao-duc.rss",
        "https://dantri.com.vn/giao-duc-khuyen-hoc.rss",
    ],

    "suc-khoe": [
        "https://vnexpress.net/rss/suc-khoe.rss",
        "https://dantri.com.vn/suc-khoe.rss",
    ],

    "giao-thong": [
        "https://vnexpress.net/rss/oto-xe-may.rss",
    ],

    "thoi-tiet": [
        "https://vnexpress.net/rss/thoi-su.rss",
    ],
}

ITEMS_PER_CATEGORY = 6
TIMEOUT = 10


# ── PARSE ─────────────────────────────────────────────────────

def parse_rss(xml_text: str) -> list[dict]:

    items = []

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    for item in root.iter("item"):

        title = (item.findtext("title") or "").strip()
        desc  = _strip_html(item.findtext("description") or "").strip()
        pub   = item.findtext("pubDate") or ""
        link  = (item.findtext("link") or "").strip()

        time_label = _format_time(pub)

        # Thumbnail: thử enclosure trước, rồi media:content
        thumbnail = ""
        enclosure = item.find("enclosure")
        if enclosure is not None:
            thumbnail = enclosure.get("url", "")

        if not thumbnail:
            media = item.find("{http://search.yahoo.com/mrss/}content")
            if media is not None:
                thumbnail = media.get("url", "")

        if title:
            items.append({
                "title":     title,
                "desc":      desc[:160] + "…" if len(desc) > 160 else desc,
                "time":      time_label,
                "link":      link,
                "thumbnail": thumbnail,
            })

    return items


def _strip_html(text: str) -> str:
    import re
    return re.sub(r"<[^>]+>", "", text)


def _format_time(pub_date: str) -> str:
    try:
        dt = parsedate_to_datetime(pub_date)
        diff = datetime.now(dt.tzinfo) - dt
        minutes = int(diff.total_seconds() / 60)

        if minutes < 60:
            return f"{minutes} phút trước"
        elif minutes < 1440:
            return f"{minutes // 60} giờ trước"
        else:
            return f"{minutes // 1440} ngày trước"
    except Exception:
        return ""


# ── FETCH ─────────────────────────────────────────────────────

async def fetch_news() -> dict:

    result = {cat: [] for cat in RSS_SOURCES}

    async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True) as client:

        for category, urls in RSS_SOURCES.items():

            for url in urls:

                try:
                    response = await client.get(url, headers={
                        "User-Agent": "Mozilla/5.0 (compatible; RSS reader)"
                    })
                    response.raise_for_status()
                    items = parse_rss(response.text)
                    result[category].extend(items)

                except Exception as e:
                    print(f"[RSS] Lỗi fetch {url}: {e}")
                    continue

            result[category] = result[category][:ITEMS_PER_CATEGORY]

    return result