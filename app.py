import json
import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/live-data", methods=["POST"])
def live_data():
    payload = request.get_json(force=True, silent=True)

    if payload is None:
        raw_payload = request.get_data(as_text=True)
        try:
            payload = json.loads(raw_payload) if raw_payload else {}
        except ValueError:
            payload = raw_payload or {}

    print("Received live data:", payload)
    socketio.emit("new_data", payload, broadcast=True)
    return jsonify({"success": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
