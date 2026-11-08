from datetime import datetime, timedelta, timezone
import requests
# dsa application

class ArrayList:
    def __init__(self):
        self.items = [None] * 4
        self.count = 0

    def add(self, item):
        if self.count == len(self.items):
            bigger = [None] * (len(self.items) * 2)
            for i in range(self.count):
                bigger[i] = self.items[i]
            self.items = bigger
        self.items[self.count] = item
        self.count += 1

    def get(self, i):
        if i < 0 or i >= self.count:
            raise IndexError("Index out of bounds")
        return self.items[i]

    def size(self):
        return self.count

    def to_list(self):
        return [self.items[i] for i in range(self.count)]


class QueueNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, value):
        new_node = QueueNode(value)
        if self.rear:
            self.rear.next = new_node
        else:
            self.front = new_node
        self.rear = new_node

    def dequeue(self):
        if not self.front:
            return None

        value = self.front.value
        self.front = self.front.next

        if not self.front:
            self.rear = None
        return value


# weather
PH_TZ = timezone(timedelta(hours=8))

COORDS = {
    "Bacoor": (14.4624, 120.9645),
    "Dasmariñas": (14.3294, 120.9367),
    "Imus": (14.4297, 120.9367),
    "General Trias": (14.3869, 120.8814),
}
LOCATIONS = list(COORDS)

HOT = 33      
DANGER = 42

def heat_index(temp_c, humidity):
    """Estimated heat index in °C (NOAA formula)."""
    t = temp_c * 9 / 5 + 32
    if t < 80:                      
        return round(temp_c, 1)
    hi = (-42.379 + 2.04901523 * t + 10.14333127 * humidity
          - 0.22475541 * t * humidity - 0.00683783 * t * t
          - 0.05481717 * humidity * humidity
          + 0.00122874 * t * t * humidity
          + 0.00085282 * t * humidity * humidity
          - 0.00000199 * t * t * humidity * humidity)
    return round((hi - 32) * 5 / 9, 1)


def level(hi):
    if hi >= 52:
        return "Extreme Danger"
    if hi >= 42:
        return "Danger"
    if hi >= 33:
        return "Extreme Caution"
    if hi >= 27:
        return "Caution"
    return "Normal"


def check_heat(area):
    if area not in COORDS:
        return {"error": "Unknown location"}
    lat, lon = COORDS[area]

    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": lat, "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,uv_index",
            "forecast_days": 1, "timezone": "Asia/Manila",
        }, timeout=10)
        h = r.json()["hourly"]

    except Exception:
        return {"error": "Could not load weather data"}

    readings = ArrayList()
    for temp, rh in zip(h["temperature_2m"], h["relative_humidity_2m"]):
        readings.add(heat_index(temp, rh))

    # peak
    peak_i = 0
    for i in range(readings.size()):
        if readings.get(i) > readings.get(peak_i):
            peak_i = i

    best_start, best_len = 0, 0
    run_start, run_len = 0, 0
    for i in range(readings.size()):
        if readings.get(i) >= HOT:
            if run_len == 0:
                run_start = i
            run_len += 1
            if run_len > best_len:
                best_start, best_len = run_start, run_len
        else:
            run_len = 0

    hot_period = None
    if best_len > 0:
        hot_period = f"{best_start:02d}:00 to {(best_start + best_len) % 24:02d}:00"

    # queue
    now = datetime.now(PH_TZ).hour
    ahead = Queue()
    for hour in range(now, readings.size()):
        ahead.enqueue(hour)

    alert_list = []
    next_danger = None
    while not ahead.is_empty():
        hour = ahead.dequeue()
        hi = readings.get(hour)

        if hi >= HOT:
            alert_list.append(f"{hour:02d}:00 - {level(hi)} ({hi}°C)")
        if hi >= DANGER and next_danger is None:
            next_danger = f"{hour:02d}:00"      

    feels = readings.get(now)

    # check peak based on deped memo
    checks = [readings.get(8), readings.get(12), readings.get(14)]
    school_peak = checks[0]
    for value in checks:
        if value > school_peak:
            school_peak = value

    return {
        "area": area,
        "temp": h["temperature_2m"][now],
        "feels_like": feels,
        "level": level(feels),
        "humidity": h["relative_humidity_2m"][now],
        "uv": h["uv_index"][now],
        "peak": readings.get(peak_i),
        "peak_time": f"{peak_i:02d}:00",
        "hot_period": hot_period,
        "next_danger": next_danger,
        "alerts": alert_list,
        "readings": readings.to_list(),
        "checks": checks,
        "school_peak": school_peak,
        "array_size": readings.size(),
        "array_capacity": len(readings.items),
        "queue_count": len(alert_list),
    }