const $ = id => document.getElementById(id);

function tick() {
  const d = new Date();
  $("clock").textContent =
    d.toLocaleDateString("en-PH", { weekday: "long", month: "short", day: "numeric" }) +
    ", " + d.toLocaleTimeString("en-PH");
}
tick();
setInterval(tick, 1000);

function fillBarangays() {
  const list = BARANGAYS[$("city").value] || [];
  $("barangay").innerHTML = '<option value="">All barangays</option>' +
    list.map(b => `<option value="${b}" ${b === SELECTED_BARANGAY ? "selected" : ""}>${b}</option>`).join("");
}
$("city").addEventListener("change", fillBarangays);
fillBarangays();

const CITY_COORDS = {
  "Bacoor": [14.4624, 120.9645],
  "Dasmariñas": [14.3294, 120.9367],
  "Imus": [14.4297, 120.9367],
  "General Trias": [14.3869, 120.8814],
};

function nearestCity(lat, lon) {
  let best = null, bestKm = Infinity;
  for (const [name, [clat, clon]] of Object.entries(CITY_COORDS)) {
    const dLat = lat - clat;
    const dLon = (lon - clon) * Math.cos(lat * Math.PI / 180);
    const km = Math.sqrt(dLat * dLat + dLon * dLon) * 111;
    if (km < bestKm) { best = name; bestKm = km; }
  }
  return best;
}

const norm = s => s.toLowerCase().replace(/[^a-z0-9]/g, "");

// show the message left by the last click 
const savedMsg = sessionStorage.getItem("locMsg");
if (savedMsg) { $("locStatus").textContent = savedMsg; sessionStorage.removeItem("locMsg"); }

$("btnLoc").addEventListener("click", () => {
  if (!navigator.geolocation) { $("locStatus").textContent = "Location not supported"; return; }
  $("locStatus").textContent = "Finding you...";

  navigator.geolocation.getCurrentPosition(async pos => {
    const lat = pos.coords.latitude, lon = pos.coords.longitude;
    const city = nearestCity(lat, lon);
        if (city !== "Bacoor") { $("locStatus").textContent = "Only Bacoor hotlines are available so far."; return; }
    
    $("city").value = city;
    fillBarangays();

    // ask OpenStreetMap which barangay these coordinates are in
    let found = "";
    try {
      const res = await fetch("https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=16&addressdetails=1&lat=" + lat + "&lon=" + lon);
      const a = (await res.json()).address || {};
      const guesses = [a.suburb, a.neighbourhood, a.quarter, a.village, a.city_district].filter(Boolean).map(norm);
      for (const opt of $("barangay").options) {
        if (opt.value && guesses.includes(norm(opt.value.replace(/\(.*\)/, "")))) { found = opt.value; break; }
      }
    } catch (e) { }

    if (found) $("barangay").value = found;
    sessionStorage.setItem("locMsg", found
      ? "Detected: " + found + ", " + city
      : "Nearest city: " + city + ". Pick your barangay.");
    $("city").form.submit();
  }, () => { $("locStatus").textContent = "Location blocked, use the dropdown"; });
});