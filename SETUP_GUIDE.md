# AI Travel System – Setup Guide

This guide will help you set up and run the complete AI Travel System, including both the Python AI service and the Node.js application.

---

## 1. Prerequisites

- **Python 3.8+** (https://www.python.org/downloads/)
- **Node.js v14+** (https://nodejs.org/)
- **MongoDB** (https://www.mongodb.com/try/download/community)
- **pip** (comes with Python)
- **npm** (comes with Node.js)

---

## 2. Python AI Service Setup

### a. Navigate to the AI service directory
```powershell
cd "ai Travel moiz/ai_service"
```

### b. (Optional) Install virtualenv if not present
```powershell
pip install virtualenv
```

### c. Create a Virtual Environment
```powershell
python -m venv venv
```

### d. Activate the Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### e. Upgrade pip (Recommended)
```powershell
python -m pip install --upgrade pip
```

### f. Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### g. Start the Python AI Service
```powershell
python app.py
```
Or use the batch file:
```powershell
start_ai_service.bat
```

The AI service will run at: http://localhost:5001

---

## 3. Node.js App Setup

### a. Open a new terminal and go to the project root
```powershell
cd "ai Travel moiz"
```

### b. Install Node.js Dependencies
```powershell
npm install
```

### c. Start the Node.js Application
```powershell
npm start
```
Or for development mode (with auto-reload):
```powershell
npm run dev
```

The Node.js app will run at: http://localhost:3000 (or as set in your .env)

---

## 4. Running Both Services Together

You can use the provided batch file to start both services:
```powershell
start_both_services.bat
```

---

## 5. Environment Variables

- Copy `env.example` to `.env` and edit as needed for your local setup.
- Make sure MongoDB is running on your system.

---

## 6. Troubleshooting

- **Port already in use:**
  - Change the port in your `.env` file or stop the process using the port.
- **Missing dependencies:**
  - Run `pip install -r requirements.txt` (Python) or `npm install` (Node.js).
- **Virtual environment not activating:**
  - Make sure you are using the correct command for your shell (see above). If you get an execution policy error, run PowerShell as Administrator and execute:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
- **MongoDB connection errors:**
  - Ensure MongoDB is running and the URI in `.env` is correct.

---

## 7. Useful Commands

```powershell
# Python virtual environment setup
cd "ai Travel moiz/ai_service"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py

# Node.js app setup
cd "ai Travel moiz"
npm install
npm start
```

---

## 8. Accessing the App
- **Frontend:** http://localhost:3000
- **AI Service (API):** http://localhost:5001

---

For more details, see the README files in the project.