from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wb99-universal-esp32-testing-platform'

# Initialize SocketIO with CORS enabled for universal access
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    """Serve the live debugging dashboard"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({"status": "ok"})

@app.route('/api/live-data', methods=['POST'])
def receive_live_data():
    """
    UNIVERSAL INGESTION ENDPOINT
    Accepts ANY payload format:
    - JSON
    - Plain text
    - CSV
    - Binary-like
    - Malformed data
    - Unknown formats
    
    This is a discovery platform - we capture EVERYTHING.
    """
    
    # Capture timestamp
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    # Capture raw body data
    raw_body = request.get_data(as_text=True)
    
    # Capture headers
    headers = dict(request.headers)
    
    # Capture content type
    content_type = request.content_type or 'unknown'
    
    # Capture method
    method = request.method
    
    # Try to parse as JSON (safely)
    parsed_json = None
    json_parse_error = None
    
    try:
        parsed_json = request.get_json(force=True, silent=False)
    except Exception as e:
        json_parse_error = str(e)
    
    # Build comprehensive payload inspection object
    inspection_data = {
        'timestamp': timestamp,
        'method': method,
        'content_type': content_type,
        'headers': headers,
        'raw_body': raw_body,
        'parsed_json': parsed_json,
        'json_parse_error': json_parse_error,
        'body_length': len(raw_body) if raw_body else 0
    }
    
    # Print EVERYTHING to terminal for debugging
    print("\n" + "="*80)
    print(f"[WB99 INGESTION] {timestamp}")
    print("="*80)
    print(f"Method: {method}")
    print(f"Content-Type: {content_type}")
    print(f"Body Length: {inspection_data['body_length']} bytes")
    print("-"*80)
    print("HEADERS:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
    print("-"*80)
    print("RAW BODY:")
    print(raw_body)
    print("-"*80)
    if parsed_json:
        print("PARSED JSON:")
        print(json.dumps(parsed_json, indent=2))
    else:
        print(f"JSON PARSE FAILED: {json_parse_error}")
    print("="*80 + "\n")
    
    # Broadcast to all connected clients via Socket.IO
    socketio.emit('new_data', inspection_data, broadcast=True)
    
    # Always return success - never crash on malformed data
    return jsonify({
        "status": "received",
        "timestamp": timestamp,
        "message": "Data captured and broadcast successfully"
    }), 200

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"[WB99] Client connected: {request.sid}")
    emit('connection_status', {'status': 'connected', 'message': 'Connected to WB99 platform'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"[WB99] Client disconnected: {request.sid}")

if __name__ == '__main__':
    # Run with eventlet for production-like behavior
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
