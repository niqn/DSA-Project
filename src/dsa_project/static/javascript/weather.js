const $ = id => document.getElementById(id);

function tick() {
  const d = new Date(), h = d.getHours();
  $("greeting").textContent = h < 12 ? "Good morning" : h < 18 ? "Good afternoon" : "Good evening";
  $("today").textContent = d.toLocaleDateString("en-PH", { weekday: "long", month: "short", day: "numeric" });
  $("clock").textContent = d.toLocaleTimeString("en-PH");
}
tick();
setInterval(tick, 1000);         

async function load() {
  const res = await fetch("/weather/api/check?area=" + encodeURIComponent($("area").value));
  const d = await res.json();
  if (d.error) { $("level").textContent = d.error; return; }

  $("temp").textContent = d.temp + "°C";
  $("level").textContent = d.level;
  $("feelsLike").textContent = d.feels_like + "°C";
  $("humidity").textContent = d.humidity + "%";
  $("uv").textContent = d.uv;
  $("peak").textContent = d.peak + "°C";
  $("peakTime").textContent = d.peak_time;

  $("areaName").textContent = d.area;
  
  // check classes
  const sp = d.school_peak;
  let msg, tier;
  if (sp >= 42)      { msg = "Face-to-face and home-based activities suspended"; tier = "stop"; }
  else if (sp >= 33) { msg = "Face-to-face suspended, home-based tasks"; tier = "warn"; }
  else if (sp >= 27) { msg = "Shorter hours or hybrid may be allowed"; tier = "ok"; }
  else               { msg = "Regular classes"; tier = "ok"; }

  $("classStatus").textContent = msg;
  $("classStatus").className = "class-" + tier;
  $("classNote").textContent =
    "DepEd guide at " + sp + "°C. Your school's announcement is the final word.";

  const hr = new Date().getHours();
  const icon = (hr < 6 || hr >= 18) ? "fa-moon"
             : d.feels_like >= 42 ? "fa-fire"
             : d.feels_like >= 33 ? "fa-sun"
             : "fa-cloud-sun";
  $("wxIcon").className = "fa-solid " + icon;

  $("hotPeriod").textContent = d.hot_period
    ? "Hottest stretch: " + d.hot_period + " (33°C or higher)"
    : "No hours at 33°C or higher today";

  $("nextDanger").textContent = d.next_danger
    ? "Danger level (42°C+) starts at " + d.next_danger
    : "No danger-level hours ahead today";

  // queue
  $("alertQueue").innerHTML = d.alerts.length
    ? d.alerts.map(a => `<li>${a}</li>`).join("")
    : "<li>No hot hours ahead today</li>";

  // array
  $("readings").innerHTML = d.readings.map((v, i) =>
    `<div class="hour"><span>${String(i).padStart(2, "0")}:00</span><strong>${v}°C</strong></div>`
  ).join("");
  const box = $("readings"), now = new Date().getHours();
  box.scrollLeft = box.children[now].offsetLeft - box.offsetLeft;
}

// coords
const CITY_COORDS = {
  "Bacoor": [14.4624, 120.9645],
  "Dasmariñas": [14.3294, 120.9367],
  "Imus": [14.4297, 120.9367],
  "General Trias": [14.3869, 120.8814],
};

// find the closest city to the user
function nearestCity(lat, lon) {
  let best = null, bestKm = Infinity;
  for (const [name, [clat, clon]] of Object.entries(CITY_COORDS)) {
    const dLat = lat - clat;
    const dLon = (lon - clon) * Math.cos(lat * Math.PI / 180);
    const km = Math.sqrt(dLat * dLat + dLon * dLon) * 111;  
    if (km < bestKm) { best = name; bestKm = km; }
  }
  return { name: best, km: bestKm };
}

$("btnLoc").addEventListener("click", () => {
  if (!navigator.geolocation) {
    $("btnLoc").textContent = "Location not supported";
    return;
  }
  $("btnLoc").textContent = "Finding you...";

  navigator.geolocation.getCurrentPosition(
    pos => {
      const c = nearestCity(pos.coords.latitude, pos.coords.longitude);
      $("area").value = c.name;                    
      $("btnLoc").textContent = c.km > 30
        ? "Far from these cities, showing " + c.name
        : "Nearest: " + c.name;
      load();                                     
    },
    () => { $("btnLoc").textContent = "Location blocked, use the dropdown"; }
  );
});

$("area").addEventListener("change", load);
load();