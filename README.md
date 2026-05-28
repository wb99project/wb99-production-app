# WB99 - Realtime ESP32 Testing Platform

WB99 is a minimal realtime JSON ingestion engine built with Flask and Flask-SocketIO.
It is designed to receive any JSON payload from an ESP32, broadcast it instantly, and show live updates in the browser.

## Features

- Accepts any JSON payload dynamically
- No strict schema validation
- Supports nested and evolving payload structures
- Realtime updates via Socket.IO
- Render deployment ready

## Local Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - macOS / Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app locally:
   ```bash
   python app.py
   ```

5. Open your browser:
   ```
   http://localhost:5000
   ```

## GitHub Push

1. Initialize Git if needed:
   ```bash
   git init
   ```

2. Add files and commit:
   ```bash
   git add .
   git commit -m "Initial WB99 realtime ESP32 platform"
   ```

3. Add your remote repository and push:
   ```bash
   git remote add origin https://github.com/<your-user>/<your-repo>.git
   git branch -M main
   git push -u origin main
   ```

## Render Deployment

1. Create a Render account and connect your GitHub repository.
2. Create a new Web Service and select the WB99 repository.
3. Set the start command to:
   ```bash
   gunicorn -k eventlet -w 1 app:app
   ```
4. Deploy the service.
5. After deployment, use the public Render URL in your ESP32 code.

## Render Endpoint Example

Use this endpoint for ESP32 data ingestion:

```text
https://your-app.onrender.com/api/live-data
```

## API Endpoints

- `GET /` - Dashboard UI
- `GET /health` - Health check
- `POST /api/live-data` - Accepts any JSON payload and broadcasts it via Socket.IO

## Socket.IO Event

- `new_data` - Emitted for every incoming payload

## Example ESP32 Payloads

The backend supports arbitrary payloads, including nested JSON:

```json
{
  "pitch": 10,
  "yaw": 5
}
```

```json
{
  "mode": "scan",
  "temperature": 36.5
}
```

```json
{
  "sensor1": 10,
  "sensor2": 20,
  "nested": {
    "x": 1
  }
}
```

