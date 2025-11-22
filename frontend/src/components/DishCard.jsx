import React from 'react';

const DishCard = ({ dish, onToggle, isLoading }) => {
  const { dishId, dishName, imageUrl, isPublished } = dish;

  return (
    <div className="bg-black border border-gray-800 overflow-hidden hover:border-white transition-all duration-300 group">
      <div className="relative h-64 overflow-hidden">
        <img
          src={imageUrl}
          alt={dishName}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/400x300?text=No+Image';
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60"></div>
        <div className={`absolute top-3 right-3 px-3 py-1 text-[10px] font-bold tracking-widest uppercase ${
          isPublished 
            ? 'bg-white text-black' 
            : 'bg-gray-800 text-white border border-gray-700'
        }`}>
          {isPublished ? 'LIVE' : 'DRAFT'}
        </div>
      </div>
      
      <div className="p-5">
        <h3 className="text-xl font-black text-white mb-4 tracking-tight uppercase">{dishName}</h3>
        
        <button
          onClick={() => onToggle(dishId)}
          disabled={isLoading}
          className={`w-full py-3 px-4 font-bold tracking-wider uppercase text-sm transition-all duration-200 ${
            isLoading
              ? 'bg-gray-800 cursor-not-allowed text-gray-600'
              : isPublished
              ? 'bg-white text-black hover:bg-gray-200'
              : 'bg-gray-900 text-white border border-gray-700 hover:bg-white hover:text-black'
          }`}
        >
          {isLoading ? 'UPDATING...' : isPublished ? 'UNPUBLISH' : 'PUBLISH'}
        </button>
      </div>
    </div>
  );
};

export default DishCard;
