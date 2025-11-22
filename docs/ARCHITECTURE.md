# System Architecture

## Overview

The Dish Management System is a full-stack application built with a three-tier architecture:

1. **Presentation Layer** (Frontend - React)
2. **Application Layer** (Backend - Node.js/Express)
3. **Data Layer** (PostgreSQL Database)

With real-time communication powered by Socket.io.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT TIER                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │         React Frontend (Port 5173)                  │     │
│  │  - Dashboard UI                                     │     │
│  │  - Dish Cards with Toggle Buttons                   │     │
│  │  - Socket.io Client                                 │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/HTTPS
                            │ WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION TIER                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │    Node.js + Express Server (Port 5000)            │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  REST API Routes                          │     │     │
│  │  │  - GET /api/dishes                        │     │     │
│  │  │  - PATCH /api/dishes/:id/toggle           │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  Socket.io Server                         │     │     │
│  │  │  - Broadcasts: dishStatusChanged          │     │     │
│  │  └──────────────────────────────────────────┘     │     │
│  │  ┌──────────────────────────────────────────┐     │     │
│  │  │  Business Logic                           │     │     │
│  │  │  - Dish Controller                        │     │     │
│  │  │  - Validation & Error Handling            │     │     │
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

### Backend: Node.js + Express
- **Why:** Non-blocking I/O perfect for real-time applications
- **Benefits:** Fast, scalable, same language as frontend (JavaScript)
- **Alternatives considered:** Python (Flask/Django), Java (Spring Boot)

### Database: PostgreSQL
- **Why:** ACID compliance, reliability, excellent for structured data
- **Benefits:** Strong data integrity, JSON support, free & open-source
- **Alternatives considered:** MySQL, MongoDB (NoSQL)

### ORM: Sequelize
- **Why:** Mature ORM with TypeScript support, migrations, and validation
- **Benefits:** Abstract SQL queries, auto-migrations, model validation
- **Alternatives considered:** Prisma, TypeORM

### Real-time: Socket.io
- **Why:** Industry standard for WebSocket communication with fallbacks
- **Benefits:** Auto-reconnection, room support, broad browser compatibility
- **Alternatives considered:** Native WebSockets, Server-Sent Events (SSE)

### Frontend: React + Vite
- **Why:** Component-based architecture, fast HMR with Vite
- **Benefits:** Virtual DOM, huge ecosystem, excellent dev experience
- **Alternatives considered:** Vue.js, Angular, Svelte

## Data Flow

### 1. Fetch Dishes (GET Request)
```
Client → HTTP GET /api/dishes → Express Router → Controller 
→ Sequelize ORM → PostgreSQL → Response JSON → Client renders
```

### 2. Toggle Dish Status (PATCH Request)
```
Client → HTTP PATCH /api/dishes/:id/toggle → Express Router 
→ Controller → Update DB → Socket.io broadcast → All clients update UI
```

### 3. Real-Time Update Flow
```
Backend DB Change → Trigger Event → Socket.io Server 
→ Emit 'dishStatusChanged' → All Connected Clients → UI Update
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

### Socket.io Communication

**Connection Flow:**
```
1. Client connects → Socket.io handshake
2. Server assigns socket ID
3. Client listens to 'dishStatusChanged' event
4. On dish toggle → Server emits to all sockets
5. Clients update UI without page refresh
```

**Event Schema:**
```javascript
{
  eventName: 'dishStatusChanged',
  payload: {
    dishId: 1,
    isPublished: false,
    timestamp: '2025-11-22T10:30:00Z'
  }
}
```

## Deployment Architecture

### Development
```
localhost:5173 (Frontend) → localhost:5000 (Backend) → localhost:5432 (PostgreSQL)
```

### Production (Recommended)
```
Vercel/Netlify (Frontend) → Railway/Render (Backend) → Managed PostgreSQL
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

1. **Unit Tests:** Jest for backend logic
2. **Integration Tests:** Supertest for API endpoints
3. **E2E Tests:** Playwright for full user flows
4. **Real-time Tests:** Socket.io-client for WebSocket testing

## Development Workflow

```
1. Feature Branch → Development → Testing → Main Branch
2. Local testing with hot reload
3. Database migrations managed by Sequelize
4. Seed data for consistent dev environment
```

---

**Document Version:** 1.0  
**Last Updated:** November 22, 2025  
**Author:** Vasanth
