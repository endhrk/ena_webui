import argparse
import json
from pathlib import Path

import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

CHAPTER_DIR = Path("chapters")
CHAPTER_DIR.mkdir(exist_ok=True)


def call_kobold(kobold_url: str, prompt: str) -> str:
    payload = {"prompt": prompt}
    try:
        response = requests.post(kobold_url, json=payload, timeout=60)
        response.raise_for_status()
    except requests.RequestException as exc:
        return f"Error: {exc}"
    data = response.json()
    # Expecting structure {"results": [{"text": "..."}]}
    return data.get("results", [{}])[0].get("text", "")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.json.get("prompt", "")
    kobold_url = app.config["KOBOLD_URL"]
    text = call_kobold(kobold_url, prompt)
    return jsonify({"text": text})


@app.route("/save", methods=["POST"])
def save():
    title = request.json.get("title", "chapter")
    text = request.json.get("text", "")
    safe_title = "_".join(title.split())
    path = CHAPTER_DIR / f"{safe_title}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"title": title, "text": text}, f, ensure_ascii=False, indent=2)
    return jsonify({"message": f"Saved {path.name}"})


def parse_args():
    parser = argparse.ArgumentParser(description="ENA webui")
    parser.add_argument("--host", default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, default=5000, help="Port number")
    parser.add_argument(
        "--kobold-url",
        default="http://localhost:5001/api/v1/generate",
        help="KoboldCpp API URL",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    app.config["KOBOLD_URL"] = args.kobold_url
    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
