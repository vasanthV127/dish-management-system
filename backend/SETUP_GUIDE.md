# Backend Setup Guide

## Step 1: Create PostgreSQL Database

### Using pgAdmin:

1. **Open pgAdmin 4**
2. **Connect to PostgreSQL Server**
   - Right-click on "Servers" → "PostgreSQL"
   - Enter your password if prompted

3. **Create Database**
   - Right-click on "Databases"
   - Select "Create" → "Database..."
   - **Database name**: `dish_management`
   - Click "Save"

### Using SQL (Alternative):

Open Query Tool in pgAdmin and run:
```sql
CREATE DATABASE dish_management;
```

## Step 2: Configure Backend Environment

1. Navigate to backend folder:
```powershell
cd "d:\VASANTH\Final year\Euphotic Labs\backend"
```

2. Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```

3. Edit `.env` file with your PostgreSQL credentials:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dish_management
DB_USER=postgres
DB_PASSWORD=your_actual_password_here
PORT=8000
```

## Step 3: Install Python Dependencies

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Initialize Database with Sample Data

```powershell
python -m app.init_db
```

Expected output:
```
🔄 Initializing database...
✅ Database initialized with 10 dishes
✅ Done!
```

## Step 5: Start Backend Server

```powershell
uvicorn app.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

## Step 6: Test Backend

Open browser and visit:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/
- Get Dishes: http://localhost:8000/api/dishes

## Troubleshooting

### Error: "could not connect to server"
- Make sure PostgreSQL service is running
- Check Windows Services → PostgreSQL
- Or use pgAdmin's dashboard

### Error: "password authentication failed"
- Update DB_PASSWORD in .env file
- Use the password you set during PostgreSQL installation

### Error: "database does not exist"
- Create database using pgAdmin (Step 1)

### Error: "pip not found"
- Make sure Python is installed
- Check: `python --version`

### Error: "module not found"
- Activate virtual environment first
- Run: `.\venv\Scripts\Activate.ps1`
