const towerAButton = document.getElementById("towerA");
const towerBButton = document.getElementById("towerB");
const towerCButton = document.getElementById("towerC");
const moveText = document.getElementById("moveText");
const minText = document.getElementById("minText");
const statusText = document.getElementById("statusText");
const resetBtn = document.getElementById("resetBtn");
const diskCountSelect = document.getElementById("diskCount");

let towerA = [];
let towerB = [];
let towerC = [];
let selectedTower = null;
let diskCount = Number(diskCountSelect.value);
let moves = 0;
let solved = false;

function topDisk(tower) {
  return tower[tower.length - 1];
}

function minimumMoves() {
  return Math.pow(2, diskCount) - 1;
}

function diskWidth(size) {
  return Math.round((size * 100) / diskCount);
}

function startGame() {
  towerA = [];
  towerB = [];
  towerC = [];

  for (let size = diskCount; size > 0; size--) {
    towerA.push(size);
  }

  moves = 0;
  selectedTower = null;
  solved = false;
  moveText.textContent = "Moves: 0";
  minText.textContent = minimumMoves();
  statusText.textContent = "";
  render();
}

function handleTowerClick(clickedTower) {
  if (solved) return;

  if (selectedTower === null) {
    if (clickedTower.length === 0) return;
    selectedTower = clickedTower;
    render();
    return;
  }

  if (clickedTower === selectedTower) {
    selectedTower = null;
    render();
    return;
  }

  const disk = topDisk(selectedTower);
  const diskOnTarget = topDisk(clickedTower);
  const targetIsEmpty = clickedTower.length === 0;

  if (!targetIsEmpty && disk > diskOnTarget) {
    statusText.textContent = "You cannot place a bigger disk on a smaller one.";
    return;
  }

  selectedTower.pop();
  clickedTower.push(disk);
  moves++;
  selectedTower = null;

  moveText.textContent = "Moves: " + moves;
  statusText.textContent = "";
  checkWin();
  render();
}

function checkWin() {
  if (towerC.length === diskCount) {
    solved = true;
    statusText.textContent = "Solved in " + moves + " moves! Minimum possible: " + minimumMoves() + ".";
  }
}

function render() {
  renderTower(towerAButton, towerA);
  renderTower(towerBButton, towerB);
  renderTower(towerCButton, towerC);
}

function renderTower(towerButton, tower) {
  const pole = towerButton.querySelector(".hanoi-pole");
  pole.innerHTML = "";

  for (let i = 0; i < tower.length; i++) {
    const size = tower[i];
    const disk = document.createElement("div");
    disk.className = "disk";
    disk.style.width = diskWidth(size) + "%";

    const isTopDisk = i === tower.length - 1;
    if (isTopDisk && tower === selectedTower) {
      disk.classList.add("picked");
    }

    pole.appendChild(disk);
  }
}

towerAButton.addEventListener("click", function () { handleTowerClick(towerA); });
towerBButton.addEventListener("click", function () { handleTowerClick(towerB); });
towerCButton.addEventListener("click", function () { handleTowerClick(towerC); });
resetBtn.addEventListener("click", startGame);
diskCountSelect.addEventListener("change", function () {
  diskCount = Number(diskCountSelect.value);
  startGame();
});

startGame();
