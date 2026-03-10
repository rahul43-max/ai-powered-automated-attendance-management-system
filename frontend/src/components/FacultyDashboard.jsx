import React, { useState, useEffect } from 'react';
import { PlayCircle, CheckCircle, Smartphone } from 'lucide-react';

export default function FacultyDashboard({ user, onLogout }) {
    const [classId, setClassId] = useState('CSE-D');
    const [status, setStatus] = useState('idle');
    const [periodId, setPeriodId] = useState(null);
    const [attendance, setAttendance] = useState([]);

    // Load final attendance automatically if complete
    const pollResults = async (pid) => {
        try {
            const resp = await fetch(`http://127.0.0.1:5000/periods/${pid}/attendance`);
            const data = await resp.json();
            setAttendance(data);
            setStatus('finished');
        } catch (e) {
            console.error(e);
        }
    };

    const startSession = async () => {
        setStatus('running');
        try {
            const resp = await fetch(`http://127.0.0.1:5000/periods/run`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ class_id: classId })
            });
            const data = await resp.json();
            setPeriodId(data.period_id);

            // Wait roughly 60 seconds (since script simulates 60 min -> 60s)
            setTimeout(() => pollResults(data.period_id), 65000);
        } catch (e) {
            setStatus('error');
        }
    };

    const handleOverride = async (sid, cStatus) => {
        const newStatus = cStatus === 'PRESENT' ? 'ABSENT' : 'PRESENT';
        await fetch(`http://127.0.0.1:5000/periods/${periodId}/override`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_id: sid, new_status: newStatus, lecturer: user.full_name, reason: 'Manual Faculty Review' })
        });
        pollResults(periodId);
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="w-full bg-[#00008b] text-white p-4 flex justify-between shadow">
                <h1 className="text-xl font-bold border-b border-yellow-400 pb-1 italic">TKREC Faculty Terminal</h1>
                <div className="flex gap-4 items-center font-bold text-sm">
                    <span>Dr. {user.full_name}</span>
                    <button onClick={onLogout} className="bg-red-600 px-3 py-1 rounded hover:bg-red-700 border border-red-800">Logout</button>
                </div>
            </header>

            <main className="max-w-6xl mx-auto mt-8 px-4 grid grid-cols-1 md:grid-cols-2 gap-8">

                {/* Left: Engine Controls */}
                <section className="bg-white border rounded shadow p-6">
                    <h2 className="text-xl font-bold text-blue-900 border-b pb-2 mb-4">Start Smart Session (60-Min Full Period)</h2>

                    <div className="mb-4">
                        <label className="text-sm font-semibold text-gray-600 uppercase">Target Timetable Class</label>
                        <input
                            type="text"
                            value={classId}
                            onChange={e => setClassId(e.target.value)}
                            className="w-full mt-1 p-2 border rounded border-gray-300 font-mono text-lg focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    <div className="bg-yellow-50 border border-yellow-200 p-4 rounded text-sm text-gray-800 mb-6 font-medium">
                        <h4 className="font-bold text-yellow-800">ERP Autonomous AI Daemon is Active:</h4>
                        <ul className="list-disc ml-5 mt-2 flex flex-col gap-1 text-xs">
                            <li>The python `cctv_daemon.py` is actively reading the scheduled 6-period timetable in the background.</li>
                            <li>When the clock hits exactly 9:40 AM (or other designated slots), the CCTV automatically activates.</li>
                            <li>10 Min Start Grace Period (No camera check).</li>
                            <li>40 Min Core Engine (Exactly 2 targeted, shuffled student sweeps).</li>
                            <li>10 Min End Grace Period (Final sweep at minute 55).</li>
                            <li>An SMS notification will dispatch to you immediately upon final sweep.</li>
                        </ul>
                    </div>

                    <div className="w-full py-4 rounded-lg font-bold text-lg flex justify-center items-center gap-2 text-white shadow bg-[#156e3a]">
                        <CheckCircle /> Automated Attendance System is Online 24/7
                    </div>
                </section>

                {/* Right: Reviews */}
                <section className="bg-white border rounded shadow flex flex-col">
                    <div className="p-4 bg-gray-100 border-b flex justify-between items-center">
                        <h2 className="text-xl font-bold text-blue-900">Period Audit & Override</h2>
                        {status === 'finished' && <Smartphone className="text-green-600 animate-pulse" />}
                    </div>

                    <div className="flex-1 overflow-auto p-4 max-h-[500px]">
                        {status === 'idle' && <p className="text-center text-gray-400 mt-20 font-bold">Start a session to generate a report.</p>}
                        {status === 'running' && <p className="text-center text-red-500 mt-20 font-bold animate-pulse">AI Engine tracking in progress...</p>}

                        {status === 'finished' && (
                            <table className="w-full text-sm text-left border-collapse tkrec-table">
                                <thead className="bg-gray-100 uppercase text-xs">
                                    <tr>
                                        <th className="p-2 border">Roll No.</th>
                                        <th className="p-2 border">Presence</th>
                                        <th className="p-2 border">Threshold Result</th>
                                        <th className="p-2 border">Faculty Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {attendance.map(r => (
                                        <tr key={r.student_id} className="border-b hover:bg-gray-50">
                                            <td className="p-2 border font-mono font-bold text-gray-700">{r.student_id}</td>
                                            <td className="p-2 border text-center font-bold text-blue-800">{r.detections_count}/3</td>
                                            <td className="p-2 border text-center font-bold">
                                                {r.final_status === 'PRESENT' ? <span className="text-green-600">PASSED</span> : <span className="text-red-600">FAILED</span>}
                                            </td>
                                            <td className="p-2 border text-center">
                                                <button
                                                    onClick={() => handleOverride(r.student_id, r.final_status)}
                                                    className="bg-gray-200 hover:bg-gray-300 text-xs px-2 py-1 rounded font-bold border border-gray-400 w-full shadow-sm"
                                                >
                                                    Mark {r.final_status === 'PRESENT' ? 'Absent' : 'Present'}
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                </section>

            </main>
        </div>
    );
}
