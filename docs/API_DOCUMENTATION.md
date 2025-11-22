# API Documentation

Base URL: `http://localhost:8000/api`

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Endpoints

### 1. Get All Dishes

Retrieve all dishes from the database with timestamps.

**Endpoint:** `GET /api/dishes`

**Request:**
```http
GET /api/dishes HTTP/1.1
Host: localhost:8000
```

**Response:** `200 OK`
```json
[
  {
    "dishId": 1,
    "dishName": "Pizza Margherita",
    "imageUrl": "https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=400",
    "isPublished": true,
    "createdAt": "2025-11-22T10:00:00.000Z",
    "updatedAt": "2025-11-22T10:00:00.000Z"
  },
  {
    "dishId": 2,
    "dishName": "Sushi Platter",
    "imageUrl": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400",
    "isPublished": false,
    "createdAt": "2025-11-22T10:00:00.000Z",
    "updatedAt": "2025-11-22T10:00:00.000Z"
  }
]
```

**Error Response:** `500 Internal Server Error`
```json
{
  "error": "Failed to fetch dishes"
}
```

---

### 2. Toggle Dish Status

Toggle the `isPublished` status of a specific dish.

**Endpoint:** `PATCH /api/dishes/{id}/toggle`

**Parameters:**
- `id` (path parameter): The dish ID (integer) to toggle

**Request:**
```http
PATCH /api/dishes/1/toggle HTTP/1.1
Host: localhost:8000
```

**Response:** `200 OK`
```json
{
  "dishId": 1,
  "dishName": "Pizza Margherita",
  "imageUrl": "https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=400",
  "isPublished": false,
  "createdAt": "2025-11-22T10:00:00.000Z",
  "updatedAt": "2025-11-22T10:30:00.000Z"
}
```

**Error Responses:**

`404 Not Found`
```json
{
  "error": "Dish not found"
}
```

`500 Internal Server Error`
```json
{
  "error": "Failed to toggle dish status"
}
```

---

## WebSocket Endpoint

### Endpoint: `ws://localhost:8000/ws`

Real-time updates endpoint using native WebSocket protocol.

**Connection:**
```javascript
const socket = new WebSocket('ws://localhost:8000/ws');

socket.onopen = () => {
  console.log('WebSocket connected');
};

socket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};
```

### Message: `dishStatusChanged`

Broadcast to all connected clients when any dish status is toggled.

**Message Structure:**
```json
{
  "type": "dishStatusChanged",
  "data": {
    "dishId": 1,
    "dishName": "Pizza Margherita",
    "imageUrl": "https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=400",
    "isPublished": false
  }
}
```

**React Hook Example:**
```javascript
import { useEffect, useState } from 'react';

export const useWebSocket = (url, onMessage) => {
  const [isConnected, setIsConnected] = useState(false);
  
  useEffect(() => {
    const ws = new WebSocket(url);
    
    ws.onopen = () => setIsConnected(true);
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      onMessage(message);
    };
    ws.onclose = () => setIsConnected(false);
    
    return () => ws.close();
  }, [url, onMessage]);
  
  return { isConnected };
};
```

---

## Error Handling

All API errors follow this structure:

```json
{
  "error": "Error message description"
}
```

**HTTP Status Codes:**
- `200` - Success
- `404` - Resource not found
- `500` - Server error

---

## Rate Limiting

Currently no rate limiting implemented. Recommended for production:
- 100 requests per 15 minutes per IP

---

## CORS Policy

**Allowed Origins (Development):**
```python
allow_origins=[
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative frontend
]
allow_methods=["*"]
allow_headers=["*"]
```

**Production:** Configure specific domain origins in environment variables

---

## Authentication

Currently no authentication required. For production, consider:
- JWT tokens
- API keys
- OAuth 2.0

---

## Testing with cURL

**Get all dishes:**
```bash
curl http://localhost:8000/api/dishes
```

**Toggle dish status:**
```bash
curl -X PATCH http://localhost:8000/api/dishes/1/toggle
```

**Test WebSocket (using websocat):**
```bash
websocat ws://localhost:8000/ws
```

---

## Testing with Python

**Using requests library:**
```python
import requests

# Get all dishes
response = requests.get('http://localhost:8000/api/dishes')
print(response.json())

# Toggle dish status
response = requests.patch('http://localhost:8000/api/dishes/1/toggle')
print(response.json())
```

**Using websockets library:**
```python
import asyncio
import websockets
import json

async def test_websocket():
    async with websockets.connect('ws://localhost:8000/ws') as websocket:
        message = await websocket.recv()
        print(f"Received: {json.loads(message)}")

asyncio.run(test_websocket())
```

---

**API Version:** 2.0  
**Framework:** FastAPI 0.104.1  
**Last Updated:** November 23, 2025  
**Author:** Vasanthakumar V
