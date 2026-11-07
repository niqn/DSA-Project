CITIES = ["Bacoor"]
CATEGORIES = ["Police", "Fire", "Medical", "Disaster"]

# the city directory's entries
BARANGAYS = {
    "Bacoor": [
        "Aniban I (I, III, V)", "Aniban II (II, IV)", "Bayanan", "Dulong Bayan",
        "Habay I", "Habay II", "Kaingin Digman", "Ligas I (I, II)", "Ligas II (III)",
        "Mabolo (I, II, III)", "Maliksi I", "Maliksi II (II, III)",
        "Mambog I", "Mambog II (II, V)", "Mambog III", "Mambog IV",
        "Molino I", "Molino II", "Molino III", "Molino IV", "Molino V", "Molino VI", "Molino VII",
        "Niog (I, II, III)", "P.F. Espiritu I", "P.F. Espiritu II (II, III)",
        "P.F. Espiritu III (IV)", "P.F. Espiritu IV (V, VI)", "P.F. Espiritu V (VII)",
        "P.F. Espiritu VI (VIII)", "Poblacion (Tabing Dagat, Daang Bukid, Campo Santo)",
        "Queens Row Central", "Queens Row East", "Queens Row West", "Real (I, II)",
        "Salinas I", "Salinas II (II, III, IV)", "San Nicolas I", "San Nicolas II", "San Nicolas III",
        "Sinbanali (Sineguelasan, Banalo, Alima)", "Talaba I (I, III, VII)", "Talaba II",
        "Talaba III (IV, V, VI)", "Zapote I (I, II)", "Zapote II (III, IV)", "Zapote III (V)",
    ],
}


def record(name, category, city, barangay, numbers, source, note=""):
    return {"name": name, "category": category, "city": city, "barangay": barangay,
            "numbers": numbers, "source": source, "note": note,
            "verified": ""}         


NOTICE = "bacoor.gov.ph notice, Sep 2024"
DIRECTORY = "Bacoor hospital directory (not yet confirmed)"
FIRE_AD = "Bacoor advisory, Mar 2026 (not yet confirmed)"
HALL_SRC = "Bacoor barangay hall directory (not yet confirmed)"

HOTLINES = [
    record("National Emergency Hotline", "General", "All", "", ["911"], "national hotline"),
    record("Bacoor City Emergency Line", "General", "Bacoor", "", ["161"], NOTICE),

    record("PNP Bacoor", "Police", "Bacoor", "",
           ["(046) 417-6366", "0977-752-0819", "0998-598-5593"], NOTICE,
           "The two mobile numbers are from the Sep 2024 notice, the landline is from the city directory"),

    record("BFP Bacoor (citywide)", "Fire", "Bacoor", "",
           ["0966-695-9711", "(046) 417-6060", "(046) 418-0241"], NOTICE),
    record("Central Fire Station", "Fire", "Bacoor", "Bayanan", ["0966-695-9711"], FIRE_AD),
    record("Molino Fire Sub-Station", "Fire", "Bacoor", "", ["0924-403-3245"], FIRE_AD,
           "Executive 2, Daang Hari Road"),
    record("San Nicolas Fire Sub-Station", "Fire", "Bacoor", "San Nicolas III", ["0924-565-1811"], FIRE_AD,
           "Green Valley"),
    record("Talaba Fire Sub-Station", "Fire", "Bacoor", "Talaba III (IV, V, VI)", ["0975-703-7435"], FIRE_AD,
           "Talaba III, Zone 4"),

    # hospitals
    record("Bacoor Doctors Medical Center", "Medical", "Bacoor", "Bayanan",
           ["(046) 416-6275", "(046) 416-6590", "0917-483-4949"], DIRECTORY),
    record("Crisostomo General Hospital", "Medical", "Bacoor", "Dulong Bayan",
           ["(046) 434-8239", "(046) 434-3195", "(046) 434-4805"], DIRECTORY),
    record("Southern Tagalog Regional Hospital", "Medical", "Bacoor", "Habay II",
           ["(046) 418-3644", "(046) 435-1071"], DIRECTORY, "Government hospital"),
    record("Molino Doctors Hospital", "Medical", "Bacoor", "Molino II",
           ["(046) 477-0830", "(046) 477-1661"], DIRECTORY),
    record("St. Michael Medical Hospital", "Medical", "Bacoor", "Molino II",
           ["(046) 477-1707", "(046) 477-1757"], DIRECTORY, "One listing says Molino IV, check it"),
    record("Cavite East Asia Medical Center", "Medical", "Bacoor", "Molino III",
           ["(046) 431-0000", "(02) 8584-4747"], DIRECTORY, "Formerly Southeast Asian Medical Center"),
    record("Metro South Medical Center", "Medical", "Bacoor", "Molino IV",
           ["(046) 477-3087", "(046) 477-1743", "(046) 885-6113", "(046) 230-9637"], DIRECTORY),
    record("South City Hospital and Medical Center", "Medical", "Bacoor", "Molino IV",
           ["(02) 8249-9100"], DIRECTORY),
    # barangay not matched to the directory's entries yet, so it shows citywide
    record("Prime Global Care Medical Center", "Medical", "Bacoor", "",
           ["(046) 970-5314", "(046) 477-0806"], DIRECTORY, "Bahayang Pag-asa Subd., Molino"),
    record("St. Dominic Medical Center", "Medical", "Bacoor", "",
           ["(046) 417-2520", "(046) 417-2525", "0998-599-4195"], DIRECTORY, "Talaba"),
]

HALLS = {
    "Aniban I (I, III, V)": ["417-7024"],
    "Bayanan": ["424-9453"],
    "Habay I": ["519-0223"],          
    "Ligas II (III)": ["417-7787"],
    "Mabolo (I, II, III)": ["436-0036"],
    "Maliksi I": ["417-8754"],
    "Mambog III": ["472-2726"],
    "Molino I": ["424-2559"],
    "Molino II": ["477-1539"],
    "Molino III": ["454-4667"],
    "Molino IV": ["477-1533"],
    "Molino VI": ["476-0461", "572-0455"],
    "P.F. Espiritu II (II, III)": ["417-4140"],
    "Poblacion (Tabing Dagat, Daang Bukid, Campo Santo)": ["571-5114"],
    "Real (I, II)": ["471-2116"],
    "San Nicolas III": ["417-5001"],
    "Sinbanali (Sineguelasan, Banalo, Alima)": ["431-2569"],
    "Zapote I (I, II)": ["519-3452"],
}
for b, nums in HALLS.items():
    HOTLINES.append(record("Barangay Hall: " + b, "General", "Bacoor", b,
                           ["(046) " + n for n in nums], HALL_SRC, "Barangay hall, for local help"))

class StackNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.count = 0

    def push(self, value):
        node = StackNode(value)
        node.next = self.top
        self.top = node
        self.count += 1

    def pop(self):
        if not self.top:
            return None
        value = self.top.value
        self.top = self.top.next
        self.count -= 1
        return value

    def peek(self):
        return self.top.value if self.top else None

    def is_empty(self):
        return self.top is None

    def size(self):
        return self.count

    def to_list(self):
        items, cur = [], self.top
        while cur:
            items.append(cur.value)
            cur = cur.next
        return items


def remember_search(saved, q):
    stack = Stack()
    for item in reversed(saved):         
        stack.push(item)

    q = q.strip()
    if q and q != stack.peek():          
        stack.push(q)
    return stack.to_list()[:5]         


def forget_last(saved):
    stack = Stack()
    for item in reversed(saved):
        stack.push(item)
    stack.pop()
    return stack.to_list()

def search(city, barangay, category, q):
    q = q.strip().lower()
    found = []
    for r in HOTLINES:                                      
        if r["city"] not in ("All", city):
            continue
        if barangay and r["barangay"] not in ("", barangay):  
            continue
        if not barangay and r["name"].startswith("Barangay Hall"):
            continue                                         
        if category and r["category"] not in (category, "General"):
            continue
        if q and q not in r["name"].lower():
            continue
        found.append(r)
    return found