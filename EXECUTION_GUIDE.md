# AI-Powered TKREC Attendance ERP System
**Complete Execution Guide (Autonomous CCTV Edition)**

This system is built as a pure **Computer Vision Automation Daemon**. It operates autonomously based on the exact 6-period daily timetable, turning the classroom cameras on and off without human intervention.

Follow these step-by-step instructions to initialize and run the automated surveillance system from scratch via PowerShell.

---

### Step 1: Prepare the AI Training Data (Initial Only)
If you have new students joining, you must generate their 360-degree AI embeddings so the system can actively search for them later.
1. Capture faces using the webcam (Name must match Roll No format, e.g., `23R91A05L6_Nithish`):
   ```powershell
   .\env\Scripts\python.exe src\capture_faces.py
   ```
2. Train the AI model (this generates `src/face_encodings.pkl`):
   ```powershell
   .\env\Scripts\python.exe src\train_model.py
   ```

### Step 2: Initialize the ERP Database & Timetable
You must load the exact 6-Period Mon-Sat Timetable (9:40 AM starts, Lunch at 12:40 PM, etc.) into the SQLite database.
```powershell
.\env\Scripts\python.exe src\bootstrap_erp.py
```
*(This wipes and injects the perfect timetable, student data, and faculty logins).*

### Step 3: Start the Autonomous CCTV Daemon
This is the core of your project. This script runs indefinitely, reading your computer's system clock. When the clock hits 9:40 AM (or any scheduled period start), it automatically wakes up the CCTV and begins the strict **10-40-10 Minute Cycle**.

Open PowerShell and run:
```powershell
cd C:\Users\nithi\OneDrive\Desktop\IOMP
.\env\Scripts\python.exe src\cctv_daemon.py
```
**Leave this window running 24/7.** 
*Note: If you want to force a simulation immediately without waiting for 9:40 AM, you can run:`.\env\Scripts\python.exe src\cctv_daemon.py --test-run`*

---

### Step 4: The TKREC Monitoring Portal (Passive Viewing)
The web application is strictly a **Viewer** now. The faculty does not trigger the AI from the website; the site merely reads what the `cctv_daemon.py` is permanently saving into the database.

To view the live data:
1. Open a **new, separate** PowerShell window.
2. Start the API Server:
   ```powershell
   cd C:\Users\nithi\OneDrive\Desktop\IOMP
   .\env\Scripts\python.exe src\api.py
   ```
3. Open your browser to **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

**Login Roles:**
*   **Student Login:** Roll: `23R91A05L6` | Pass: `password`. You can view exactly what the TKREC portal shows (Absence logs, subject matrices).
*   **Staff Login:** ID: `FACULTY_01` | Pass: `password`. You can review the finished periods the daemon calculated, review the 95%+ confidence logs, and apply legal manual overrides if the student claims they were present.
