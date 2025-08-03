from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load summarizer model once at startup
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
        if length == "short":
            max_len, min_len = 60, 20
        elif length == "long":
            max_len, min_len = 200, 80
        else:
            max_len, min_len = 130, 30

        result = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
        summary = result[0]['summary_text']
        return jsonify({"summary": summary})
    else:
        return jsonify({"summary": "Please enter at least 50 words."})

if __name__ == "__main__":
    app.run(debug=True)
