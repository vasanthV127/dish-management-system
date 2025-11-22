from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json

from .database import engine, get_db, Base
from .models import Dish
from .schemas import DishResponse

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dish Management API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"❌ Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# Routes
@app.get("/")
def read_root():
    return {"message": "Dish Management API", "status": "running"}

@app.get("/api/dishes", response_model=List[DishResponse])
def get_dishes(db: Session = Depends(get_db)):
    """Get all dishes"""
    dishes = db.query(Dish).order_by(Dish.dishId).all()
    return dishes

@app.patch("/api/dishes/{dish_id}/toggle", response_model=DishResponse)
async def toggle_dish_status(dish_id: int, db: Session = Depends(get_db)):
    """Toggle dish published status"""
    dish = db.query(Dish).filter(Dish.dishId == dish_id).first()
    
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    # Toggle the status
    dish.isPublished = not dish.isPublished
    db.commit()
    db.refresh(dish)
    
    # Broadcast update to all WebSocket clients
    await manager.broadcast({
        "type": "dishStatusChanged",
        "data": {
            "dishId": dish.dishId,
            "dishName": dish.dishName,
            "imageUrl": dish.imageUrl,
            "isPublished": dish.isPublished
        }
    })
    
    return dish

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for messages
            data = await websocket.receive_text()
            # Echo back or handle client messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
