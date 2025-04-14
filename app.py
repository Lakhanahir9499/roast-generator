from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from io import BytesIO
import base64
import openai
import random

app = Flask(__name__)
openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_roast(name, mood):
    prompt = f"{name} ke liye ek {mood} mood me hindi-desi mix roast likho."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    name = data.get("name")
    mood = data.get("mood")
    roast = generate_roast(name, mood)

    # Voice
    tts = gTTS(roast, lang='hi')
    voice = BytesIO()
    tts.write_to_fp(voice)
    voice.seek(0)
    voice_base64 = base64.b64encode(voice.read()).decode("utf-8")

    # Dummy meme (static image for now)
    meme_url = f"https://api.memegen.link/images/custom/{name}_roasted.png?background=https://i.imgflip.com/1bij.jpg&text={roast.replace(' ', '_')}"

    return jsonify({
        "roast": roast,
        "voice": voice_base64,
        "meme": meme_url
    })

if __name__ == "__main__":
    app.run(debug=True)
