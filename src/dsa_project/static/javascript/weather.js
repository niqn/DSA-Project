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

  const rows = document.querySelectorAll("#infoPanel tbody tr");
  let active = rows[0];
  rows.forEach(r => {
    r.classList.remove("now");
    if (d.peak >= Number(r.dataset.min)) active = r;  
  });
  active.classList.add("now");

  $("suspendStatus").textContent =
    "Today's estimated peak is " + d.peak + "°C. DepEd guide: " + active.cells[1].textContent + ".";

  // queue
  $("alertQueue").innerHTML = d.alerts.length
    ? d.alerts.map(a => `<li>${a}</li>`).join("")
    : "<li>No danger hours today</li>";

  // array
  $("readings").innerHTML = d.readings.map((v, i) =>
    `<div class="hour"><span>${String(i).padStart(2, "0")}:00</span><strong>${v}°C</strong></div>`
  ).join("");
  const box = $("readings"), now = new Date().getHours();
  box.scrollLeft = box.children[now].offsetLeft - box.offsetLeft;
}

$("area").addEventListener("change", load);
load();