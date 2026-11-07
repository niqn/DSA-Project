import time
from datetime import datetime, timedelta, timezone

from email.utils import parsedate_to_datetime

from concurrent.futures import ThreadPoolExecutor
import threading

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
PH_TZ = timezone(timedelta(hours=8))  
MAX_AGE_DAYS = 30

BARANGAYS = [
    "Alima", "Aniban", "Banalo", "Habay", "Kaingin Digman",
    "Mambog", "Molino", "Niog", "P.F. Espiritu", "PF Espiritu", "Queens Row",
]

PLACES = BARANGAYS + ["Bacoor"]

FEEDS = [
    ('Bacoor (brownout OR "power interruption" OR Meralco OR blackout)', "Power"),
    ('Bacoor (water OR Maynilad OR "water interruption")', "Water"),
    ('Bacoor (heat OR "El Niño" OR mainit OR temperature)', "Heat"),
    ('Bacoor (dengue OR hospital OR health OR clinic OR DOH)', "Health"),
    ('Bacoor (flood OR typhoon OR habagat OR baha OR bagyo)', "Flood"),
    ('Bacoor (traffic OR road OR LRT OR Cavitex OR bridge)', "Roads"),
    ('Bacoor (school OR students OR DepEd OR "class suspension")', "Education"),
    ('Bacoor (police OR arrested OR killed OR crime)', "Crime"),
    ('Bacoor (mayor OR "city hall" OR council OR ordinance OR LGU)', "Government"),
    ('Bacoor (fire OR accident OR crash)', "Community"),
    ('Bacoor (business OR investment OR project OR program)', "Community"),
    ('Bacoor (sports OR basketball OR event OR festival)', "Community"),
    ('"Bacoor City"', "Community"),
    ('"Bacoor, Cavite"', "Community"),
    ('Bacoor balita', "Community"),
    ('Bacoor', "Community"),
]

KEYWORDS = {
    "Flood":      ["flood", "typhoon", "storm", "rain", "baha", "habagat", "bagyo", "tide"],
    "Power":      ["power", "brownout", "meralco", "electric", "blackout"],
    "Water":      ["water", "tubig", "maynilad"],
    "Heat":       ["heat", "mainit", "temperature", "el nino", "drought"],
    "Health":     ["health", "hospital", "clinic", "dengue", "vaccine", "disease", "outbreak", "doh"],
    "Roads":      ["road", "traffic", "bridge", "construction", "highway", "cavitex", "flyover", "lrt"],
    "Education":  ["school", "student", "deped", "university", "class suspension"],
    "Crime":      ["killed", "arrest", "police", "shooting", "murder", "robbery", "suspect"],
    "Government": ["mayor", "city hall", "council", "ordinance", "lgu", "barangay", "election", "budget"],
}

CATEGORIES = ["Flood", "Power", "Water", "Heat", "Health",
              "Roads", "Education", "Crime", "Government", "Community"]

for i in range(0, len(BARANGAYS), 6):
    group = " OR ".join(f'"{b}"' for b in BARANGAYS[i:i + 6])
    FEEDS.append((f"Bacoor ({group})", "Community"))

def find_place(title):
    text = title.lower()
    for place in PLACES:
        if re.search(r"\b" + re.escape(place.lower()) + r"\b", text):
            return place
    return None

def get_tag(title):
    text = title.lower()
    for tag, words in KEYWORDS.items():
        for word in words:
            if re.search(r"\b" + word, text):
                return tag
    return None


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
    
    now_dt = datetime.now(timezone.utc)
    for i in items:
        i["is_new"] = now_dt - i["date"] < timedelta(hours=24)
        i["date"] = i["date"].astimezone(PH_TZ).strftime("%b %d, %Y at %I:%M %p")
    return items


def fetch_feed(feed):
    query, default_tag = feed
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)

    try:
        r = requests.get("https://news.google.com/rss/search", params={"q": f"{query} when:{MAX_AGE_DAYS}d", "hl": "en-PH", "gl": "PH", "ceid": "PH:en"}, timeout=5,)
        root = ET.fromstring(r.content)
    except Exception:
        return []

    stories = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        title = title.rsplit(" - ", 1)[0]
        pub = item.findtext("pubDate")

        if not title or not pub:
            continue

        desc = item.findtext("description") or ""
        place = find_place(title) or find_place(desc)
        if not place:
            continue

        date = parsedate_to_datetime(pub)
        if date < cutoff:
            continue

        stories.append({
            "title": title,
            "source": item.findtext("source", "Unknown"),
            "url": item.findtext("link", ""),
            "date": date,
            "tag": get_tag(title) or default_tag,
            "place": place,
        })
    return stories


def fetch_all_news():
    news_list = newsList()
    seen = set()

    with ThreadPoolExecutor(max_workers=10) as pool:
        results = pool.map(fetch_feed, FEEDS)

    for stories in results:
        for story in stories:
            if story["title"] in seen:
                continue
            seen.add(story["title"])
            news_list.insertSort(story)

    return news_list.to_list()


# load the news in the background when the server starts
threading.Thread(target=get_news, daemon=True).start()
