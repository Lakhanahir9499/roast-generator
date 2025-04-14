async function generateRoast() {
  const name = document.getElementById("name").value;
  const mood = document.getElementById("mood").value;
  const res = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, mood })
  });
  const data = await res.json();
  document.getElementById("output").innerHTML = `
    <p>${data.roast}</p>
    <audio controls src="data:audio/mp3;base64,${data.voice}"></audio>
    <br/>
    <img src="${data.meme}" width="300" />
  `;
}
