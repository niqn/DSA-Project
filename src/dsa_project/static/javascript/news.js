function tick() {
  const d = new Date();
  document.getElementById("clock").textContent =  d.toLocaleDateString("en-PH", { weekday: "long", month: "short", day: "numeric" }) +
    ", " + d.toLocaleTimeString("en-PH");
}
tick();
setInterval(tick, 1000);     