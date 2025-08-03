from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)

# Use a smaller model for free-tier memory limits
summarizer = pipeline("summarization", model="t5-small")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("article", "")
    length = data.get("length", "medium")

    if text and len(text.split()) > 50:
        # Truncate input to avoid out-of-memory
        if len(text.split()) > 400:
            text = " ".join(text.split()[:400])

        if length == "short":
            max_len, min_len = 60, 20
        elif length == "long":
            max_len, min_len = 200, 80
        else:
            max_len, min_len = 130, 30

        try:
            result = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
            summary = result[0]['summary_text']
        except Exception as e:
            summary = f"⚠️ Summarization failed: {str(e)}"

        return jsonify({"summary": summary})
    else:
        return jsonify({"summary": "Please enter at least 50 words."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
