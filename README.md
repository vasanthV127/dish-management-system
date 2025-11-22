# Dish Management System

Full-stack application for managing and displaying dish information with real-time updates using modern black and white UI design.

## 🚀 Features

- ✅ View all dishes with beautiful images and details
- ✅ Toggle publish/unpublish status with one click
- ✅ **Real-time updates** across all connected clients via WebSocket
- ✅ Modern black & white minimalist design
- ✅ RESTful API with FastAPI
- ✅ Fully responsive dashboard UI
- ✅ Professional typography and animations

## 🛠️ Tech Stack

**Backend:**
- Python 3.12 + FastAPI
- PostgreSQL (Database)
- WebSockets (Real-time)
- SQLAlchemy (ORM)

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- Axios
- WebSocket Client

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app & WebSocket
│   │   ├── database.py     # Database connection
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── crud.py         # Database operations
│   │   ├── config.py       # Environment config
│   │   └── init_db.py      # Database seeding
│   ├── requirements.txt
│   ├── .env
│   └── SETUP_GUIDE.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   └── DishCard.jsx
│   │   ├── hooks/
│   │   │   └── useWebSocket.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── docs/
│   ├── ARCHITECTURE.md
│   └── API_DOCUMENTATION.md
├── README.md
└── SETUP_INSTRUCTIONS.md
```

## 🔧 Setup Instructions

### Prerequisites
- Python (v3.12+)
- PostgreSQL (v14+)
- Node.js (v18+)
- npm
- pgAdmin (optional, for database management)

### Backend Setup

1. Navigate to backend folder:
```powershell
cd backend
```

2. Create and activate virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Create `.env` file:
```powershell
copy .env.example .env
```

5. Update `.env` with your PostgreSQL credentials:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dish_management
DB_USER=postgres
DB_PASSWORD=your_password
PORT=8000
```

6. Create PostgreSQL database using pgAdmin or:
```sql
CREATE DATABASE dish_management;
```

7. Initialize database with sample data:
```powershell
python -m app.init_db
```

8. Start the backend server:
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Server runs on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend folder:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Install Tailwind CSS (if not already installed):
```powershell
npm install -D tailwindcss postcss autoprefixer
```

4. Start the development server:
```powershell
npm run dev
```

Frontend runs on `http://localhost:5173`

## 🎮 Usage

1. Open `http://localhost:5173` in your browser
2. View all dishes in the modern black and white dashboard
3. Click "PUBLISH" or "UNPUBLISH" buttons to toggle dish status
4. Open multiple browser tabs to see instant real-time updates
5. Check the "LIVE" indicator in the header for connection status

> 💡 **Tip:** For detailed setup instructions, see `SETUP_INSTRUCTIONS.md`

## 🧪 Testing Real-Time Updates

To test real-time functionality:

1. Open the dashboard in **two different browser windows** (http://localhost:5173)
2. Toggle a dish status (Publish/Unpublish) in one window
3. **Observe the instant update** in the other window without page refresh
4. Alternatively, update the database directly in pgAdmin:
   ```sql
   UPDATE dishes SET "isPublished" = NOT "isPublished" WHERE "dishId" = 1;
   ```
   Watch the dashboard update automatically!

## 📹 Demo Videos

1. **App Demonstration** (1 minute): Shows the working application with real-time updates
2. **Code Explanation** (1 minute): Explains the architecture and key code components

## 🔌 API Endpoints

### GET /api/dishes
Fetch all dishes

**Response:**
```json
[
  {
    "dishId": 1,
    "dishName": "Pizza Margherita",
    "imageUrl": "https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=400",
    "isPublished": true,
    "createdAt": "2025-11-22T10:00:00.000Z",
    "updatedAt": "2025-11-22T10:00:00.000Z"
  }
]
```

### PATCH /api/dishes/{id}/toggle
Toggle dish published status

**Response:**
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

### WebSocket: ws://localhost:8000/ws
Real-time updates endpoint

**Event: dishStatusChanged**
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

## 🎨 Design Features

- **Modern Black & White Theme**: Professional minimalist design
- **Full Color Images**: Vibrant food photography that stands out
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Live Status Indicator**: Shows real-time connection status
- **Bold Typography**: Clean, readable uppercase headings

## 📦 Deployment

### Backend
- Can be deployed to Railway, Render, or AWS
- Ensure PostgreSQL database is configured
- Set environment variables in production

### Frontend
- Deploy to Vercel, Netlify, or Cloudflare Pages
- Update API URL and WebSocket URL in production build

## 🤝 Contributing

This project was built as part of the Euphotic Labs Backend Development Internship assignment.

## 📝 License

MIT

## 📹 Demo Videos

1. **App Demonstration** (1 minute): Shows the working application with real-time updates
2. **Code Explanation** (1 minute): Explains the architecture and key components

## 👨‍💻 Author

**Vasanth** - Backend Development Intern Candidate  
Euphotic Labs Private Limited

## 🎯 Assignment Requirements

This project fulfills all requirements of the Full Stack Problem Statement:

✅ Database with dishes table (dishId, dishName, imageUrl, isPublished)  
✅ API to fetch all dishes  
✅ API to toggle dish published status  
✅ React dashboard displaying all dishes  
✅ Toggle button updating UI and backend  
✅ **Bonus: Real-time updates** using WebSockets

---

Built with ❤️ for Euphotic Labs Internship Assignment
