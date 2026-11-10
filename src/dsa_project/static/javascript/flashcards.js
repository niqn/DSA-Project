const card = document.getElementById("card");

if (card) {
  let showingFront = true;
  card.addEventListener("click", () => {
    showingFront = !showingFront;
    document.getElementById("face").textContent = showingFront ? FRONT : BACK;
    card.classList.toggle("back", !showingFront);
  });
}