import React from 'react';

const Header = ({ isConnected }) => {
  return (
    <header className="bg-black text-white border-b border-gray-800">
      <div className="container mx-auto px-6 py-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-black tracking-tight">DISH MANAGEMENT</h1>
            <p className="text-gray-400 mt-2 text-sm font-light tracking-wide uppercase">Real-time Publishing Platform</p>
          </div>
          
          <div className="flex items-center gap-3 bg-gray-900 px-4 py-2 rounded-full border border-gray-800">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-white' : 'bg-gray-600'} animate-pulse`}></div>
            <span className="text-xs font-bold tracking-wider uppercase">
              {isConnected ? 'LIVE' : 'OFFLINE'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
