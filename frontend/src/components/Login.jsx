import React, { useState } from 'react';
import { User, Lock } from 'lucide-react';

export default function Login({ onLogin }) {
    const [role, setRole] = useState('student');
    const [userId, setUserId] = useState('23R91A05L6');
    const [password, setPassword] = useState('password');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const resp = await fetch('http://127.0.0.1:5000/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, password })
            });
            const data = await resp.json();
            if (resp.ok) {
                onLogin(data);
            } else {
                setError(data.error || 'Login failed');
            }
        } catch (err) {
            setError('Server unreachable. Please check backend.');
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center bg-gray-100">
            {/* Fake Header replicating TKREC */}
            <header className="w-full bg-white flex justify-center py-4 border-b">
                <div className="flex flex-col items-center">
                    <h1 className="text-[#00008b] text-3xl font-bold font-serif tracking-wide border-b-2 border-yellow-400 pb-1">
                        TEEGALA KRISHNA REDDY ENGINEERING COLLEGE
                    </h1>
                    <p className="text-sm font-bold text-gray-600 mt-1">(UGC-AUTONOMOUS)</p>
                    <p className="text-xs text-red-600 font-semibold">(Sponsored by TKR Educational Society, Approved by AICTE, Affiliated to JNTUH Accredited by NAAC & NBA)</p>
                    <p className="text-xs text-gray-500">Medbowli, Meerpet, Balapur(M), Hyderabad, Telangana- 500097</p>
                </div>
            </header>

            {/* Fake Nav */}
            <nav className="w-full bg-[#00008b] text-white flex px-10 py-2 text-sm font-semibold shadow-md">
                <ul className="flex gap-6 mx-auto w-full max-w-6xl">
                    <li className="bg-black px-3 py-1 cursor-pointer">Home</li>
                    <li className="cursor-pointer hover:underline py-1">News Letters</li>
                    <li className="cursor-pointer hover:underline py-1">Gallary</li>
                    <li className="cursor-pointer hover:underline py-1">Study Materials ▼</li>
                    <li className="cursor-pointer hover:underline py-1">Notifications</li>
                    <li className="cursor-pointer hover:underline py-1">Syllabus</li>
                    <li className="cursor-pointer hover:underline py-1">Downloads</li>
                    <li className="cursor-pointer hover:underline py-1">Feedback</li>
                    <li className="cursor-pointer hover:underline py-1 uppercase">cbt</li>
                </ul>
            </nav>

            {/* Body Content */}
            <main className="w-full max-w-6xl flex gap-6 mt-8">

                {/* Left: Fake Slider */}
                <div className="flex-1 bg-white border border-gray-300 p-2 shadow-sm rounded-sm">
                    <div className="w-full h-[400px] bg-gray-200 overflow-hidden relative group rounded flex items-center justify-center border">
                        {/* Placeholder for the graduation photo from screenshot */}
                        <div className="absolute inset-0 bg-gradient-to-tr from-blue-900/10 to-transparent"></div>
                        <img
                            src="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=1470&auto=format&fit=crop"
                            alt="Graduation Celebration"
                            className="object-cover w-full h-full"
                        />
                        <div className="absolute left-2 top-1/2 bg-black/50 text-white p-2 rounded-full cursor-pointer hover:bg-black/70">←</div>
                        <div className="absolute right-2 top-1/2 bg-black/50 text-white p-2 rounded-full cursor-pointer hover:bg-black/70">→</div>
                    </div>
                </div>

                {/* Right: Login Panels */}
                <div className="w-80 flex flex-col gap-4">

                    <div
                        onClick={() => setRole('staff')}
                        className={`cursor-pointer border border-[#00a896] bg-[#00e5ff] text-[#006064] font-bold p-3 flex justify-between items-center ${role === 'staff' ? 'ring-2 ring-black' : ''}`}
                    >
                        <span>Staff Login</span>
                        <span>{role === 'staff' ? '▲' : '▼'}</span>
                    </div>

                    <div
                        onClick={() => setRole('student')}
                        className={`cursor-pointer border border-green-700 bg-green-600 text-white font-bold p-3 flex justify-between items-center ${role === 'student' ? 'ring-2 ring-black' : ''}`}
                    >
                        <span>Student Login</span>
                        <span>{role === 'student' ? '▲' : '▼'}</span>
                    </div>

                    <div className="border border-green-600 p-4 bg-white -mt-4 shadow-sm relative z-10 border-t-0">
                        {error && <p className="text-red-500 text-xs mb-2 font-bold">{error}</p>}
                        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                            <div className="flex items-center border border-gray-300 rounded px-2 bg-white">
                                <User className="text-gray-400 w-4 h-4" />
                                <input
                                    type="text"
                                    value={userId}
                                    onChange={(e) => setUserId(e.target.value.toUpperCase())}
                                    placeholder="Roll / Staff ID"
                                    className="w-full p-2 outline-none text-sm font-mono text-gray-700 uppercase"
                                />
                            </div>
                            <div className="flex items-center border border-gray-300 rounded px-2 bg-white">
                                <Lock className="text-gray-400 w-4 h-4" />
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Password"
                                    className="w-full p-2 outline-none text-sm font-mono text-gray-700"
                                />
                            </div>
                            <button
                                type="submit"
                                className="bg-[#1b8c4c] text-white font-bold text-sm py-2 px-6 rounded mx-auto hover:bg-[#156e3a] transition-colors"
                            >
                                Login
                            </button>
                        </form>
                    </div>

                    {/* Notifications Panel */}
                    <div className="border border-yellow-500 mt-2 bg-[#fdf2b8] shadow-sm">
                        <div className="bg-[#ffcc00] font-bold text-center py-1 text-sm text-gray-800 border-b border-yellow-500">
                            Notifications
                        </div>
                        <ul className="text-[11px] font-bold text-gray-700 p-3 flex flex-col gap-2 uppercase leading-snug">
                            <li className="hover:text-red-600 cursor-pointer">END EXAMINATIONS (SEE) MARCH-2026-TIME TABLE</li>
                            <li className="hover:text-red-600 cursor-pointer">R25 M TECH I-YEAR I-SEMESTER REGULAR END EXAMINATIONS (SEE) MARCH-2026-TIMETABLE</li>
                            <li className="hover:text-red-600 cursor-pointer mt-4">R22 M TECH I-YEAR II-SEMESTER SUPPLEMENTARY END (SEE) EXAMINATIONS MARCH-2026-TIMETABLE</li>
                            <li className="hover:text-red-600 cursor-pointer">R22 M TECH I-YEAR I-SEMESTER SUPPLEMENTARY END EXAMINATIONS MARCH-2026-TIMETABLE</li>
                            <li className="hover:text-red-600 cursor-pointer">R22-MBA I-YEAR II-SEMESTER -SUPPLEMENTARY END -(SEE) EXAMINATIONS MARCH-2026-TIME</li>
                        </ul>
                    </div>

                </div>
            </main>
        </div>
    );
}
