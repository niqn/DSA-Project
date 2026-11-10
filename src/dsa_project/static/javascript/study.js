const card = document.getElementById("nowCard");

if (card) {
  const countdown = document.getElementById("countdown");
  const startBtn = document.getElementById("startBtn");

  let remaining = Number(card.dataset.minutes) * 60;   
  let endAt = null;
  let timer = null;

  function show() {
    const m = String(Math.floor(remaining / 60)).padStart(2, "0");
    const s = String(remaining % 60).padStart(2, "0");
    countdown.textContent = m + ":" + s;
  }

  function tick() {
    remaining = Math.max(0, Math.round((endAt - Date.now()) / 1000));
    show();
    if (remaining === 0) {
      clearInterval(timer);
      countdown.textContent = "Time's up!";
      startBtn.disabled = true;
    }
  }

  show();

  startBtn.addEventListener("click", () => {
    if (timer) {                       
      clearInterval(timer);
      timer = null;
      startBtn.textContent = "Resume";
      return;
    }
    endAt = Date.now() + remaining * 1000;
    timer = setInterval(tick, 250);
    startBtn.textContent = "Pause";
  });
}