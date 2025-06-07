from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    lang = request.json.get("lang", "en")

    system_prompt = {
        "en": "You are a helpful AI assistant who replies in English.",
        "hi": "आप एक सहायक AI हैं जो हिंदी में उत्तर देता है।"
    }.get(lang, "You are a helpful AI assistant.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)