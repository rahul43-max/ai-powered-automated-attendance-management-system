import React from 'react';
import Navbar from '../components/Navbar';

const SMS = () => {
  const smsData = [
    { sno: 1, date: '04-03-2026', phone: '9912961798', msg: 'Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 6 periods out of 6 periods on 04-03-2026. For any queries, contact mentor: VEDELLI NARESH, 8886660836 between 9:00AM to 7:00PM only. Principal, TKREC.' },
    { sno: 2, date: '25-02-2026', phone: '9912961798', msg: 'Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 6 periods out of 6 periods on 25-02-2026. For any queries, contact mentor: VEDELLI NARESH, 8886660836 between 9:00AM to 7:00PM only. Principal, TKREC.' },
    { sno: 3, date: '24-02-2026', phone: '9912961798', msg: 'Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 3 periods out of 6 periods on 24-02-2026. For any queries, contact mentor: VEDELLI NARESH, 8886660836 between 9:00AM to 7:00PM only. Principal, TKREC.' },
    { sno: 4, date: '20-02-2026', phone: '9912961798', msg: 'Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 3 periods out of 6 periods on 20-02-2026. For any queries, contact mentor: VEDELLI NARESH, 8886660836 between 9:00AM to 7:00PM only. Principal, TKREC.' },
    { sno: 5, date: '17-02-2026', phone: '9912961798', msg: 'Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 6 periods out of 6 periods on 17-02-2026. For any queries, contact mentor: VEDELLI NARESH, 8886660836 between 9:00AM to 7:00PM only. Principal, TKREC.' },
    { sno: 6, date: '13-02-2026', phone: '9912961798', msg: 'Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 6 periods out of 6 periods on 13-02-2026. For any queries, contact mentor: VEDELLI NARESH, 8886660836 between 9:00AM to 7:00PM only. Principal, TKREC.' },
    { sno: 7, date: '09-02-2026', phone: '9912961798', msg: 'Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 6 periods out of 6 periods on 09-02-2026. For any queries, contact mentor: VEDELLI NARESH, 8886660836 between 9:00AM to 7:00PM only. Principal, TKREC.' },
    { sno: 8, date: '05-02-2026', phone: '9912961798', msg: 'Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 3 periods out of 6 periods on 05-02-2026. For any queries, contact mentor: VEDELLI NARESH, 8886660836 between 9:00AM to 7:00PM only. Principal, TKREC.' },
    { sno: 9, date: '19-01-2026', phone: '9912961798', msg: 'Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 6 periods out of 6 periods on 19-01-2026. For any queries, contact mentor: VEDELLI NARESH, 8886660836 between 9:00AM to 7:00PM only. Principal, TKREC.' },
    { sno: 10, date: '27-12-2025', phone: '9912961798', msg: 'Dear Parent, Your ward Panjugula Rahul with Roll No : 23R91A05P1 is Absent for 6 periods out of 6 periods on 27-12-2025. For any queries, contact mentor: Chanda Priyanka, 9000104040 between 9:00AM to 7:00PM only. Principal, TKREC.' },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-[#f4f4f4]">
      <Navbar />
      <div className="flex-1 p-2 overflow-auto">
        <div className="max-w-7xl mx-auto space-y-4 pt-2">
          
          {/* Student Details Header */}
          <div className="tkrec-card bg-white border">
            <div className="text-center font-bold border-b p-1 bg-[#ffeaea]">Student Details</div>
            <div className="p-4 flex gap-4 items-center justify-between">
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

          {/* SMS Table Content */}
          <div className="tkrec-card border-[#e5a0a0] overflow-hidden">
            <div className="bg-[#fad8d8] p-2 flex justify-between items-center border-b border-[#e5a0a0]">
              <span className="text-sm font-semibold text-gray-800">III - II Sem</span>
              <span className="text-gray-500 text-xs">▼</span>
            </div>
            <div className="p-2 bg-white">
               <table className="w-full border-collapse text-xs text-center border border-blue-300">
                  <thead>
                    <tr><th colSpan="4" className="bg-[#e6f2ff] border border-blue-300 p-1.5 font-bold">Absentees SMS</th></tr>
                    <tr className="bg-[#e6f2ff]">
                      <th className="border border-blue-300 p-1.5 w-16">S. No</th>
                      <th className="border border-blue-300 p-1.5 w-32">Date</th>
                      <th className="border border-blue-300 p-1.5 w-32">Phone</th>
                      <th className="border border-blue-300 p-1.5">Message</th>
                    </tr>
                  </thead>
                  <tbody>
                    {smsData.map((row) => (
                      <tr key={row.sno} className="hover:bg-gray-50">
                         <td className="border border-blue-200 p-1.5">{row.sno}</td>
                         <td className="border border-blue-200 p-1.5 font-semibold text-gray-800">{row.date}</td>
                         <td className="border border-blue-200 p-1.5">{row.phone}</td>
                         <td className="border border-blue-200 p-1.5 text-left">{row.msg}</td>
                      </tr>
                    ))}
                  </tbody>
               </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SMS;
