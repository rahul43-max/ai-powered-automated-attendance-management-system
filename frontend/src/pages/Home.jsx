import React from 'react';
import Navbar from '../components/Navbar';

const Home = () => {
  return (
    <div className="min-h-screen flex flex-col bg-[#f4f4f4]">
      <Navbar />
      <div className="flex-1 p-2 overflow-auto">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-2 max-w-[1600px] mx-auto">
          
          {/* LEFT COLUMN */}
          <div className="space-y-2">
            
            {/* Student Details */}
            <div className="bg-white border text-xs">
              <div className="bg-[#e6f0fa] border-b p-1 text-center font-bold">Student Details</div>
              <div className="p-2 flex gap-4">
                <div className="flex-1 space-y-2">
                  <div className="flex justify-between border-b border-dashed pb-1">
                    <span className="text-gray-600">Roll No.</span><span className="font-semibold">23R91A05P1</span>
                  </div>
                  <div className="flex justify-between border-b border-dashed pb-1">
                    <span className="text-gray-600">Student Name</span><span className="font-semibold">Panjugula Rahul</span>
                  </div>
                  <div className="flex justify-between border-b border-dashed pb-1">
                    <span className="text-gray-600">Fathers Name</span><span className="font-semibold">P.Ashok</span>
                  </div>
                  <div className="flex justify-between border-b border-dashed pb-1">
                    <span className="text-gray-600">Department</span><span className="font-semibold">III CSE II D (B.Tech)</span>
                  </div>
                </div>
                <div className="w-20 h-24 border bg-blue-100 flex-shrink-0">
                  <img src="https://via.placeholder.com/80x100" alt="Student" className="w-full h-full object-cover" />
                </div>
              </div>
            </div>

            {/* Absentees SMS */}
            <div className="bg-white border text-xs">
              <div className="bg-[#e6f0fa] border-b p-1 text-center font-bold">Absentees SMS</div>
              <div className="overflow-x-auto">
                <table className="tkrec-table w-full">
                  <thead>
                    <tr><th>Date</th><th>Phone</th><th>Message</th></tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>04-03-26</td><td>9912961798</td>
                      <td className="text-left w-64 p-2 text-[10px]">Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 6 periods out of 6 periods on 04-03-2026. For any queries, contact mentor: VEDELLI NARESH, 8886660836 between 9:00AM to 7:00PM only. Principal, TKREC.</td>
                    </tr>
                    <tr>
                      <td>25-02-26</td><td>9912961798</td>
                      <td className="text-left w-64 p-2 text-[10px]">Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 6 periods out of 6 periods on 25-02-2026.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
          </div>

          {/* MIDDLE COLUMN */}
          <div className="space-y-2">
            
            {/* Attendance Summary */}
            <div className="bg-white border text-xs">
              <div className="bg-[#fff3cd] border-b p-1 text-center font-bold text-yellow-900 overflow-hidden">Attendance</div>
              <table className="tkrec-table w-full">
                <thead>
                  <tr>
                    <th rowSpan="2" className="bg-[#fff9e6]">Subject</th>
                    <th colSpan="3" className="bg-[#fff9e6]">Classes</th>
                  </tr>
                  <tr><th className="bg-[#fff9e6]">C</th><th className="bg-[#fff9e6]">A</th><th className="bg-[#fff9e6]">%</th></tr>
                </thead>
                <tbody>
                  <tr><td className="text-left">Machine Learning</td><td className="text-blue-600 font-bold">66</td><td className="text-blue-600 font-bold">50</td><td className="text-blue-600 font-bold">75.76</td></tr>
                  <tr><td className="text-left">Formal Languages And Automata Theory</td><td className="text-blue-600 font-bold">66</td><td className="text-blue-600 font-bold">54</td><td className="text-blue-600 font-bold">81.82</td></tr>
                  <tr><td className="text-left">Artificial Intelligence</td><td className="text-blue-600 font-bold">65</td><td className="text-blue-600 font-bold">50</td><td className="text-blue-600 font-bold">76.92</td></tr>
                  <tr><td className="text-left font-bold text-red-500">Industrial Oriented Mini Project / Internship / Skill Development Course</td><td className="text-red-500 font-bold">0</td><td colSpan="2"></td></tr>
                  <tr><td className="text-left">Machine Learning Lab</td><td className="text-blue-600 font-bold">31</td><td className="text-blue-600 font-bold">28</td><td className="text-blue-600 font-bold">90.32</td></tr>
                  <tr className="bg-orange-50 font-bold"><td className="text-right text-gray-800">Total :</td><td className="text-black">441</td><td className="text-black">359</td><td className="text-blue-700">81.41</td></tr>
                </tbody>
              </table>
            </div>

            {/* Periods Matrix */}
            <div className="bg-white border text-xs">
              <div className="bg-[#fff3cd] border-b p-1 text-center font-bold text-yellow-900">Periods</div>
              <table className="tkrec-table w-full">
                <thead>
                  <tr>
                    <th>Date</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>Total</th><th>Attend</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><td>09-03-26</td><td className="tkrec-present text-green-700">P</td><td className="tkrec-present text-green-700">P</td><td className="tkrec-present text-green-700">P</td><td className="tkrec-present text-green-700">P</td><td className="tkrec-present text-green-700">P</td><td className="tkrec-present text-green-700">P</td><td className="font-bold">6</td><td className="text-green-700 font-bold">6</td></tr>
                  <tr className="bg-[#ffeaea]"><td className="font-bold text-red-600">04-03-26</td><td className="tkrec-absent">A</td><td className="tkrec-absent">A</td><td className="tkrec-absent">A</td><td className="tkrec-absent">A</td><td className="tkrec-absent">A</td><td className="tkrec-absent">A</td><td className="font-bold text-red-600">6</td><td className="font-bold text-red-600">0</td></tr>
                  <tr><td>02-03-26</td><td className="tkrec-absent">A</td><td className="tkrec-present text-green-700">P</td><td className="tkrec-present text-green-700">P</td><td className="tkrec-present text-green-700">P</td><td className="tkrec-present text-green-700">P</td><td className="tkrec-present text-green-700">P</td><td className="font-bold">6</td><td className="text-red-600 font-bold">5</td></tr>
                </tbody>
              </table>
            </div>

          </div>

          {/* RIGHT COLUMN */}
          <div className="space-y-2">
            
            {/* Mid Marks */}
            <div className="bg-white border text-xs overflow-x-auto">
              <table className="tkrec-table w-full">
                <thead>
                  <tr className="bg-[#e6fcf5]"><th className="bg-[#e6fcf5]">Subject</th><th className="bg-[#e6fcf5]">I Mid</th><th className="bg-[#e6fcf5]">II Mid</th><th className="bg-[#e6fcf5]">Avg</th><th className="bg-[#e6fcf5]">Activity</th><th className="bg-[#e6fcf5]">Total</th></tr>
                </thead>
                <tbody>
                  <tr><td>ML</td><td>31</td><td></td><td>31</td><td></td><td>31</td></tr>
                  <tr><td>FLAT</td><td>25</td><td></td><td>25</td><td></td><td>25</td></tr>
                  <tr><td>AI</td><td>25</td><td></td><td>25</td><td></td><td>25</td></tr>
                  <tr><td>SL</td><td>25</td><td></td><td>25</td><td></td><td>25</td></tr>
                  <tr><td>FIT</td><td>30</td><td></td><td>30</td><td></td><td>30</td></tr>
                  <tr><td>ML Lab</td><td>26</td><td></td><td>26</td><td></td><td>26</td></tr>
                </tbody>
              </table>
            </div>

            {/* Upto Date Results */}
            <div className="bg-white border text-xs overflow-x-auto">
              <div className="bg-[#e6fcf5] border-b p-1 text-center font-bold">Upto Date Results (Roll No. 23R91A05P1)</div>
              <table className="tkrec-table w-full">
                <thead>
                  <tr><th>Sem</th><th>Credits</th><th>Back Logs</th><th>Fail Subjects</th></tr>
                </thead>
                <tbody>
                  <tr><td className="font-bold">III - I</td><td className="text-blue-600 font-bold">20 / 20</td><td className="text-blue-600 font-bold">Nil</td><td className="text-blue-600 font-bold">Nil</td></tr>
                  <tr><td className="font-bold">II - II</td><td className="text-blue-600 font-bold">20 / 20</td><td className="text-blue-600 font-bold">Nil</td><td className="text-blue-600 font-bold">Nil</td></tr>
                  <tr><td className="font-bold">II - I</td><td className="text-blue-600 font-bold">20 / 20</td><td className="text-blue-600 font-bold">Nil</td><td className="text-blue-600 font-bold">Nil</td></tr>
                  <tr className="bg-[#e6fcf5] font-bold"><td className="text-right">Upto</td><td className="text-blue-600">100 / 100</td><td className="text-blue-600">Nil</td><td className="text-blue-600">Nil</td></tr>
                </tbody>
              </table>
            </div>

            {/* Sem Details */}
            <div className="bg-white border text-xs overflow-x-auto">
              <div className="bg-[#e6fcf5] border-b p-1 text-center font-bold">III - I Sem (Roll No. 23R91A05P1)</div>
              <table className="tkrec-table w-full">
                <thead>
                  <tr><th colSpan="2">Subject</th><th rowSpan="2">G</th><th rowSpan="2">GP</th><th rowSpan="2">C</th><th rowSpan="2">Result</th></tr>
                  <tr><th>Code</th><th>Name</th></tr>
                </thead>
                <tbody>
                  <tr><td>22CS501PC</td><td className="text-left">Design And Analysis Of Algorithms</td><td>A</td><td>8</td><td>4.00</td><td>Pass</td></tr>
                  <tr><td>22CS502PC</td><td className="text-left">Computer Networks</td><td>A+</td><td>9</td><td>3.00</td><td>Pass</td></tr>
                  <tr><td>22CS503PC</td><td className="text-left">Dev Ops</td><td>A+</td><td>9</td><td>3.00</td><td>Pass</td></tr>
                  <tr><td>22CS513PE</td><td className="text-left">Data Analytics</td><td>A+</td><td>9</td><td>3.00</td><td>Pass</td></tr>
                </tbody>
              </table>
            </div>

          </div>

        </div>
      </div>
    </div>
  );
};

export default Home;
