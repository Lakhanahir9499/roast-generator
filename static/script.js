async function generateRoast() {
  const name = document.getElementById("name").value;
  const mood = document.getElementById("mood").value;
  const resultDiv = document.getElementById("result");
  const memeDiv = document.getElementById("meme");
  const audio = document.getElementById("audio");

  resultDiv.innerHTML = "Roasting...";
  memeDiv.innerHTML = "";
  audio.hidden = true;

  const response = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, mood }),
  });

  const data = await response.json();
  if (data.roast) {
    resultDiv.innerHTML = data.roast;
    memeDiv.innerHTML = `<p class='text-lg'>\"${data.roast}\"</p>`;
    if (data.audio) {
      audio.src = "data:audio/mp3;base64," + data.audio;
      audio.hidden = false;
      audio.load();
    }
  } else {
    resultDiv.innerHTML = "Error: " + data.error;
  }
}

function saveMeme() {
  html2canvas(document.getElementById("meme")).then((canvas) => {
    const link = document.createElement("a");
    link.download = "roast-meme.png";
    link.href = canvas.toDataURL();
    link.click();
  });
}
