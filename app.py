import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # allow requests from Moodle/browser

# IMPORTANT: no key here, we will add it later in Render
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/ping")
def ping():
    return jsonify({"status": "ok"})

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    question = (data.get("message") or "").strip()
    if not question:
        return jsonify({"error": "No message received"}), 400

    try:
        resp = client.responses.create(
            model="gpt-5-mini",
            input=[
                {"role": "system", "content": "You are a patient tutor for Integrated Electronics."},
                {"role": "system", "content": "Format neatly with short paragraphs, bullet points, and line breaks."},
                {"role": "system", "content": "If off-topic, reply exactly: Sorry I cannot help you with that, I can only answer questions about Integrated Electronics."},
                {"role": "user", "content": question}
            ],
        )
        return jsonify({"reply": resp.output_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
