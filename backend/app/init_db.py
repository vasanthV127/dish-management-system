from sqlalchemy.orm import Session
from .database import engine, SessionLocal, Base
from .models import Dish

# Sample dish data
sample_dishes = [
    {
        "dishName": "Pizza Margherita",
        "imageUrl": "https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=400",
        "isPublished": True
    },
    {
        "dishName": "Pasta Carbonara",
        "imageUrl": "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400",
        "isPublished": True
    },
    {
        "dishName": "Chicken Biryani",
        "imageUrl": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400",
        "isPublished": False
    },
    {
        "dishName": "Sushi Platter",
        "imageUrl": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400",
        "isPublished": True
    },
    {
        "dishName": "Tacos al Pastor",
        "imageUrl": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400",
        "isPublished": False
    },
    {
        "dishName": "Pad Thai",
        "imageUrl": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400",
        "isPublished": True
    },
    {
        "dishName": "Butter Chicken",
        "imageUrl": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400",
        "isPublished": True
    },
    {
        "dishName": "Greek Salad",
        "imageUrl": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400",
        "isPublished": False
    },
    {
        "dishName": "Ramen Bowl",
        "imageUrl": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400",
        "isPublished": True
    },
    {
        "dishName": "Chocolate Lava Cake",
        "imageUrl": "https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=400",
        "isPublished": False
    }
]

def init_database():
    """Initialize database with sample data"""
    print("🔄 Creating database tables...")
    
    # Create all tables
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tables created successfully.")
    
    # Create session
    db = SessionLocal()
    
    try:
        print("🔄 Inserting sample dishes...")
        
        # Insert sample dishes
        for dish_data in sample_dishes:
            dish = Dish(**dish_data)
            db.add(dish)
        
        db.commit()
        
        count = db.query(Dish).count()
        print(f"✅ {count} dishes inserted successfully.")
        
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
