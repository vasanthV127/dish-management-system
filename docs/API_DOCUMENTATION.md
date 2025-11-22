# API Documentation

Base URL: `http://localhost:5000/api`

## Endpoints

### 1. Get All Dishes

Retrieve all dishes from the database.

**Endpoint:** `GET /api/dishes`

**Request:**
```http
GET /api/dishes HTTP/1.1
Host: localhost:5000
```

**Response:** `200 OK`
```json
[
  {
    "dishId": 1,
    "dishName": "Pizza Margherita",
    "imageUrl": "https://example.com/pizza.jpg",
    "isPublished": true,
    "createdAt": "2025-11-22T10:00:00.000Z",
    "updatedAt": "2025-11-22T10:00:00.000Z"
  },
  {
    "dishId": 2,
    "dishName": "Pasta Carbonara",
    "imageUrl": "https://example.com/pasta.jpg",
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

**Endpoint:** `PATCH /api/dishes/:id/toggle`

**Parameters:**
- `id` (path parameter): The dish ID to toggle

**Request:**
```http
PATCH /api/dishes/1/toggle HTTP/1.1
Host: localhost:5000
```

**Response:** `200 OK`
```json
{
  "dishId": 1,
  "dishName": "Pizza Margherita",
  "imageUrl": "https://example.com/pizza.jpg",
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

## Socket.io Events

### Event: `dishStatusChanged`

Emitted to all connected clients when any dish status is toggled.

**Event Data:**
```json
{
  "dishId": 1,
  "dishName": "Pizza Margherita",
  "imageUrl": "https://example.com/pizza.jpg",
  "isPublished": false
}
```

**Client-side listener:**
```javascript
socket.on('dishStatusChanged', (dish) => {
  console.log('Dish updated:', dish);
  // Update UI with new dish data
});
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
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative frontend)

**Production:** Configure specific domain origins

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
curl http://localhost:5000/api/dishes
```

**Toggle dish status:**
```bash
curl -X PATCH http://localhost:5000/api/dishes/1/toggle
```

---

## Testing with Postman

1. Import collection from `/postman/dish-management.json`
2. Set base URL to `http://localhost:5000`
3. Test all endpoints

---

**API Version:** 1.0  
**Last Updated:** November 22, 2025
