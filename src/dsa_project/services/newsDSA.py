import time
from email.utils import parsedate_to_datetime
import requests
import xml.etree.ElementTree as ET
import re

# dsa application


class newsNode:
    def __init__(self, item):
        self.item = item
        self.next = None


class newsList:
    def __init__(self):
        self.head = None

    def insertSort(self, item):
        new_node = newsNode(item)

        if not self.head or item["date"] > self.head.item["date"]:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.item["date"] >= item["date"]:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def to_list(self):
        items = []
        current_node = self.head
        while current_node:
            items.append(current_node.item)
            current_node = current_node.next
        return items


# for the news page
FEEDS = [
    "Bacoor",
    "Bacoor Cavite",
    "Bacoor city government",
    "Bacoor flood OR typhoon",
    "Cavite news",
]

KEYWORDS = {
    "Flood":  ["flood", "typhoon", "rain", "baha"],
    "Heat":   ["heat", "init", "temperature"],
    "Power":  ["power", "brownout", "meralco", "electric"],
    "Health": ["health", "hospital", "clinic", "dengue", "vaccine"],
    "Roads":  ["road", "traffic", "bridge", "construction"],
    "Water":  ["water", "tubig", "maynilad", "baha"],
}

CATEGORIES = ["Roads", "Health", "Heat",
              "Flood", "Power", "Community", "Water"]


def get_tag(title):
    text = title.lower()
    for tag, words in KEYWORDS.items():
        for word in words:
            if re.search(r"\b" + word, text):
                return tag
    return "Community"


_cache = {"items": [], "time": 0}
CACHE_SECONDS = 1800


def get_news(category=None):
    now = time.time()
    if not _cache["items"] or now - _cache["time"] > CACHE_SECONDS:
        _cache["items"] = fetch_all_news()
        _cache["time"] = now

    items = _cache["items"]
    if category:
        items = [i for i in items if i["tag"] == category]

    items = [dict(i) for i in items[:20]]
    for i in items:
        i["date"] = i["date"].strftime("%b %d, %Y")
    return items


def fetch_all_news():
    news_list = newsList()
    seen = set()

    for q in FEEDS:
        try:
            r = requests.get("https://news.google.com/rss/search", params={
                             "q": q, "hl": "en-PH", "gl": "PH", "ceid": "PH:en"}, timeout=10)
            root = ET.fromstring(r.content)
        except Exception:
            continue

        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            title = title.rsplit(" - ", 1)[0]
            pub = item.findtext("pubDate")

            if not title or not pub or title in seen:
                continue
            seen.add(title)

            news_list.insertSort({
                "title": title,
                "source": item.findtext("source", "Unknown"),
                "url": item.findtext("link", ""),
                "date": parsedate_to_datetime(pub),
                "tag": get_tag(title),
            })

    return news_list.to_list()
