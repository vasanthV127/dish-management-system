# System Architecture

## Overview

The Dish Management System is a full-stack application built with a three-tier architecture:

1. **Presentation Layer** (Frontend - React + Vite)
2. **Application Layer** (Backend - FastAPI + Python)
3. **Data Layer** (PostgreSQL Database)

With real-time communication powered by native WebSockets.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT TIER                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │         React Frontend (Port 5173)                  │     │
│  │  - Dashboard UI with Tailwind CSS                   │     │
│  │  - Dish Cards with Toggle Buttons                   │     │
│  │  - Native WebSocket Client                          │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/HTTPS
                            │ WebSocket (ws://)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION TIER                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │    FastAPI + Uvicorn Server (Port 8000)            │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  REST API Routes                          │     │     │
│  │  │  - GET /api/dishes                        │     │     │
│  │  │  - PATCH /api/dishes/{id}/toggle          │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  WebSocket Endpoint                       │     │     │
│  │  │  - ws://localhost:8000/ws                 │     │     │
│  │  │  - ConnectionManager broadcasts updates   │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  Business Logic                           │     │     │
│  │  │  - CRUD Operations (crud.py)              │     │     │
│  │  │  - Pydantic Validation (schemas.py)       │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │ SQL Queries
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         DATA TIER                            │
│  ┌────────────────────────────────────────────────────┐     │
│  │         PostgreSQL Database                         │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  dishes Table                             │     │     │
│  │  │  - dishId (PK, SERIAL)                    │     │     │
│  │  │  - dishName (VARCHAR)                     │     │     │
│  │  │  - imageUrl (TEXT)                        │     │     │
│  │  │  - isPublished (BOOLEAN)                  │     │     │
│  │  │  - createdAt (TIMESTAMP)                  │     │     │
│  │  │  - updatedAt (TIMESTAMP)                  │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Technology Choices & Rationale

### Backend: FastAPI (Python 3.12)
- **Why:** Modern async framework, automatic API documentation, type safety
- **Benefits:** Fast performance, built-in validation, excellent async support
- **Alternatives considered:** Flask, Django, Node.js (Express)

### Database: PostgreSQL
- **Why:** ACID compliance, reliability, excellent for structured data
- **Benefits:** Strong data integrity, JSON support, free & open-source
- **Alternatives considered:** MySQL, MongoDB (NoSQL)

### ORM: SQLAlchemy
- **Why:** Most mature Python ORM, excellent async support
- **Benefits:** Powerful query builder, declarative models, migration support
- **Alternatives considered:** Tortoise ORM, Peewee

### Real-time: Native WebSockets
- **Why:** FastAPI has built-in WebSocket support, no extra dependencies
- **Benefits:** Lower overhead, direct protocol implementation, simpler setup
- **Alternatives considered:** Socket.io (requires additional library), Server-Sent Events (SSE)

### Frontend: React 18 + Vite
- **Why:** Component-based architecture, fast HMR with Vite
- **Benefits:** Virtual DOM, huge ecosystem, excellent dev experience
- **Alternatives considered:** Vue.js, Angular, Svelte

### Styling: Tailwind CSS
- **Why:** Utility-first CSS framework for rapid UI development
- **Benefits:** No custom CSS needed, consistent design, small bundle size
- **Alternatives considered:** Bootstrap, Material-UI, styled-components

## Data Flow

### 1. Fetch Dishes (GET Request)
```
Client → HTTP GET /api/dishes → FastAPI Route → CRUD Function
→ SQLAlchemy ORM → PostgreSQL → Pydantic Schema → JSON Response → Client renders
```

### 2. Toggle Dish Status (PATCH Request)
```
Client → HTTP PATCH /api/dishes/{id}/toggle → FastAPI Route
→ CRUD Update → PostgreSQL → WebSocket Broadcast → All clients update UI
```

### 3. Real-Time Update Flow
```
Backend DB Change → ConnectionManager.broadcast() → WebSocket Server
→ Send JSON to all connections → All Connected Clients → UI Update
```

## Database Schema

### dishes Table

| Column      | Type         | Constraints        | Description                    |
|-------------|--------------|--------------------|--------------------------------|
| dishId      | SERIAL       | PRIMARY KEY        | Unique identifier              |
| dishName    | VARCHAR(255) | NOT NULL           | Name of the dish               |
| imageUrl    | TEXT         | NOT NULL           | URL to dish image              |
| isPublished | BOOLEAN      | DEFAULT FALSE      | Publication status             |
| createdAt   | TIMESTAMP    | DEFAULT NOW()      | Record creation time           |
| updatedAt   | TIMESTAMP    | DEFAULT NOW()      | Last update time               |

**Indexes:**
- Primary key on `dishId` (auto-created)
- Optional: Index on `isPublished` for faster filtering

## API Design

### RESTful Principles
- Uses standard HTTP methods (GET, PATCH)
- Resource-based URLs (`/api/dishes`)
- Stateless communication
- JSON response format

### Error Handling
```javascript
{
  "error": "Error message",
  "status": 400/404/500
}
```

### Success Response
```javascript
{
  "dishId": 1,
  "dishName": "Pizza",
  "imageUrl": "...",
  "isPublished": true
}
```

## Security Considerations

1. **CORS:** Configured to allow frontend origin
2. **Input Validation:** Validate dish IDs and request bodies
3. **SQL Injection:** Protected via Sequelize parameterized queries
4. **Environment Variables:** Sensitive data in `.env` file
5. **Rate Limiting:** (Optional) Can add with `express-rate-limit`

## Scalability

### Current Setup (Single Server)
- Suitable for 100-1000 concurrent users
- Single database instance

### Future Improvements
1. **Load Balancing:** Multiple backend instances behind Nginx
2. **Database Replication:** Read replicas for scaling reads
3. **Caching:** Redis for frequently accessed dishes
4. **CDN:** Serve images from CloudFront/Cloudflare
5. **Microservices:** Split into dish-service, notification-service

## Real-Time Architecture

### Native WebSocket Communication

**Connection Flow:**
```
1. Client connects → ws://localhost:8000/ws
2. WebSocket handshake completes
3. ConnectionManager stores active connection
4. Client listens for incoming messages
5. On dish toggle → Server broadcasts to all connections
6. Clients parse JSON and update UI without page refresh
```

**Message Schema:**
```javascript
{
  "type": "dishStatusChanged",
  "data": {
    "dishId": 1,
    "dishName": "Pizza Margherita",
    "imageUrl": "https://images.unsplash.com/...",
    "isPublished": false
  }
}
```

**ConnectionManager Class:**
```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)
```

## Deployment Architecture

### Development
```
localhost:5173 (Frontend) → localhost:8000 (Backend) → localhost:5432 (PostgreSQL)
                             ws://localhost:8000/ws (WebSocket)
```

### Production (Recommended)
```
Vercel/Netlify (Frontend) → Railway/Render (Backend FastAPI) → Managed PostgreSQL
                             wss://api.domain.com/ws (Secure WebSocket)
```

## Performance Optimization

1. **Frontend:**
   - Lazy loading components
   - Image optimization (WebP format)
   - Debounce toggle button clicks

2. **Backend:**
   - Connection pooling for database
   - Gzip compression for responses
   - Efficient SQL queries with indexes

3. **Database:**
   - Query optimization
   - Proper indexing
   - Regular VACUUM operations

## Monitoring & Logging

**Development:**
- Console logs for debugging
- Sequelize query logging

**Production (Recommended):**
- Winston/Pino for structured logging
- PM2 for process management
- Sentry for error tracking
- PostgreSQL slow query log

## Testing Strategy

1. **Unit Tests:** pytest for backend logic and CRUD operations
2. **Integration Tests:** TestClient (FastAPI) for API endpoints
3. **E2E Tests:** Playwright for full user flows
4. **Real-time Tests:** websockets library for WebSocket testing

## Development Workflow

```
1. Feature Branch → Development → Testing → Main Branch
2. Local testing with hot reload
3. Database migrations managed by Sequelize
4. Seed data for consistent dev environment
```

---

**Document Version:** 2.0  
**Last Updated:** November 23, 2025  
**Author:** Vasanthakumar V
