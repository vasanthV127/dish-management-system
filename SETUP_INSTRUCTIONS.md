# Complete Setup Instructions

## Prerequisites

Before starting, ensure you have:

- **Python 3.12+** installed ([Download Python](https://www.python.org/downloads/))
- **Node.js 18+** and npm installed ([Download Node.js](https://nodejs.org/))
- **PostgreSQL 14+** installed ([Download PostgreSQL](https://www.postgresql.org/download/))
- **pgAdmin** (comes with PostgreSQL) or any PostgreSQL client
- **Git** (optional, for version control)

## Step-by-Step Setup

### 1. Clone or Download the Project

```powershell
cd "d:\VASANTH\Final year\Euphotic Labs"
```

### 2. Setup PostgreSQL Database

**Option A: Using pgAdmin**
1. Open pgAdmin 4
2. Right-click on "Databases" → "Create" → "Database"
3. Enter database name: `dish_management`
4. Click "Save"

**Option B: Using SQL**
```sql
CREATE DATABASE dish_management;
```

### 3. Backend Setup

```powershell
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
```

**Edit `.env` file with your credentials:**
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dish_management
DB_USER=postgres
DB_PASSWORD=your_actual_password
PORT=8000
```

**Initialize database with sample data:**
```powershell
python -m app.init_db
```

Expected output:
```
🔄 Creating database tables...
✅ Tables created successfully.
🔄 Inserting sample dishes...
✅ 10 dishes inserted successfully.
```

**Start backend server:**
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Server will run on: http://localhost:8000

### 4. Frontend Setup

**Open a new PowerShell terminal:**

```powershell
# Navigate to frontend folder
cd "d:\VASANTH\Final year\Euphotic Labs\frontend"

# Install dependencies
npm install

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer

# Start development server
npm run dev
```

Frontend will run on: http://localhost:5173

## 5. Test the Application

1. Open your browser and visit: **http://localhost:5173**
2. You should see the Dish Management Dashboard
3. Try toggling dish status (Publish/Unpublish)

## 6. Test Real-Time Updates

1. Open **http://localhost:5173** in two browser windows side-by-side
2. Click "UNPUBLISH" or "PUBLISH" on any dish in one window
3. Watch the other window update **instantly** without page refresh!

## Troubleshooting

### Backend Issues

**Error: "could not connect to database"**
- Ensure PostgreSQL service is running
- Check Windows Services → PostgreSQL
- Verify credentials in `.env` file

**Error: "ModuleNotFoundError"**
- Make sure virtual environment is activated
- Run: `.\venv\Scripts\Activate.ps1`
- Reinstall: `pip install -r requirements.txt`

**Error: "database does not exist"**
- Create database in pgAdmin: `dish_management`

### Frontend Issues

**Error: "npm: command not found"**
- Install Node.js from https://nodejs.org/

**CSS not applied:**
- Run: `npm install -D tailwindcss postcss autoprefixer`
- Restart dev server: `npm run dev`

**Connection error:**
- Ensure backend is running on port 8000
- Check browser console for errors

## API Documentation

Once backend is running, visit:
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Stopping the Servers

**Backend:**
- Press `Ctrl + C` in the backend terminal

**Frontend:**
- Press `Ctrl + C` in the frontend terminal

## Next Steps

1. Test all features
2. Record demo videos (1 min each)
3. Push to GitHub
4. Submit for review

## Support

For issues or questions, refer to:
- `docs/ARCHITECTURE.md` - System architecture
- `docs/API_DOCUMENTATION.md` - API details
- `README.md` - Project overview
