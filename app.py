from flask import Flask, render_template, request
from waf import analyze_request
from datetime import datetime
import json
from pathlib import Path

app = Flask(__name__)

LOG_FILE = Path("logs/request_log.json")


def load_history():
    if not LOG_FILE.exists():
        return []

    try:
        with LOG_FILE.open("r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    LOG_FILE.parent.mkdir(exist_ok=True)

    with LOG_FILE.open("w") as file:
        json.dump(history, file, indent=4)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    submitted_request = ""

    request_history = load_history()

    if request.method == "POST":
        submitted_request = request.form.get("request_data", "")
        result = analyze_request(submitted_request)

        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "payload": submitted_request,
            "status": result["status"],
            "attack": result["attack"] or "None",
        }

        request_history.insert(0, entry)

        save_history(request_history)

    total_requests = len(request_history)

    blocked_requests = sum(
        1
        for entry in request_history
        if entry["status"] == "BLOCKED"
    )

    allowed_requests = sum(
        1
        for entry in request_history
        if entry["status"] == "ALLOWED"
    )

    return render_template(
        "index.html",
        result=result,
        submitted_request=submitted_request,
        total_requests=total_requests,
        blocked_requests=blocked_requests,
        allowed_requests=allowed_requests,
        request_history=request_history[:10],
    )


if __name__ == "__main__":
    app.run(debug=True)
