import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('student'); // 'staff' or 'student'

  const handleLogin = (e) => {
    e.preventDefault();
    navigate('/home');
  };

  return (
    <div className="min-h-screen bg-white flex flex-col font-sans">
      
      {/* Top Header Logo Area */}
      <div className="flex justify-center items-center py-2 border-b">
        <div className="text-center font-bold text-[#1a237e] flex flex-col items-center">
            {/* Mocked Logo text / structure to match screenshot header */}
            <div className="text-2xl tracking-wide">TEEGALA KRISHNA REDDY ENGINEERING COLLEGE</div>
            <div className="text-sm font-semibold">(UGC-AUTONOMOUS)</div>
            <div className="text-[10px] text-gray-700 font-normal">
              (Sponsored by TKR Educational Society, Approved by AICTE, Affiliated to JNTUH Accredited by NAAC & NBA)<br />
              Medbowli, Meerpet, Balapur(M), Hyderabad, Telangana - 500097
            </div>
        </div>
      </div>

      {/* Blue Navigation Bar */}
      <div className="bg-[#1a237e] text-white flex px-4">
        <button className="bg-black text-green-500 font-bold px-4 py-1.5 text-sm m-1">Home</button>
        <button className="px-4 py-1.5 text-sm hover:bg-black/20 transition-colors">News Letters</button>
        <button className="px-4 py-1.5 text-sm hover:bg-black/20 transition-colors">Gallary</button>
        <button className="px-4 py-1.5 text-sm hover:bg-black/20 transition-colors">Study Materials ▾</button>
        <button className="px-4 py-1.5 text-sm hover:bg-black/20 transition-colors">Notifications</button>
        <button className="px-4 py-1.5 text-sm hover:bg-black/20 transition-colors">Syllabus</button>
        <button className="px-4 py-1.5 text-sm hover:bg-black/20 transition-colors">Downloads</button>
        <button className="px-4 py-1.5 text-sm hover:bg-black/20 transition-colors">Feedback</button>
        <button className="px-4 py-1.5 text-sm hover:bg-black/20 transition-colors">cbt</button>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 p-2 max-w-[1600px] mx-auto w-full grid grid-cols-1 lg:grid-cols-4 gap-4 mt-2">
        
        {/* Left Carousel / Banner Area (Takes 3 columns) */}
        <div className="lg:col-span-3 border-[3px] border-[#00bcd4] rounded-xl overflow-hidden relative min-h-[500px] bg-gray-100 flex items-center justify-center">
           {/* Mocking the banner image with a placeholder that roughly shows the context */}
           <img 
              src="https://via.placeholder.com/1200x600/f0f8ff/333333?text=College+Graduation+Day+Banner" 
              alt="Graduation Day Banner" 
              className="w-full h-full object-cover mix-blend-multiply"
           />
           {/* Mock Arrows for visual fidelity */}
           <div className="absolute left-4 top-1/2 transform -translate-y-1/2 w-10 h-10 bg-green-500/50 rounded-full flex items-center justify-center text-white text-xl cursor-not-allowed">
              ‹
           </div>
           <div className="absolute right-4 top-1/2 transform -translate-y-1/2 w-10 h-10 bg-green-500/50 rounded-full flex items-center justify-center text-white text-xl cursor-not-allowed">
              ›
           </div>
        </div>

        {/* Right Sidebar Login & Notifications */}
        <div className="space-y-4">
          
          {/* Login Accordions */}
          <div className="border border-gray-300 rounded shadow-sm overflow-hidden">
            
            {/* Staff Login Tab */}
            <div>
              <button 
                onClick={() => setActiveTab(activeTab === 'staff' ? '' : 'staff')}
                className={`w-full text-left px-4 py-2 font-bold flex justify-between items-center transition-colors ${
                  activeTab === 'staff' ? 'bg-[#00bcd4] text-white' : 'bg-[#e0f7fa] text-gray-800 border-b border-gray-300'
                }`}
              >
                Staff Login
                <span>{activeTab === 'staff' ? '▲' : '▼'}</span>
              </button>
              
              {activeTab === 'staff' && (
                <div className="p-4 bg-white border-b border-gray-300">
                  <form onSubmit={handleLogin} className="space-y-3">
                    <div className="relative flex items-center">
                      <div className="w-10 h-10 flex items-center justify-center border border-gray-300 bg-gray-50 text-gray-500">
                        👤
                      </div>
                      <input 
                        type="text" 
                        required
                        defaultValue="23R91A05P1"
                        className="flex-1 h-10 border border-l-0 border-gray-300 px-3 bg-[#f0f8ff] focus:outline-none focus:ring-1 focus:ring-blue-500"
                      />
                    </div>
                    <div className="relative flex items-center">
                      <div className="w-10 h-10 flex items-center justify-center border border-gray-300 bg-gray-50 text-gray-500">
                        🔒
                      </div>
                      <input 
                        type="password" 
                        required
                        defaultValue="..........."
                        className="flex-1 h-10 border border-l-0 border-gray-300 px-3 bg-[#f0f8ff] focus:outline-none focus:ring-1 focus:ring-blue-500"
                      />
                    </div>
                    <div className="text-center pt-2">
                      <button type="submit" className="bg-[#4caf50] text-white px-6 py-1.5 font-bold rounded shadow hover:bg-green-600 transition-colors">
                        Login
                      </button>
                    </div>
                  </form>
                </div>
              )}
            </div>

            {/* Student Login Tab */}
            <div>
              <button 
                onClick={() => setActiveTab(activeTab === 'student' ? '' : 'student')}
                className={`w-full text-left px-4 py-2 font-bold flex justify-between items-center transition-colors ${
                  activeTab === 'student' ? 'bg-[#4caf50] text-white' : 'bg-[#e8f5e9] text-gray-800'
                }`}
              >
                Student Login
                <span>{activeTab === 'student' ? '▲' : '▼'}</span>
              </button>
              
              {activeTab === 'student' && (
                <div className="p-4 bg-white">
                  <form onSubmit={handleLogin} className="space-y-3">
                    <div className="relative flex items-center">
                      <div className="w-10 h-10 flex items-center justify-center border border-gray-300 bg-gray-50 text-gray-500">
                        👤
                      </div>
                      <input 
                        type="text" 
                        required
                        defaultValue="23R91A05P1"
                        className="flex-1 h-10 border border-l-0 border-gray-300 px-3 bg-[#f0f8ff] focus:outline-none focus:ring-1 focus:ring-blue-500"
                      />
                    </div>
                    <div className="relative flex items-center">
                      <div className="w-10 h-10 flex items-center justify-center border border-gray-300 bg-gray-50 text-gray-500">
                        🔒
                      </div>
                      <input 
                        type="password" 
                        required
                        defaultValue="..........."
                        className="flex-1 h-10 border border-l-0 border-gray-300 px-3 bg-[#f0f8ff] focus:outline-none focus:ring-1 focus:ring-blue-500"
                      />
                    </div>
                    <div className="text-center pt-2">
                      <button type="submit" className="bg-[#4caf50] text-white px-6 py-1.5 font-bold rounded shadow hover:bg-green-600 transition-colors">
                        Login
                      </button>
                    </div>
                  </form>
                </div>
              )}
            </div>

          </div>

          {/* Notifications Panel */}
          <div className="border border-[#ffca28] rounded overflow-hidden">
            <div className="bg-[#ffca28] font-bold text-center py-2 text-sm text-gray-900">
              Notifications
            </div>
            <div className="p-4 bg-white h-64 overflow-y-auto space-y-4 text-xs font-bold text-gray-700">
               <p className="border-b pb-2 cursor-pointer hover:text-blue-600">
                 R25 M TECH I-YEAR I-SEMESTER REGULAR END EXAMINATIONS (SEE) MARCH-2026-TIMETABLE
               </p>
               <p className="border-b pb-2 cursor-pointer hover:text-blue-600">
                 R22 M TECH I-YEAR II-SEMESTER SUPPLEMENTARY END EXAMINATIONS MARCH-2026-TIMETABLE
               </p>
               <p className="border-b pb-2 cursor-pointer hover:text-blue-600">
                 R22-MBA I-YEAR II-SEMESTER -SUPPLEMENTARY END -(SEE) EXAMINATIONS MARCH-2026-TIME TABLE
               </p>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Login;
