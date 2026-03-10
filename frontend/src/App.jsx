import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import Details from './pages/Details';
import TimeTable from './pages/TimeTable';
import Attendance from './pages/Attendance';
import SMS from './pages/SMS';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/details" element={<Details />} />
        <Route path="/timetable" element={<TimeTable />} />
        <Route path="/attendance" element={<Attendance />} />
        <Route path="/sms" element={<SMS />} />
        {/* Dummy placeholders for other tabs to prevent 404s */}
        <Route path="/marks" element={<Navigate to="/home" />} />
        <Route path="/results" element={<Navigate to="/home" />} />
        <Route path="/course-exit" element={<Navigate to="/home" />} />
        <Route path="/voting" element={<Navigate to="/home" />} />
      </Routes>
    </Router>
  );
}

export default App;
