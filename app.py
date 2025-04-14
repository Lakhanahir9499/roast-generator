from flask import Flask, render_template, request, jsonify
import openai
import os
from gtts import gTTS
import base64
from io import BytesIO

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    name = data.get("name")
    mood = data.get("mood")

    prompt = f"Tum ek savage comedian ho. Kisi ka naam hai '{name}'. Uske liye ek {mood} roast likho jo Hindi aur Desi style mein ho, funny ho, aur halka CarryMinati ya roast content jaisa lage."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        roast = response["choices"][0]["message"]["content"].strip()

        tts = gTTS(text=roast, lang='hi')
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')

        return jsonify({"roast": roast, "audio": audio_base64})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
