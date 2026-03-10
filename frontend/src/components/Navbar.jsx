import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const tabs = [
    { name: 'Home', path: '/home' },
    { name: 'Details', path: '/details' },
    { name: 'TimeTable', path: '/timetable' },
    { name: 'Attendance', path: '/attendance' },
    { name: 'Marks', path: '/marks' },
    { name: 'SMS', path: '/sms' },
    { name: 'Results', path: '/results' },
    { name: 'Course Exit', path: '/course-exit' },
    { name: 'Voting', path: '/voting' }
  ];

  const handleLogout = () => {
    navigate('/');
  };

  return (
    <nav className="bg-[#df414e] text-white flex justify-between items-center py-2 px-4 shadow-md z-50">
      <div className="flex items-center space-x-4">
        <div className="flex items-center text-xl font-bold bg-white text-[#df414e] px-2 py-0.5 rounded shadow">
          <span>TKREC</span>
        </div>
        <div className="flex space-x-1">
          {tabs.map((tab) => (
            <NavLink
              key={tab.name}
              to={tab.path}
              className={({ isActive }) =>
                `px-3 py-1 text-sm font-medium transition-colors rounded-md ${
                  isActive ? 'bg-white text-[#df414e]' : 'hover:bg-white/20'
                }`
              }
            >
              {tab.name}
            </NavLink>
          ))}
        </div>
      </div>
      <div className="flex items-center space-x-2 relative">
        <div 
          className="text-sm font-medium cursor-pointer flex items-center bg-[#fcecec] text-black px-2 py-1 rounded shadow"
          onClick={() => setDropdownOpen(!dropdownOpen)}
        >
          Panjugula Rahul <span className="ml-1 text-xs">▼</span>
        </div>
        
        {dropdownOpen && (
          <div className="absolute top-10 right-0 w-36 bg-[#fcecec] rounded-md shadow-xl border border-[#e5a0a0] z-50 overflow-hidden">
            <button 
              onClick={handleLogout}
              className="w-full text-left px-4 py-2 text-sm text-black font-semibold hover:bg-[#fad8d8] transition-colors"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
