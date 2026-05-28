# WB99 - Universal ESP32 Testing & Payload Discovery Platform

**WB99** is a universal realtime ingestion engine designed for ESP32 payload discovery, protocol inspection, and debugging. It accepts **ANY** data format and displays everything in realtime.

## 🎯 Purpose

This is **NOT** production software. This is a **testing and discovery platform** for:

- ✅ ESP32 payload discovery
- ✅ Protocol inspection
- ✅ Realtime debugging
- ✅ Format testing
- ✅ Universal data ingestion

## 🚀 Key Features

### Universal Ingestion
Accepts **ANY** payload format:
- ✅ JSON (valid or malformed)
- ✅ Plain text
- ✅ CSV-like strings
- ✅ Binary-like content
- ✅ Unknown formats
- ✅ Nested structures
- ✅ Form data
- ✅ Empty payloads

### Realtime Monitoring
- Live Socket.IO updates
- Instant payload inspection
- Connection status tracking
- Auto-reconnect support

### Complete Inspection
Displays everything received:
- Raw body content
- Parsed JSON (if valid)
- All headers
- Content-Type
- Timestamp
- Body length
- Parse errors

### Never Crashes
- Safe JSON parsing with fallback
- Handles malformed data gracefully
- Always returns success response
- Comprehensive error logging

## 📁 Project Structure

```
wb99/
│
├── app.py                  # Flask backend with universal ingestion
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment config
├── README.md              # This file
├── .gitignore             # Git ignore rules
│
├── templates/
│   └── index.html         # Live debugging dashboard
│
└── static/
    ├── css/
    └── js/
```

## 🛠️ Local Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Locally

```bash
python app.py
```

### 5. Open Dashboard

```
http://localhost:5000
```

You should see the live debugging dashboard with connection status.

## 🌐 GitHub Push

### Initialize Git (if needed)

```bash
git init
git add .
git commit -m "Initial WB99 universal ESP32 testing platform"
```

### Push to GitHub

```bash
git remote add origin https://github.com/<your-username>/<your-repo>.git
git branch -M main
git push -u origin main
```

## ☁️ Render Deployment

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up or log in
3. Connect your GitHub account

### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your WB99 repository
3. Configure:
   - **Name:** `wb99` (or your choice)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -k eventlet -w 1 app:app`

### Step 3: Deploy
1. Click **"Create Web Service"**
2. Wait for deployment to complete
3. Copy your public URL: `https://your-app.onrender.com`

### Step 4: Test
Open your Render URL in a browser to see the dashboard.

## 📡 API Endpoints

### `GET /`
Live debugging dashboard UI

### `GET /health`
Health check endpoint
```json
{
  "status": "ok"
}
```

### `POST /api/live-data`
**Universal ingestion endpoint** - accepts ANY payload format

**Example URL:**
```
https://your-app.onrender.com/api/live-data
```

**Response:**
```json
{
  "status": "received",
  "timestamp": "2026-05-28T10:30:00.000Z",
  "message": "Data captured and broadcast successfully"
}
```

## 🔌 ESP32 Testing Instructions

### Example 1: JSON Payload

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* serverUrl = "https://your-app.onrender.com/api/live-data";

void sendData() {
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  
  String payload = "{\"pitch\":12,\"yaw\":5}";
  int httpCode = http.POST(payload);
  
  Serial.println("Response: " + String(httpCode));
  http.end();
}
```

### Example 2: Plain Text

```cpp
void sendData() {
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "text/plain");
  
  String payload = "temp=36.5";
  int httpCode = http.POST(payload);
  
  Serial.println("Response: " + String(httpCode));
  http.end();
}
```

### Example 3: CSV-like Data

```cpp
void sendData() {
  HTTPClient http;
  http.begin(serverUrl);
  
  String payload = "12,55,66";
  int httpCode = http.POST(payload);
  
  Serial.println("Response: " + String(httpCode));
  http.end();
}
```

### Example 4: Nested JSON

```cpp
void sendData() {
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  
  String payload = "{\"gyro\":{\"x\":1,\"y\":2},\"mode\":\"scan\"}";
  int httpCode = http.POST(payload);
  
  Serial.println("Response: " + String(httpCode));
  http.end();
}
```

## 📊 What Gets Displayed

When ESP32 sends data, the dashboard shows:

1. **Connection Status** - Live connection state
2. **Request Metadata:**
   - Timestamp
   - HTTP method
   - Content-Type
   - Body length
3. **Raw Body** - Exact bytes received
4. **Parsed JSON** - If payload is valid JSON
5. **Headers** - All HTTP headers
6. **Parse Errors** - If JSON parsing fails

## 🧪 Testing Different Formats

The platform supports testing with:

| Format | Example | Result |
|--------|---------|--------|
| Valid JSON | `{"temp":36}` | Parsed + Raw displayed |
| Malformed JSON | `{temp:36}` | Parse error + Raw displayed |
| Plain text | `temperature=36` | Raw displayed |
| CSV | `12,55,66` | Raw displayed |
| Empty | `` | Empty body message |
| Binary-like | `\x01\x02\x03` | Raw displayed |

## 🔍 Terminal Logging

All received data is logged to terminal with full details:

```
================================================================================
[WB99 INGESTION] 2026-05-28T10:30:00.000Z
================================================================================
Method: POST
Content-Type: application/json
Body Length: 25 bytes
--------------------------------------------------------------------------------
HEADERS:
  Host: your-app.onrender.com
  Content-Type: application/json
  Content-Length: 25
--------------------------------------------------------------------------------
RAW BODY:
{"pitch":12,"yaw":5}
--------------------------------------------------------------------------------
PARSED JSON:
{
  "pitch": 12,
  "yaw": 5
}
================================================================================
```

## 🔄 Socket.IO Events

### Client → Server
- `connect` - Client connects to server
- `disconnect` - Client disconnects

### Server → Client
- `connection_status` - Connection confirmation
- `new_data` - New payload received (broadcasts to all clients)

## ⚠️ Important Notes

### This is NOT:
- ❌ Production medical software
- ❌ A database system
- ❌ An authentication platform
- ❌ A reporting system
- ❌ Final implementation

### This IS:
- ✅ A testing platform
- ✅ A payload discovery tool
- ✅ A protocol inspector
- ✅ A debugging dashboard
- ✅ A universal ingestion engine

## 🛡️ Security Note

This platform has **NO authentication** and accepts **ANY data**. It is designed for:
- Development testing
- Protocol discovery
- ESP32 debugging

**Do NOT:**
- Use in production
- Send sensitive data
- Expose to untrusted networks
- Store received data permanently

## 📝 Dependencies

- **Flask** - Web framework
- **Flask-SocketIO** - Realtime communication
- **eventlet** - Async server
- **gunicorn** - Production WSGI server

## 🐛 Troubleshooting

### Dashboard not updating?
- Check browser console for Socket.IO errors
- Verify connection status shows "CONNECTED"
- Check Render logs for backend errors

### ESP32 not connecting?
- Verify WiFi connection
- Check server URL is correct
- Ensure HTTPS (not HTTP) for Render
- Check ESP32 serial monitor for HTTP response codes

### Render deployment failing?
- Verify `Procfile` exists
- Check `requirements.txt` is complete
- Review Render build logs
- Ensure Python 3 environment selected

## 📄 License

This is a testing platform for development purposes.

## 🤝 Contributing

This is a discovery platform. Modify as needed for your testing requirements.

---

**WB99** - Universal ESP32 Testing Platform
*Receive anything. Display everything.*

