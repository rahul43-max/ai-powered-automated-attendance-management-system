import React, { useState } from 'react';
import Navbar from '../components/Navbar';

const Attendance = () => {
  // State to toggle accordions. We mock one open for demonstration.
  const [openDate, setOpenDate] = useState('09-03-2026');

  const toggleAccordion = (date) => {
    setOpenDate(openDate === date ? null : date);
  };

  const attendanceData = [
    { date: '09-03-2026', c: 6, p: 6, details: [
      { p: 1, a: 'P', sub: 'Machine Learning', fac: 'Edikoju Shirisha', top: 'Unit- 5 Introduction' },
      { p: 2, a: 'P', sub: 'Formal Languages And Automata Theory', fac: 'Chanda Priyanka', top: 'Turing Machine' },
      { p: 3, a: 'P', sub: 'Scripting Languages', fac: 'A Mounika', top: 'Subroutines' },
      { p: 4, a: 'P', sub: 'Fundamentals Of Internet Of Things', fac: 'Boyinipally Naveena', top: 'Sensor Cloud' },
      { p: 5, a: 'P', sub: 'Artificial Intelligence', fac: 'T. Rakesh Kumar', top: 'Other Classical Planning' },
      { p: 6, a: 'P', sub: 'Machine Learning', fac: 'Edikoju Shirisha', top: 'Reinforcement Learning' },
    ]},
    { date: '07-03-2026', c: 6, p: 6, details: [] },
    { date: '06-03-2026', c: 6, p: 6, details: [] },
    { date: '05-03-2026', c: 6, p: 6, details: [] },
    { date: '04-03-2026', c: 6, p: 0, details: [] },
    { date: '02-03-2026', c: 6, p: 5, details: [] },
    { date: '28-02-2026', c: 6, p: 6, details: [] },
    { date: '27-02-2026', c: 6, p: 6, details: [] },
    { date: '26-02-2026', c: 6, p: 6, details: [] },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-[#f4f4f4]">
      <Navbar />
      <div className="flex-1 p-2 overflow-auto">
        <div className="max-w-7xl mx-auto space-y-2 pt-2">
          
          {attendanceData.map((day) => {
            const isOpen = openDate === day.date;
            
            return (
              <div key={day.date} className="tkrec-card rounded-md overflow-hidden border-[#e5a0a0]">
                {/* Accordion Header */}
                <div 
                  className={`bg-[#fcecec] border-b border-[#e5a0a0] p-2 flex justify-between items-center cursor-pointer hover:bg-[#fad8d8] transition-colors`}
                  onClick={() => toggleAccordion(day.date)}
                >
                  <span className="text-sm font-semibold text-gray-800">
                    {day.date} <span className="text-gray-500 font-normal">| Classes Conducted: {day.c} | Present: {day.p}</span>
                  </span>
                  <span className="text-gray-500 text-xs">
                    {isOpen ? '▲' : '▼'}
                  </span>
                </div>
                
                {/* Accordion Body */}
                {isOpen && (
                  <div className="p-2 bg-white">
                    {day.details.length > 0 ? (
                      <table className="tkrec-table w-full text-left">
                        <thead>
                          <tr className="bg-[#fff0f0]">
                            <th className="w-12 text-center">P</th>
                            <th className="w-12 text-center">A</th>
                            <th className="w-1/4">Subject</th>
                            <th className="w-1/4">Faculty</th>
                            <th className="w-1/4">Topic</th>
                          </tr>
                        </thead>
                        <tbody>
                          {day.details.map((detail, idx) => (
                            <tr key={idx}>
                              <td className="text-center font-bold text-blue-600">{detail.p}</td>
                              <td className="text-center font-bold text-green-700">{detail.a}</td>
                              <td>{detail.sub}</td>
                              <td>{detail.fac}</td>
                              <td>{detail.top}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    ) : (
                      <div className="text-center text-sm text-gray-500 py-4 italic">No detailed records available for this date.</div>
                    )}
                  </div>
                )}
              </div>
            );
          })}

        </div>
      </div>
    </div>
  );
};

export default Attendance;
