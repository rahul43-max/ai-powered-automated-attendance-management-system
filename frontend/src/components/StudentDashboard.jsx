import React, { useEffect, useState } from 'react';

export default function StudentDashboard({ user, onLogout }) {
    const [smsLogs, setSmsLogs] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:5000/api/sms_logs')
            .then(res => res.json())
            .then(data => setSmsLogs(data));
    }, []);

    return (
        <div className="min-h-screen bg-[#f4f4f4] flex flex-col items-center pb-10">

            {/* Top Red Header */}
            <header className="w-full bg-[#ef3d4c] text-white flex justify-between items-center px-4 py-2 border-b-4 border-[#c52834]">
                <div className="flex items-center gap-4 text-sm font-bold tracking-wide">
                    <h1 className="text-xl italic mr-2 border-r border-white/30 pr-4">TKREC</h1>
                    <nav className="flex gap-4">
                        <a href="#" className="bg-white text-red-600 px-3 py-1 rounded-sm shadow-sm ring-1 ring-red-800">Home</a>
                        <a href="#" className="hover:text-gray-200">Details</a>
                        <a href="#" className="hover:text-gray-200">TimeTable</a>
                        <a href="#" className="hover:text-gray-200">Attendance</a>
                        <a href="#" className="hover:text-gray-200">Marks</a>
                        <a href="#" className="hover:text-gray-200">Feedback</a>
                        <a href="#" className="hover:text-gray-200">SMS</a>
                        <a href="#" className="hover:text-gray-200">Results</a>
                        <a href="#" className="hover:text-gray-200">Course Exit</a>
                        <a href="#" className="hover:text-gray-200">Voting</a>
                    </nav>
                </div>

                <div className="flex items-center gap-2 text-sm font-semibold relative group cursor-pointer border border-transparent hover:border-white/50 px-2 py-1">
                    <span>{user?.full_name || 'Mukkam Nithish Kumar'}</span>
                    <span>▼</span>
                    <div className="absolute right-0 top-full mt-1 w-32 bg-white text-black shadow-lg hidden group-hover:block z-50 border">
                        <button onClick={onLogout} className="w-full text-left px-4 py-2 hover:bg-gray-100 text-sm font-bold text-red-600">Logout</button>
                    </div>
                </div>
            </header>

            {/* Main Grid Content */}
            <main className="w-full max-w-[1400px] mt-4 grid grid-cols-12 gap-2 px-2">

                {/* Left Column (Student Details & SMS) */}
                <div className="col-span-3 flex flex-col gap-2">

                    {/* Student Profile */}
                    <div className="bg-blue-50 border border-blue-200 shadow-sm text-sm">
                        <div className="text-center bg-white border-b border-blue-200 py-1 font-semibold text-gray-700">
                            Student Details
                        </div>
                        <div className="flex justify-between p-2">
                            <div className="flex flex-col gap-1 w-full text-xs">
                                <div className="flex justify-between border-b border-blue-100 pb-1">
                                    <span className="text-gray-600 w-1/3 text-right pr-2">Roll No.</span>
                                    <span className="font-bold text-gray-800 flex-1">{user?.user_id}</span>
                                </div>
                                <div className="flex justify-between border-b border-blue-100 pb-1 pt-1">
                                    <span className="text-gray-600 w-1/3 text-right pr-2">Student Name</span>
                                    <span className="font-bold text-gray-800 flex-1">{user?.full_name}</span>
                                </div>
                                <div className="flex justify-between border-b border-blue-100 pb-1 pt-1">
                                    <span className="text-gray-600 w-1/3 text-right pr-2">Fathers Name</span>
                                    <span className="font-bold text-gray-800 flex-1">Mukkam Krishna Goud</span>
                                </div>
                                <div className="flex justify-between pt-1">
                                    <span className="text-gray-600 w-1/3 text-right pr-2">Department</span>
                                    <span className="font-bold text-gray-800 flex-1">III CSE II D (B.Tech)</span>
                                </div>
                            </div>
                            <div className="flex-shrink-0 border border-gray-300 ml-2 w-16 h-20 bg-gray-200 flex items-center justify-center overflow-hidden">
                                <img src="/api/placeholder/100/120" alt="Profile" className="object-cover w-full h-full" />
                            </div>
                        </div>
                    </div>

                    {/* Absentees SMS */}
                    <div className="bg-[#f0f9ff] border border-blue-200 shadow-sm mt-1 flex-1">
                        <div className="text-center bg-white border-b border-blue-200 py-1 font-semibold text-gray-700 text-sm">
                            Absentees SMS
                        </div>
                        <table className="w-full text-xs text-left border-collapse border border-blue-200">
                            <thead>
                                <tr className="bg-blue-50 border-b border-blue-200">
                                    <th className="p-1.5 font-semibold text-center border-r border-blue-200">Date</th>
                                    <th className="p-1.5 font-semibold text-center border-r border-blue-200">Phone</th>
                                    <th className="p-1.5 font-semibold text-center">Message</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white">
                                {smsLogs.slice(0, 10).map((log, i) => (
                                    <tr key={i} className="border-b border-gray-200 align-top">
                                        <td className="p-1.5 border-r border-gray-200 text-center font-mono">{log.sent_at.split('T')[0]}</td>
                                        <td className="p-1.5 border-r border-gray-200 text-center font-mono">{log.phone_number}</td>
                                        <td className="p-1.5 text-gray-700 leading-tight">
                                            {log.message}
                                        </td>
                                    </tr>
                                ))}
                                {smsLogs.length === 0 && (
                                    <tr className="border-b border-gray-200">
                                        <td colSpan="3" className="p-2 text-center text-gray-500 italic">No SMS logs generated yet.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>

                </div>

                {/* Middle Column (Attendance Grid) */}
                <div className="col-span-5 flex flex-col gap-2">

                    {/* Subject Wise Summary */}
                    <div className="bg-[#fffdf2] border border-yellow-200 shadow-sm">
                        <div className="text-center py-1 font-semibold text-gray-700 text-sm border-b border-yellow-200">
                            Attendance
                        </div>
                        <table className="w-full text-xs border-collapse">
                            <thead>
                                <tr>
                                    <th className="border-b border-r border-yellow-200 p-1 w-2/3" rowSpan={2}>Subject</th>
                                    <th className="border-b border-yellow-200 p-1 text-center font-semibold bg-yellow-50" colSpan={3}>Classes</th>
                                </tr>
                                <tr className="bg-yellow-50">
                                    <th className="border-b border-r border-l border-yellow-200 p-1 w-10 text-center">C</th>
                                    <th className="border-b border-r border-yellow-200 p-1 w-10 text-center">A</th>
                                    <th className="border-b border-yellow-200 p-1 w-12 text-center">%</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white">
                                {[
                                    { n: 'Machine Learning', c: 64, a: 42, p: 65.63 },
                                    { n: 'Formal Languages And Automata Theory', c: 65, a: 41, p: 63.08 },
                                    { n: 'Artificial Intelligence', c: 64, a: 39, p: 60.94 },
                                    { n: 'Scripting Languages', c: 61, a: 40, p: 65.57 },
                                    { n: 'Fundamentals Of Internet Of Things', c: 55, a: 26, p: 47.27 },
                                    { n: 'Environmental Science', c: 14, a: 9, p: 64.29 },
                                    { n: 'Industrial Oriented Mini Project / Internship', c: 0, a: 0, p: 0 },
                                    { n: 'Machine Learning Lab', c: 31, a: 19, p: 61.29 },
                                    { n: 'Artificial Intelligence Lab', c: 30, a: 24, p: 80.00 },
                                    { n: 'Scripting Languages Lab', c: 45, a: 33, p: 73.33 },
                                ].map(s => (
                                    <tr key={s.n} className="border-b border-yellow-100 hover:bg-gray-50">
                                        <td className="p-1 border-r border-yellow-100 text-red-600 font-medium pl-2">{s.n}</td>
                                        <td className="p-1 border-r border-yellow-100 text-center font-bold text-blue-800">{s.c}</td>
                                        <td className="p-1 border-r border-yellow-100 text-center font-bold text-blue-800">{s.a}</td>
                                        <td className="p-1 text-center font-bold text-blue-800">{s.p.toFixed(2)}</td>
                                    </tr>
                                ))}
                            </tbody>
                            <tfoot className="bg-yellow-100 font-bold border-t-2 border-yellow-300">
                                <tr>
                                    <td className="p-1 text-right pr-2">Total :</td>
                                    <td className="p-1 text-center text-blue-900 border-l border-r border-yellow-200">429</td>
                                    <td className="p-1 text-center text-blue-900 border-r border-yellow-200">273</td>
                                    <td className="p-1 text-center text-blue-900">63.63</td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>

                    {/* Period Grid */}
                    <div className="bg-[#fffdf2] border border-yellow-200 shadow-sm flex-1 mb-2">
                        <div className="text-center bg-yellow-100 text-gray-700 font-semibold py-1 text-sm border-b border-yellow-200">
                            Periods
                        </div>
                        <div className="overflow-x-auto h-[400px]">
                            <table className="w-full text-xs text-center border-collapse">
                                <thead className="sticky top-0 bg-yellow-50 shadow-sm z-10">
                                    <tr>
                                        <th className="p-1.5 border border-yellow-200 w-24 tracking-wide font-bold">Date</th>
                                        <th className="p-1.5 border border-yellow-200 w-8">1</th>
                                        <th className="p-1.5 border border-yellow-200 w-8">2</th>
                                        <th className="p-1.5 border border-yellow-200 w-8">3</th>
                                        <th className="p-1.5 border border-yellow-200 w-8">4</th>
                                        <th className="p-1.5 border border-yellow-200 w-8">5</th>
                                        <th className="p-1.5 border border-yellow-200 w-8">6</th>
                                        <th className="p-1.5 border border-yellow-200 w-10 font-bold">Total</th>
                                        <th className="p-1.5 border border-yellow-200 w-10 font-bold">Attend</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white">
                                    {/* Mock Data referencing the period grid from screenshot */}
                                    {Array.from({ length: 15 }).map((_, idx) => {
                                        const rowDate = `0${8 - idx}-03-26`;
                                        return (
                                            <tr key={idx} className="border-b border-yellow-100">
                                                <td className="p-1.5 border-r border-yellow-200 font-bold text-gray-600">{idx === 0 ? 'Today' : (idx === 1 ? '07-03-26' : `0${7 - idx + 1}-03-26`)}</td>
                                                {[1, 2, 3, 4, 5, 6].map(p => {
                                                    const isAbsent = Math.random() > 0.7; // Simulate absences randomly
                                                    return (
                                                        <td key={p} className={`p-1 border-r border-yellow-200 font-bold text-lg ${isAbsent ? 'bg-[#ffebee] text-red-600' : 'text-green-700'}`}>
                                                            {isAbsent ? 'A' : 'P'}
                                                        </td>
                                                    )
                                                })}
                                                <td className="p-1.5 border-r border-yellow-200 font-bold text-gray-600 bg-yellow-50">6</td>
                                                <td className="p-1.5 font-bold text-red-600 bg-yellow-50">4</td>
                                            </tr>
                                        )
                                    })}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Right Column (Marks & Results) */}
                <div className="col-span-4 flex flex-col gap-2">
                    {/* Marks */}
                    <div className="bg-[#f0fdf4] border border-green-200 shadow-sm">
                        <table className="w-full text-xs text-center border-collapse">
                            <thead>
                                <tr className="bg-green-100 border-b border-green-200">
                                    <th className="p-1.5 font-semibold border-r border-green-200 text-left pl-2">Subject</th>
                                    <th className="p-1.5 font-semibold border-r border-green-200">I Mid</th>
                                    <th className="p-1.5 font-semibold border-r border-green-200">II Mid</th>
                                    <th className="p-1.5 font-semibold border-r border-green-200">Avg</th>
                                    <th className="p-1.5 font-semibold border-r border-green-200">Activity</th>
                                    <th className="p-1.5 font-semibold text-gray-800">Total</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white">
                                {['ML', 'FLAT', 'AI', 'SL', 'FIT', 'EN', 'ML Lab', 'AI Lab', 'SL Lab', 'IOMP'].map((sub, idx) => (
                                    <tr key={sub} className="border-b border-green-100">
                                        <td className="p-1 border-r border-green-100 text-green-800 font-medium text-left pl-2">{sub}</td>
                                        <td className="p-1 border-r border-green-100 text-red-600">{Math.floor(Math.random() * 10) + 25}</td>
                                        <td className="p-1 border-r border-green-100 text-red-600"></td>
                                        <td className="p-1 border-r border-green-100 font-bold">{Math.floor(Math.random() * 10) + 25}</td>
                                        <td className="p-1 border-r border-green-100 text-gray-500"></td>
                                        <td className="p-1 font-bold">{Math.floor(Math.random() * 10) + 25}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Results Up to date */}
                    <div className="bg-[#f0fdf4] border border-green-200 shadow-sm mt-1">
                        <div className="text-center py-1 font-bold text-xs text-gray-700 border-b border-green-200 bg-green-50">
                            Upto Date Results (Roll No. {user?.user_id})
                        </div>
                        <table className="w-full text-xs text-center border-collapse">
                            <thead className="bg-[#e0f2e9]">
                                <tr>
                                    <th className="p-1 border-b border-r border-green-200">Sem</th>
                                    <th className="p-1 border-b border-r border-green-200">Credits</th>
                                    <th className="p-1 border-b border-r border-green-200">Back Logs</th>
                                    <th className="p-1 border-b border-green-200">Fail Subjects</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white font-semibold text-blue-800">
                                {['I - I', 'I - II', 'II - I', 'II - II'].map(sem => (
                                    <tr key={sem} className="border-b border-green-100">
                                        <td className="p-1 border-r border-green-100 bg-gray-50">{sem}</td>
                                        <td className="p-1 border-r border-green-100">20 / 20</td>
                                        <td className="p-1 border-r border-green-100">Nil</td>
                                        <td className="p-1 text-blue-600">Nil</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="w-full bg-[#ef3d4c] text-white py-3 mt-auto flex justify-between px-10 text-xs font-semibold tracking-wide">
                <p>Copyright © 2026 Teegala Krishna Reddy Engineering College. All Rights Reserved.</p>
                <div className="text-right flex flex-col items-end">
                    <p>Under the Guidance of <span className="font-bold border-b border-white/50">Dr. B. Srinivas Rao</span> (Dean Academics, TKREC)</p>
                    <p className="mt-1">Designer, Developer & Maintenance - <span className="font-bold">A. Srinivas Reddy</span> (TKREC)</p>
                </div>
            </footer>

        </div>
    );
}
