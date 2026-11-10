const buttons = document.querySelectorAll(".simon-btn");
const levelText = document.getElementById("levelText");
const highScoreText = document.getElementById("highScore");
const startBtn = document.getElementById("startBtn");

let sequence = [];
let level = 0;
let playerIndex = 0;
let highScore = 0;
let accepting = false;
let playing = false;
let playToken = 0;

function randomNumber() {
  return Math.floor(Math.random() * 9) + 1;
}

function startGame() {
  playToken++;
  sequence = [];
  level = 0;
  playerIndex = 0;
  playing = true;
  highScoreText.textContent = highScore;
  nextLevel();
}

function nextLevel() {
  level++;
  playerIndex = 0;
  accepting = false;
  sequence.push(randomNumber());
  levelText.textContent = "Level: " + level;
  playSequence();
}

function playSequence() {
  const current = playToken;
  let delay = 0;
  for (let i = 0; i < sequence.length; i++) {
    const button = document.querySelector('.simon-btn[data-number="' + sequence[i] + '"]');
    setTimeout(function () {
      if (current !== playToken) return;
      flash(button);
    }, delay);
    delay += 600;
  }
  setTimeout(function () {
    if (current !== playToken) return;
    accepting = true;
  }, delay);
}

function flash(button) {
  button.classList.add("flash");
  setTimeout(function () {
    button.classList.remove("flash");
  }, 350);
}

function gameOver() {
  playing = false;
  accepting = false;
  playToken++;
  if (level - 1 > highScore) {
    highScore = level - 1;
  }
  highScoreText.textContent = highScore;
  levelText.textContent = "Game Over";
}

function handleClick(event) {
  if (!playing || !accepting) return;

  const button = event.currentTarget;
  const number = Number(button.dataset.number);

  button.classList.add("pressed");
  setTimeout(function () {
    button.classList.remove("pressed");
  }, 200);

  if (number !== sequence[playerIndex]) {
    gameOver();
    return;
  }

  playerIndex++;

  if (playerIndex === sequence.length) {
    accepting = false;
    setTimeout(nextLevel, 700);
  }
}

for (let i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener("click", handleClick);
}

startBtn.addEventListener("click", startGame);
