#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
손경제 유니버스 RSS 자동 생성 스크립트 (비공식)
- 프로그램: 본방(평일), 플러스(매일), 상담소(매일)
- 결과: public/rss_songecon.xml
"""
import sys
from datetime import datetime, timedelta, timezone
import requests
import xml.etree.ElementTree as ET
import os

KST = timezone(timedelta(hours=9))

PROGRAMS = [
    ("손에 잡히는 경제", "ECONOMY", "0830", True),       # 평일만
    ("손경제 플러스",   "ECONOMYPLUS", "2005", False),   # 매일
    ("손경제 상담소",   "ECONOMYCOUNSEL", "1352", False) # 매일
]

BASE_URL = "https://podcastfile.imbc.com/cgi-bin/podcast.fcgi/podcast/economy/{code}_{yyyymmdd}.mp3"

def exists(url: str, timeout=15) -> bool:
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True)
        if r.status_code in (403, 405):  # HEAD 제한시 GET 시도
            r = requests.get(url, timeout=timeout, stream=True)
        if not r.ok:
            return False
        size = int(r.headers.get("Content-Length", "0"))
        return size > 1000
    except requests.RequestException:
        return False

def collect_items(days: int = 10):
    today = datetime.now(KST)
    items = []
    for i in range(days):
        d = today - timedelta(days=i)
        ymd = d.strftime("%Y%m%d")
        dow = d.weekday()  # 0=Mon .. 6=Sun
        for name, code, hhmm, weekdays_only in PROGRAMS:
            if weekdays_only and dow >= 5:
                continue
            url = BASE_URL.format(code=code, yyyymmdd=ymd)
            if not exists(url):
                continue
            pub = d.replace(hour=int(hhmm[:2]), minute=int(hhmm[2:]), second=0, microsecond=0, tzinfo=KST)
            items.append({
                "title": f"{name} - {d.strftime('%Y-%m-%d')}",
                "url": url,
                "pubDate": pub,
                "guid": f"{code}-{ymd}"
            })
    items.sort(key=lambda x: x["pubDate"], reverse=True)
    return items

def rfc2822(dt: datetime) -> str:
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z")

def build_rss(items):
    rss = ET.Element("rss", attrib={"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "손경제 유니버스 (비공식 RSS)"
    ET.SubElement(channel, "link").text = "https://github.com/"
    ET.SubElement(channel, "description").text = "MBC 손경제/플러스/상담소의 자동 생성된 비공식 RSS. 개인적 용도로만."
    ET.SubElement(channel, "lastBuildDate").text = rfc2822(datetime.now(KST))
    for it in items:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = it["title"]
        ET.SubElement(item, "link").text = it["url"]
        ET.SubElement(item, "guid").text = it["guid"]
        ET.SubElement(item, "pubDate").text = rfc2822(it["pubDate"])
        enc = ET.SubElement(item, "enclosure")
        enc.set("url", it["url"])
        enc.set("type", "audio/mpeg")
    return ET.ElementTree(rss)

def main():
    days = int(os.getenv("DAYS", "10"))
    items = collect_items(days=days)
    os.makedirs("public", exist_ok=True)
    tree = build_rss(items)
    out = "public/rss_songecon.xml"
    tree.write(out, encoding="utf-8", xml_declaration=True)
    print(f"Generated {out} with {len(items)} items.")

if __name__ == "__main__":
    main()
