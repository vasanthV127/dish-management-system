import React, { useState, useEffect, useCallback } from 'react';
import { dishAPI } from './services/api';
import { useWebSocket } from './hooks/useWebSocket';
import Header from './components/Header';
import DishCard from './components/DishCard';
import './index.css';

function App() {
  const [dishes, setDishes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updatingDishId, setUpdatingDishId] = useState(null);
  const [error, setError] = useState(null);

  // Fetch all dishes
  const fetchDishes = async () => {
    try {
      setLoading(true);
      const data = await dishAPI.getAllDishes();
      setDishes(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching dishes:', err);
      setError('Failed to load dishes. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  // Handle WebSocket messages for real-time updates
  const handleWebSocketMessage = useCallback((message) => {
    if (message.type === 'dishStatusChanged') {
      const updatedDish = message.data;
      setDishes(prevDishes =>
        prevDishes.map(dish =>
          dish.dishId === updatedDish.dishId
            ? { ...dish, isPublished: updatedDish.isPublished }
            : dish
        )
      );
    }
  }, []);

  // Connect to WebSocket
  const { isConnected } = useWebSocket(handleWebSocketMessage);

  // Toggle dish status
  const handleToggleDish = async (dishId) => {
    try {
      setUpdatingDishId(dishId);
      await dishAPI.toggleDishStatus(dishId);
      // The update will come through WebSocket
    } catch (err) {
      console.error('Error toggling dish:', err);
      alert('Failed to update dish status');
    } finally {
      setUpdatingDishId(null);
    }
  };

  useEffect(() => {
    fetchDishes();
  }, []);

  return (
    <div className="min-h-screen bg-black">
      <Header isConnected={isConnected} />
      
      <main className="container mx-auto px-6 py-12">
        {error && (
          <div className="bg-gray-900 border border-red-900 text-red-500 px-6 py-4 mb-8 font-mono text-sm">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-white"></div>
          </div>
        ) : (
          <>
            <div className="mb-12 flex justify-between items-center">
              <div>
                <h2 className="text-3xl font-black text-white tracking-tight">
                  ALL DISHES
                </h2>
                <p className="text-gray-500 text-sm mt-1 font-light tracking-wide">
                  {dishes.length} items in catalog
                </p>
              </div>
              <button
                onClick={fetchDishes}
                className="bg-white text-black px-6 py-3 font-bold tracking-wider uppercase text-xs hover:bg-gray-200 transition-all"
              >
                REFRESH
              </button>
            </div>

            {dishes.length === 0 ? (
              <div className="text-center py-24">
                <p className="text-gray-600 text-lg uppercase tracking-wider font-light">No dishes available</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {dishes.map((dish) => (
                  <DishCard
                    key={dish.dishId}
                    dish={dish}
                    onToggle={handleToggleDish}
                    isLoading={updatingDishId === dish.dishId}
                  />
                ))}
              </div>
            )}
          </>
        )}
      </main>

      <footer className="bg-black border-t border-gray-900 py-8 mt-16">
        <div className="container mx-auto px-6 text-center">
          <p className="text-gray-600 text-xs uppercase tracking-widest font-light">
            React × Tailwind CSS × FastAPI × PostgreSQL
          </p>
          <p className="text-gray-800 text-xs mt-3 tracking-wide">
            Euphotic Labs — Backend Development Internship
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
