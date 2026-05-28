from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime, timezone
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wb99-secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/api/live-data', methods=['POST'])
def live_data():
    timestamp = datetime.now(timezone.utc).isoformat()
    raw_body = request.get_data(as_text=True)
    headers = dict(request.headers)
    content_type = request.content_type or 'unknown'

    parsed_json = None
    parse_error = None
    try:
        parsed_json = request.get_json(force=True, silent=False)
    except Exception as e:
        parse_error = str(e)

    payload = {
        'timestamp': timestamp,
        'method': request.method,
        'content_type': content_type,
        'body_length': len(raw_body) if raw_body else 0,
        'raw_body': raw_body,
        'parsed_json': parsed_json,
        'parse_error': parse_error,
        'headers': headers,
    }

    print("\n" + "=" * 80)
    print(f"[WB99] {timestamp}")
    print(f"Content-Type : {content_type}")
    print(f"Body Length  : {payload['body_length']} bytes")
    print("--- HEADERS ---")
    for k, v in headers.items():
        print(f"  {k}: {v}")
    print("--- RAW BODY ---")
    print(raw_body if raw_body else "(empty)")
    if parsed_json is not None:
        print("--- PARSED JSON ---")
        print(json.dumps(parsed_json, indent=2))
    else:
        print(f"--- JSON PARSE ERROR: {parse_error} ---")
    print("=" * 80 + "\n")

    socketio.emit('new_data', payload)

    return jsonify({"status": "received", "timestamp": timestamp}), 200


@socketio.on('connect')
def on_connect():
    print(f"[WB99] Client connected: {request.sid}")
    emit('connection_status', {'status': 'connected'})


@socketio.on('disconnect')
def on_disconnect():
    print(f"[WB99] Client disconnected: {request.sid}")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
