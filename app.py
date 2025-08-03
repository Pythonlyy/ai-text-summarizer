from flask import Flask, render_template, request, jsonify
import requests, os

app = Flask(__name__)
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_API_TOKEN = os.environ.get("HF_TOKEN")  # store your token in Render environment variables

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("article", "")
    length = data.get("length", "medium")

    if not text or len(text.split()) < 50:
        return jsonify({"summary": "Please enter at least 50 words."})

    payload = {"inputs": text, "parameters": {"max_length": 130, "min_length": 30}}
    response = requests.post(HF_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        summary = response.json()[0]['summary_text']
    else:
        summary = f"Error from Hugging Face API: {response.text}"

    return jsonify({"summary": summary})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
