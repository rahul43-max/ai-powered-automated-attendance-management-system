import React from 'react';
import Navbar from '../components/Navbar';

const TimeTable = () => {
  return (
    <div className="min-h-screen flex flex-col bg-[#f4f4f4]">
      <Navbar />
      <div className="flex-1 p-2 overflow-auto">
        <div className="max-w-6xl mx-auto space-y-4 pt-2">
          
          {/* Student Details Header */}
          <div className="tkrec-card bg-[#ffeaea] border">
            <div className="text-center font-bold border-b p-1">Student Details</div>
            <div className="p-4 flex gap-4 bg-white items-center justify-between">
              <div className="flex-1 grid grid-cols-[150px_1fr] gap-y-2 text-sm text-center">
                <span className="text-gray-600 text-right pr-4">Roll No.</span><span className="font-semibold text-left">23R91A05P1</span>
                <span className="text-gray-600 text-right pr-4">Student Name</span><span className="font-semibold text-left">Panjugula Rahul</span>
                <span className="text-gray-600 text-right pr-4">Fathers Name</span><span className="font-semibold text-left">P.Ashok</span>
                <span className="text-gray-600 text-right pr-4">Department</span><span className="font-semibold text-left">III CSE II D (B.Tech)</span>
              </div>
              <div className="w-24 h-28 border bg-blue-100 flex-shrink-0">
                <img src="https://via.placeholder.com/96x112" alt="Student" className="w-full h-full object-cover" />
              </div>
            </div>
          </div>

          {/* TimeTable Main Card */}
          <div className="tkrec-card bg-white p-4">
            
            {/* Header Section */}
            <div className="text-center mb-6 border-b pb-4">
              <h1 className="text-2xl font-bold text-[#b71c1c]">
                TEEGALA KRISHNA REDDY ENGINEERING COLLEGE
              </h1>
              <p className="text-xs font-semibold">(UGC-AUTONOMOUS)</p>
              <p className="text-[10px] text-gray-600 mb-2">
                (Sponsored by TKR Educational Society, Approved by AICTE, Affiliated to JNTUH Accredited by NAAC & NBA)<br />
                Medbowli, Meerpet, Balapur(M), Hyderabad, Telangana - 500097
              </p>
            </div>

            {/* TimeTable Matrix */}
            <table className="tkrec-table w-full">
              <thead>
                <tr className="bg-[#ffeaea]"><th colSpan="7" className="text-center font-bold border-b">III CSE II D</th></tr>
                <tr className="bg-[#ffeaea]">
                  <th rowSpan="2" className="w-16">DAY</th>
                  <th colSpan="6" className="text-center">PERIODS</th>
                </tr>
                <tr className="bg-[#ffeaea]">
                  <th className="w-1/6">1</th><th className="w-1/6">2</th><th className="w-1/6">3</th><th className="w-1/6">4</th><th className="w-1/6">5</th><th className="w-1/6">6</th>
                </tr>
              </thead>
              <tbody>
                <tr><th className="bg-[#fff9e6]">MON</th><td>ML</td><td>FLAT</td><td>SL</td><td>FIT</td><td>AI</td><td>ML</td></tr>
                <tr><th className="bg-[#fff9e6]">TUE</th><td>FLAT</td><td>FLAT</td><td>AI</td><td>SL</td><td>FIT</td><td>ML</td></tr>
                <tr><th className="bg-[#fff9e6]">WED</th><td>AI Lab</td><td>AI Lab</td><td>AI Lab</td><td>SL</td><td>AI</td><td>FIT</td></tr>
                <tr><th className="bg-[#fff9e6]">THU</th><td>ML Lab</td><td>ML Lab</td><td>ML Lab</td><td>SL</td><td>FLAT</td><td>FIT</td></tr>
                <tr><th className="bg-[#fff9e6]">FRI</th><td>SL</td><td>AI</td><td>FIT</td><td>FLAT</td><td>ML</td><td>EN</td></tr>
                <tr><th className="bg-[#fff9e6]">SAT</th><td>SL Lab</td><td>SL Lab</td><td>SL Lab</td><td>FLAT</td><td>AI</td><td>ML</td></tr>
              </tbody>
            </table>

          </div>

        </div>
      </div>
    </div>
  );
};

export default TimeTable;
