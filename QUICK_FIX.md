# 🔧 Quick Fix for ModuleNotFoundError

## Problem
You're getting `ModuleNotFoundError: No module named 'librosa'` because:
- Python is using the global installation (`C:\Python314\python.exe`)
- But packages are installed in your virtual environment (`.venv`)
- Streamlit is running from the wrong Python interpreter

---

## ✅ Solution 1: Use the Setup Script (Easiest)

Just run this in PowerShell:

```powershell
.\setup_and_run.bat
```

This will:
1. ✅ Create/activate virtual environment
2. ✅ Install all dependencies
3. ✅ Start the app automatically

---

## ✅ Solution 2: Manual Activation

### Step 1: Activate Virtual Environment

```powershell
# Navigate to project
cd "d:\Sid python\PRONUNEX\speech-therapy-platform"

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```

**If you get an error about execution policy:**
```powershell
# Run this first (as Administrator if needed):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Try minimal requirements first
pip install -r requirements_minimal.txt
```

### Step 3: Verify Installation

```powershell
python -c "import streamlit; import librosa; print('✓ Success!')"
```

### Step 4: Run the App

```powershell
streamlit run app.py
```

---

## ✅ Solution 3: Quick Test (No Virtual Env)

If you just want to test quickly without venv:

```powershell
# Install to user directory
pip install --user streamlit librosa soundfile openai-whisper transformers g2p-en plotly pandas sqlalchemy

# Run
streamlit run app.py
```

---

## 🔍 Verifying It Works

After activation, your prompt should show `(.venv)`:

```
(.venv) PS D:\Sid python\PRONUNEX\speech-therapy-platform>
```

Then check Python path:

```powershell
python -c "import sys; print(sys.executable)"
```

Should show:
```
D:\Sid python\PRONUNEX\speech-therapy-platform\.venv\Scripts\python.exe
```

---

## ⚡ After Fixing

Once you see the Streamlit app in your browser:

1. Go to **🎙️ Practice** page
2. Click the **audio input** widget
3. Allow microphone access
4. Speak a sentence
5. Click **"Analyze My Pronunciation"**

---

## 🐛 Still Having Issues?

### Option A: Recreate Virtual Environment

```powershell
# Remove old venv
Remove-Item -Recurse -Force .venv

# Create fresh one
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements_minimal.txt
```

### Option B: Use Global Python

```powershell
# Just install globally and run
pip install streamlit librosa soundfile openai-whisper
streamlit run app.py
```

---

## 📝 What Each Solution Does

| Solution | Pros | Cons |
|----------|------|------|
| **Setup Script** | ✅ Fully automated | Requires batch file execution |
| **Manual Activation** | ✅ Full control | Multiple steps |
| **No Virtual Env** | ✅ Quickest | May conflict with other projects |

---

**Recommended:** Use **Solution 1** (setup script) for easiest setup! 🚀
